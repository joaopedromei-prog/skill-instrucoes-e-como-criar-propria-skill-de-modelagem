"""Lê um Google Doc e despeja: a lista de tabs (com tabId) e, para o tab alvo,
o texto em ordem de documento. Serve para o modelo localizar âncoras e ads.

Uso:
    python3 read_doc.py <fileId>                 # lista os tabs
    python3 read_doc.py <fileId> --tab <tabId>   # despeja o texto do tab
    python3 read_doc.py <fileId> --tab <tabId> --json   # saída JSON crua (chars+índices)
"""
import argparse
import json

from _common import get_services, get_tab, collect_chars


def list_tabs(doc):
    out = []

    def walk(tlist, depth=0):
        for t in tlist:
            tp = t.get("tabProperties", {})
            out.append({
                "tabId": tp.get("tabId"),
                "title": tp.get("title"),
                "depth": depth,
            })
            walk(t.get("childTabs", []), depth + 1)

    walk(doc.get("tabs", []))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file_id")
    ap.add_argument("--tab", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    docs, _ = get_services()
    doc = docs.documents().get(
        documentId=args.file_id, includeTabsContent=True
    ).execute()

    tabs = list_tabs(doc)
    if args.tab is None and tabs:
        print("TABS no documento:")
        for t in tabs:
            indent = "  " * t["depth"]
            print(f"  {indent}- {t['title']}  (tabId={t['tabId']})")
        print("\nRode de novo com --tab <tabId> para ver o conteúdo.")
        return

    tab = get_tab(doc, args.tab)
    chars = collect_chars(tab)

    if args.json:
        print(json.dumps(
            {"tabId": args.tab, "chars": [[c, i] for c, i in chars]},
            ensure_ascii=False))
        return

    text = "".join(c for c, _ in chars)
    print(f"=== TEXTO do tab {args.tab} (len={len(text)}) ===")
    print(text)


if __name__ == "__main__":
    main()
