"""Segmenta um tab em ads estruturados — barato em tokens e determinístico.
Em vez de mandar 89k caracteres pro modelo, devolve um JSON compacto por ad com:
título, hooks (code/SP/formato), seções de editor/Murilo, se o Murilo grava, e
o intervalo de índices do ad (pra escopar a escrita).

Uso:
    python3 parse_ads.py <fileId> --tab <tabId> [--ad "AD 38"]
"""
import argparse
import json
import re

from _common import get_services, get_tab, collect_chars, char_width, refs_in_range

HOOK_RE = re.compile(
    r"BUMFB\s*\|\s*(Ad[\w.]+)\s*-\s*(\w+)\s*\|\s*F\s*([A-Z]+)\s*\|\s*SP(\d+)",
    re.IGNORECASE)
# Título real do ad ("AD 38" ou "AD38" no início da linha) — não casa "Ad38.1".
AD_TITLE_RE = re.compile(r"(?m)^\s*AD\s*\d+")
NENHUMA_RE = re.compile(r"^\s*nenhuma", re.IGNORECASE)


def section(text, start_marker, end_markers):
    """Extrai o texto entre start_marker e o primeiro dos end_markers."""
    i = text.find(start_marker)
    if i == -1:
        return ""
    i += len(start_marker)
    end = len(text)
    for em in end_markers:
        j = text.find(em, i)
        if j != -1:
            end = min(end, j)
    return text[i:end].strip()


def parse_ad(title, body, start_index, refs=None):
    hooks = []
    for m in HOOK_RE.finditer(body):
        hooks.append({"name": m.group(1), "hook_id": m.group(2),
                      "formato": m.group(3).upper(), "sp": int(m.group(4))})
    editor = section(body, "Instruções para o editor de vídeo:",
                     ["Instruções para o Murilo:", "ROTEIRO", "BODY"])
    murilo = section(body, "Instruções para o Murilo:",
                     ["ROTEIRO", "BODY", "INSTRUÇÕES DE GRAVAÇÃO"])
    murilo_grava = bool(murilo) and not NENHUMA_RE.match(murilo)
    sps = {h["sp"] for h in hooks}
    formatos = sorted({h["formato"] for h in hooks})
    out = {
        "title": title.strip(),
        "start_index": start_index,
        "hooks": hooks,
        "sp_codes": sorted(sps),
        "formatos": formatos,
        "murilo_grava": murilo_grava,
        "hooks_sp1": sorted([h["name"] for h in hooks if h["sp"] == 1]),
        "hooks_externos": sorted([h["name"] for h in hooks if h["sp"] != 1]),
        "editor_instr": editor,
        "murilo_instr": murilo,
    }
    # Referências que o copy colocou (links com URL + imagens embutidas) — o
    # parser de texto não as enxerga, então surgem aqui pra serem PRESERVADAS.
    if refs is not None:
        out["copy_refs"] = refs
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file_id")
    ap.add_argument("--tab", default=None)
    ap.add_argument("--ad", default=None, help="filtrar um ad só, ex. 'AD 38'")
    args = ap.parse_args()

    docs, _ = get_services()
    doc = docs.documents().get(
        documentId=args.file_id, includeTabsContent=True).execute()
    tab = get_tab(doc, args.tab)
    chars = collect_chars(tab)
    full = "".join(c for c, _ in chars)

    def doc_idx(off):
        ch, idx = chars[off]
        return idx

    def section_of(idx, ed_i, mu_i, ro_i):
        if ed_i is not None and mu_i is not None and ed_i <= idx < mu_i:
            return "editor"
        if mu_i is not None and ro_i is not None and mu_i <= idx < ro_i:
            return "murilo"
        return "body"

    bounds = [(m.start(), m.group()) for m in AD_TITLE_RE.finditer(full)]
    ads = []
    for k, (pos, title) in enumerate(bounds):
        end = bounds[k + 1][0] if k + 1 < len(bounds) else len(full)
        body = full[pos:end]
        start_index = chars[pos][1]
        # referências do copy dentro do ad (links + imagens), por seção
        ad_start_idx = chars[pos][1]
        last_ch, last_idx = chars[end - 1]
        ad_end_idx = last_idx + char_width(last_ch)
        imgs, links = refs_in_range(tab, ad_start_idx, ad_end_idx)

        def mk(name):
            j = full.find(name, pos, end)
            return doc_idx(j) if j != -1 else None
        ed_i, mu_i, ro_i = (mk("Instruções para o editor"),
                            mk("Instruções para o Murilo"), mk("ROTEIRO"))
        refs = [{"kind": "image", "section": section_of(im["idx"], ed_i, mu_i, ro_i),
                 "uri": im["uri"]} for im in imgs]
        refs += [{"kind": "link", "section": section_of(l["idx"], ed_i, mu_i, ro_i),
                  "text": l["text"], "url": l["url"]} for l in links]
        ad = parse_ad(title, body, start_index, refs=refs)
        if args.ad and args.ad.replace(" ", "").upper() not in \
                ad["title"].replace(" ", "").upper():
            continue
        ads.append(ad)

    print(json.dumps({"tabId": args.tab, "ads": ads},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
