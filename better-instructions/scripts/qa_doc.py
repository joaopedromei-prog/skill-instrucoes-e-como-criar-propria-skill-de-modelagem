"""QA / Definition of Done por ad — auditoria antiburro do doc final.

Lê o doc do jeito que está e imprime, por ad, um SELO ✅/❌ do que está garantido:
- Edição (todo ad): ritmo, legenda (ou "sem legenda"), formato, e REF quando o
  formato/ritmo exige (ritmo sempre; React/CXP/CNM têm vídeo de ref).
- B-roll: exigido por formato (React/CNM) ou por pistas (b-roll, cenas de mulher,
  takes de apoio, cenas externas, antes/depois de aluna, blogueira).
- Gravação (regra do Murilo): se "Instruções para o Murilo" = "Nenhuma", não exige.
  Se houver qualquer instrução, exige cenário + microfone/áudio + takes.
Também avisa imagens duplicadas adjacentes. Não escreve nada no doc.

Uso:
    python3 qa_doc.py <fileId> [--tab <tabId>] [--ad "AD 66"]
"""
import argparse
import re

from _common import get_services, get_tab, collect_chars

AD_RE = re.compile(r"(?m)^\s*AD\s*\d+")


def section(text, start, ends):
    i = text.find(start)
    if i == -1:
        return ""
    i += len(start)
    end = len(text)
    for e in ends:
        j = text.find(e, i)
        if j != -1:
            end = min(end, j)
    return text[i:end].strip()


def has(text, *needles):
    low = text.lower()
    return any(n.lower() in low for n in needles)


def detect_formato(editor):
    if has(editor, "react"):
        return "react"
    if has(editor, "caixinha", "cxp"):
        return "cxp"
    if has(editor, "cinematográfico", "cnm", "narração"):
        return "cnm"
    if has(editor, "tela dividida", "split"):
        return "tela-dividida"
    if has(editor, "teleprompter", "formato tp", "f tp"):
        return "teleprompter"
    if has(editor, "ugc"):
        return "ugc"
    return "?"


def audit_ad(title, body):
    """Auditoria pura (texto → linhas de selo). Testável sem Google Docs."""
    editor = section(body, "Instruções para o editor de vídeo:",
                     ["Instruções para o Murilo:", "ROTEIRO"])
    murilo = section(body, "Instruções para o Murilo:", ["ROTEIRO"])
    grava = bool(murilo) and not murilo.lower().startswith("nenhuma")
    fmt = detect_formato(editor)

    rows = []

    def chk(label, ok, note=""):
        rows.append((label, ok, note))

    # ---- EDIÇÃO (todo ad) ----
    chk("ritmo", has(editor, "ritmo de tiktok", "atropelado"))
    chk("legenda", has(editor, "legenda", "sem legenda"))
    chk("formato", has(editor, "formato"))

    # ref exigida: ritmo sempre carrega ref; React/CXP/CNM têm vídeo de ref
    tem_ref = "🔗" in editor or "ref. do copy" in editor.lower() or "ref.:" in editor.lower()
    precisa_ref = has(editor, "ritmo de tiktok", "atropelado") or fmt in ("react", "cxp", "cnm")
    if precisa_ref:
        chk("referência (🔗)", tem_ref, "ritmo/React/CXP/CNM têm que carregar ref")

    # b-roll: por formato (React/CNM) ou por pistas de material de terceiro
    usa_broll = fmt in ("react", "cnm") or has(
        editor, "b-roll", "cenas de mulher", "takes de apoio", "cenas externas",
        "antes/depois", "alunas", "blogueira", "vídeos de apoio")
    if usa_broll:
        chk("ressalva b-roll", has(editor, "b-roll", "mulher que treina"),
            "tem take de terceiro → exige ressalva b-roll-realista")

    # ---- GRAVAÇÃO (regra do Murilo) ----
    if grava:
        chk("cenário", has(murilo, "cenário", "confirmar cenário"))
        chk("microfone/áudio", has(murilo, "áudio", "microfone", "lapela"))
        chk("takes", has(murilo, "takes"))
    else:
        rows.append(("(gravação)", None, "Murilo não grava (Nenhuma) — não exigido"))

    return rows, grava, fmt


def dup_images_by_ad(tab, bounds_idx):
    """Avisa imagens duplicadas adjacentes (mesma sourceUri, juntas) por ad."""
    io = tab.get("documentTab", {}).get("inlineObjects", {})

    def src(oid):
        o = io.get(oid, {})
        return (o.get("inlineObjectProperties", {}).get("embeddedObject", {})
                .get("imageProperties", {}).get("sourceUri"))

    seq = []  # (docIndex, sourceUri)
    for se in tab.get("documentTab", {}).get("body", {}).get("content", []):
        p = se.get("paragraph")
        if not p:
            continue
        for el in p.get("elements", []):
            ioe = el.get("inlineObjectElement")
            if ioe:
                seq.append((el.get("startIndex", 0), src(ioe["inlineObjectId"])))
    dups = []
    for a, b in zip(seq, seq[1:]):
        if a[1] and a[1] == b[1] and b[0] - a[0] < 200:
            # acha em qual ad caiu
            ad = next((t for idx, t in reversed(bounds_idx) if b[0] >= idx), "?")
            dups.append(ad)
    return dups


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file_id")
    ap.add_argument("--tab", default=None)
    ap.add_argument("--ad", default=None)
    args = ap.parse_args()

    docs, _ = get_services()
    doc = docs.documents().get(
        documentId=args.file_id, includeTabsContent=True).execute()
    tab = get_tab(doc, args.tab)
    chars = collect_chars(tab)
    full = "".join(c for c, _ in chars)

    bounds = [(m.start(), m.group().strip()) for m in AD_RE.finditer(full)]
    bounds_idx = [(chars[pos][1], title) for pos, title in bounds]
    dups = dup_images_by_ad(tab, bounds_idx)

    total_fail = 0
    for k, (pos, title) in enumerate(bounds):
        end = bounds[k + 1][0] if k + 1 < len(bounds) else len(full)
        if args.ad and args.ad.replace(" ", "").upper() not in title.replace(" ", "").upper():
            continue
        rows, grava, fmt = audit_ad(title, full[pos:end])
        fails = [r for r in rows if r[1] is False]
        total_fail += len(fails)
        seal = "✅ OK" if not fails else f"❌ {len(fails)} faltando"
        print(f"\n=== {title}  [{seal}]  (formato: {fmt} · Murilo grava: {'sim' if grava else 'não'})")
        for label, ok, note in rows:
            mark = "✅" if ok else ("❌" if ok is False else "—")
            print(f"   {mark} {label}" + (f"  ({note})" if note and ok is not True else ""))
        if title in dups:
            print(f"   ⚠️  imagem duplicada adjacente neste ad — rode cleanup_doc.py")

    print(f"\n{'TUDO OK' if total_fail == 0 else f'{total_fail} item(ns) faltando no total'}.")


if __name__ == "__main__":
    main()
