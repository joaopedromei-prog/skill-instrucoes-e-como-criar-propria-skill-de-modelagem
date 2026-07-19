"""Deixa TODA URL de texto plano clicável (link azul sublinhado) num tab.
Útil para consertar links já inseridos como texto puro.

Uso:
    python3 linkify_doc.py <fileId> --tab <tabId> [--dry-run]
"""
import argparse

from _common import get_services, get_tab, build_linkify_requests


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file_id")
    ap.add_argument("--tab", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    docs, _ = get_services()
    doc = docs.documents().get(
        documentId=args.file_id, includeTabsContent=True).execute()
    tab = get_tab(doc, args.tab)
    reqs = build_linkify_requests(tab, args.tab)

    if not reqs:
        print("Nenhuma URL encontrada.")
        return
    if args.dry_run:
        for r in reqs:
            print(r["updateTextStyle"]["textStyle"]["link"]["url"])
        print(f"\n{len(reqs)} URL(s) seriam linkificadas (dry-run).")
        return

    docs.documents().batchUpdate(
        documentId=args.file_id, body={"requests": reqs}).execute()
    print(f"{len(reqs)} URL(s) agora estão clicáveis.")


if __name__ == "__main__":
    main()
