"""Garante que todo arquivo do Drive referenciado no manifest (video_refs,
anti_refs e image_urls) esteja como "qualquer pessoa com o link pode ver".
Assim os links de exemplo/B-roll abrem pro editor sem pedir acesso.

Links que não são do Google Drive (ex. TikTok) são ignorados.

Uso:
    python3 ensure_shared.py [--dry-run]
"""
import argparse
import re

from _common import get_services, load_manifest

DRIVE_ID_RES = [
    re.compile(r"/file/d/([\w-]+)"),
    re.compile(r"[?&]id=([\w-]+)"),
    re.compile(r"/document/d/([\w-]+)"),
]


def drive_id(url):
    for rx in DRIVE_ID_RES:
        m = rx.search(url)
        if m:
            return m.group(1)
    return None


def collect_ids(manifest):
    ids = {}
    for e in manifest["examples"]:
        for key in ("video_refs", "anti_refs", "image_urls"):
            for url in e.get(key, []):
                fid = drive_id(url)
                if fid:
                    ids.setdefault(fid, []).append(e["tag"])
    return ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    _, drive = get_services()
    ids = collect_ids(load_manifest())
    print(f"{len(ids)} arquivo(s) do Drive referenciado(s).")

    done, failed = 0, []
    for fid, tags in ids.items():
        if args.dry_run:
            print(f"  (dry) {fid}  <- {', '.join(sorted(set(tags)))}")
            continue
        try:
            drive.permissions().create(
                fileId=fid, body={"role": "reader", "type": "anyone"}).execute()
            done += 1
            print(f"  OK {fid}")
        except Exception as ex:  # noqa: BLE001
            msg = str(ex)
            if "already" in msg.lower() or "duplicate" in msg.lower():
                done += 1
                print(f"  já público {fid}")
            else:
                failed.append(fid)
                print(f"  FALHOU {fid}: {msg[:90]}")

    if not args.dry_run:
        print(f"\n{done} compartilhado(s)/ok.", end="")
        if failed:
            print(f" Falhas (cheque acesso): {', '.join(failed)}")
        else:
            print()


if __name__ == "__main__":
    main()
