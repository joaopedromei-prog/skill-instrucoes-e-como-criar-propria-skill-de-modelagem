"""Renderiza o texto canônico de um template em CÓDIGO (determinístico).
O modelo não escreve a prosa — só decide template + slots; isso economiza tokens
e garante que a mesma entrada gera sempre a mesma instrução.

Uso:
    python3 render.py <template_id> [--slots cor=branca,posicao=centro]
    python3 render.py --list                # lista templates + triggers (p/ detecção)
    python3 render.py --list --section edicao

Saída: JSON {template, slots, text, image_tags, video_refs, anti_refs}.
O campo image_tags vai direto no "images" do plano de write_instructions.py.
"""
import argparse
import json
import os
import re

from _common import SCRIPT_DIR, load_manifest, manifest_by_tag

TEMPLATES_PATH = os.path.join(SCRIPT_DIR, "templates.json")


def load_templates():
    with open(TEMPLATES_PATH, encoding="utf-8") as f:
        return json.load(f)["templates"]


def _resolve_slots(tpl, given):
    slots = {}
    for name, spec in tpl.get("slots", {}).items():
        slots[name] = given.get(name, spec.get("default"))
    return slots


def _base_text(tpl, slots):
    if "text_by" in tpl:
        key = tpl["text_by"]["slot"]
        m = tpl["text_by"]["map"]
        val = slots.get(key)
        if val in m:
            return m[val]
        # fallback: default do slot
        default = tpl["slots"][key]["default"]
        return m.get(default, "")
    return tpl.get("text", "")


def _resolve_example(tpl, slots):
    ex = tpl.get("example", {})
    if not ex:
        return None
    if "by_slot" in ex:
        return ex["map"].get(slots.get(ex["by_slot"]), ex.get("default_tag"))
    return ex.get("tag")


# condicional inline {slot=valor→texto} / {slot≠valor→texto} (P0-2: evita que
# cláusula de um valor "vaze" pra outro — ex.: dica de academia no cenário casa)
COND_RE = re.compile(r"\{(\w+)\s*(≠|!=|=)\s*([^→}]+?)\s*→\s*([^{}]*)\}")


def _eval_conditionals(text, slots):
    def repl(m):
        name, op, val, out = m.group(1), m.group(2), m.group(3).strip(), m.group(4)
        eq = str(slots.get(name, "")) == val
        keep = eq if op == "=" else (not eq)
        return out if keep else ""
    prev = None
    while prev != text:
        prev = text
        text = COND_RE.sub(repl, text)
    return text


def _insert_merge(text, merge):
    """Insere a especificidade do copy ANTES da linha de referência (🔗/✅/❌),
    pra nunca colar o texto do copy na mesma linha do link (P0-1)."""
    if not merge:
        return text
    merge = merge.strip()
    marks = [text.find(m) for m in ("\n🔗", "\n✅", "\n❌") if text.find(m) != -1]
    if marks:
        i = min(marks)
        return text[:i].rstrip() + " " + merge + text[i:]
    return text.rstrip() + " " + merge


def render(tid, given_slots, merge=None, with_img=False):
    templates = load_templates()
    if tid not in templates:
        raise SystemExit(f"ERRO: template '{tid}' não existe. "
                         f"Use --list para ver os disponíveis.")
    tpl = templates[tid]
    slots = _resolve_slots(tpl, given_slots)
    text = _base_text(tpl, slots)
    had_vr_placeholder = "{video_refs}" in text  # b-roll já injeta inline

    # condicionais primeiro, depois substitui {slot} (usando as_text quando houver)
    text = _eval_conditionals(text, slots)
    for name, spec in tpl.get("slots", {}).items():
        val = slots[name]
        sub = spec.get("as_text", {}).get(val, val) if "as_text" in spec else val
        text = text.replace("{" + name + "}", str(sub))

    # exemplo -> imagem/vídeo no manifest
    tag = _resolve_example(tpl, slots)
    entry = manifest_by_tag(load_manifest()).get(tag, {}) if tag else {}
    video_refs = entry.get("video_refs", [])
    anti_refs = entry.get("anti_refs", [])
    ref_label = entry.get("ref_label")  # P1-5: o que OLHAR na referência
    image_tags = [tag] if (tag and entry.get("image_urls")) else []

    # links viram PALAVRAS clicáveis em sintaxe markdown [rótulo](url) — o
    # write_instructions.py converte isso em link na palavra (economiza tela).
    def fmt_refs(urls, label):
        return " · ".join(f"[{label} {i + 1}]({u})" for i, u in enumerate(urls))

    text = text.replace("{video_refs}", fmt_refs(video_refs, "vídeo"))
    text = text.replace("{anti_refs}", fmt_refs(anti_refs, "evitar"))

    # mescla do copy entra ANTES da linha de ref (nunca cola no link)
    text = _insert_merge(text, merge)

    # se o template tem ref de vídeo e não a injetou inline, anexa em nova linha,
    # SEMPRE dizendo o que observar (ref_label) — instrução anti-burro
    if video_refs and not had_vr_placeholder:
        ref_line = "\n🔗 Ref.: " + fmt_refs(video_refs, "vídeo")
        if ref_label:
            ref_line += " — " + ref_label
        text = text.rstrip() + ref_line

    # limpeza leve
    text = re.sub(r"  +", " ", text).replace(" .", ".").replace(" ,", ",")
    text = text.replace("( ", "(").strip()

    # mecanismo principal de imagem: já devolve o marcador [[img:tag]] no fim da
    # instrução (write_instructions o resolve pra imagem logo abaixo dela)
    if with_img:
        for t in image_tags:
            text += f"\n[[img:{t}]]"

    return {"template": tid, "slots": slots, "text": text,
            "image_tags": image_tags, "video_refs": video_refs,
            "anti_refs": anti_refs, "ref_label": ref_label}


def list_templates(section=None):
    templates = load_templates()
    out = []
    for tid, t in templates.items():
        if section and t.get("secao") != section:
            continue
        out.append({"id": tid, "secao": t.get("secao"),
                    "obrigatorio": t.get("obrigatorio"),
                    "triggers": t.get("triggers", []),
                    "slots": {k: {"default": v.get("default"),
                                  "values": v.get("values")}
                              for k, v in t.get("slots", {}).items()}})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("template_id", nargs="?")
    ap.add_argument("--slots", default="", help="ex: cor=branca,posicao=centro")
    ap.add_argument("--merge", default=None,
                    help="especificidade do copy a costurar no corpo (entra ANTES "
                         "da linha de ref, nunca colado no link)")
    ap.add_argument("--with-img", action="store_true",
                    help="já devolve o texto com o marcador [[img:tag]] no fim "
                         "(mecanismo principal de imagem)")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--section", default=None, choices=["edicao", "gravacao"])
    args = ap.parse_args()

    if args.list:
        print(json.dumps(list_templates(args.section), ensure_ascii=False, indent=2))
        return
    if not args.template_id:
        raise SystemExit("Informe um template_id ou use --list.")

    given = {}
    for pair in args.slots.split(","):
        if "=" in pair:
            k, v = pair.split("=", 1)
            given[k.strip()] = v.strip()
    print(json.dumps(render(args.template_id, given, merge=args.merge,
                            with_img=args.with_img),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
