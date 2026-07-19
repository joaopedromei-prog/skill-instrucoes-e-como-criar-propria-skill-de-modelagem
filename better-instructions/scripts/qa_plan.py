"""QA do PLANO — valida o plano.json ANTES de rodar write_instructions.py.

Pega erros antes de tocar no doc: campos faltando, marcadores proibidos vazando
pro doc, `[[img:tag]]` que não existe no manifest, link sem http, etc.

Uso:
    python3 qa_plan.py plano.json

Saída: resumo OK / erros / warnings por edit. Exit 0 = OK, exit 1 = erro bloqueante.
"""
import argparse
import json
import re
import sys

from _common import load_manifest, manifest_by_tag

IMG_RE = re.compile(r"\[\[img:([^\]]+)\]\]")
# link markdown [rótulo](url) — não casa [[img:...]] (não tem "](" logo após)
LINK_RE = re.compile(r"(?<!\[)\[([^\[\]]+)\]\(([^)]+)\)")
# marcadores proibidos que NUNCA podem ir pro doc
FORBIDDEN = [
    (re.compile(r"\[obrigat", re.I), "marcador [obrigatório...]"),
    (re.compile(r"\[confirmar", re.I), "marcador [confirmar...] (use o texto canônico '⚠️ CONFIRMAR cenário', sem colchete)"),
    (re.compile(r"\[falta", re.I), "marcador [falta...]"),
    (re.compile(r"\bTODO\b"), "TODO"),
    (re.compile(r"\bver ad\s", re.I), "'ver ad X' (cada criativo é independente — repita a ref)"),
    (re.compile(r"igual ao de cima", re.I), "'igual ao de cima'"),
]


def validate_plan(plan, by_tag):
    """Valida o dict do plano. Retorna (errors, warnings): listas de (escopo, msg)."""
    errors, warnings = [], []

    if not isinstance(plan, dict) or "edits" not in plan:
        errors.append(("plano", "falta o array 'edits'"))
        return errors, warnings
    edits = plan["edits"]
    if not isinstance(edits, list) or not edits:
        errors.append(("plano", "'edits' tem que ser um array não-vazio"))
        return errors, warnings

    for i, edit in enumerate(edits):
        label = (edit.get("ad") or edit.get("label") or f"edit#{i}") if isinstance(edit, dict) else f"edit#{i}"
        if not isinstance(edit, dict):
            errors.append((label, "edit não é um objeto"))
            continue

        # 3-4: campos obrigatórios não-vazios
        for field in ("ad", "anchor", "replace_with"):
            val = edit.get(field)
            if val is None or (isinstance(val, str) and val.strip() == ""):
                errors.append((label, f"campo '{field}' faltando ou vazio"))

        rw = edit.get("replace_with")
        if not isinstance(rw, str) or not rw:
            continue  # já reportado acima

        # 5: marcadores proibidos
        for rx, name in FORBIDDEN:
            if rx.search(rw):
                errors.append((label, f"marcador proibido no replace_with: {name}"))

        # 6-7: [[img:tag]] tem que existir no manifest; sem image_urls = warning
        for tag in IMG_RE.findall(rw):
            entry = by_tag.get(tag)
            if entry is None:
                errors.append((label, f"[[img:{tag}]] não existe no manifest.json"))
            elif not entry.get("image_urls"):
                warnings.append((label, f"tag '{tag}' não tem image_urls (não vai inserir imagem)"))

        # 8: link markdown precisa de URL http/https
        for lbl, url in LINK_RE.findall(rw):
            if not re.match(r"https?://", url.strip()):
                errors.append((label, f"link '[{lbl}](...)' com URL inválida (precisa http/https): {url[:40]}"))

        # 9: política de saída — replace_with começa com '\n' (linha em branco após cabeçalho)
        if not rw.startswith("\n"):
            warnings.append((label, "replace_with não começa com '\\n' (esperado: linha em branco após o cabeçalho)"))

    return errors, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    args = ap.parse_args()

    # 1: JSON válido
    try:
        with open(args.plan, encoding="utf-8") as f:
            plan = json.load(f)
    except FileNotFoundError:
        print(f"❌ arquivo não encontrado: {args.plan}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ JSON inválido: {e}")
        sys.exit(1)

    errors, warnings = validate_plan(plan, manifest_by_tag(load_manifest()))

    n = len(plan.get("edits", [])) if isinstance(plan, dict) else 0
    print(f"Plano: {n} edit(s). Erros: {len(errors)} · Warnings: {len(warnings)}")
    for scope, msg in errors:
        print(f"  ❌ [{scope}] {msg}")
    for scope, msg in warnings:
        print(f"  ⚠️  [{scope}] {msg}")

    if errors:
        print("\nBLOQUEADO: corrija os erros antes de rodar write_instructions.py.")
        sys.exit(1)
    print("\n✅ OK pra escrever (rode write_instructions.py com --dry-run primeiro).")
    sys.exit(0)


if __name__ == "__main__":
    main()
