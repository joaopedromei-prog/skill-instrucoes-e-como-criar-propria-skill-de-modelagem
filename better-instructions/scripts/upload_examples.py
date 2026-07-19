"""Sobe as imagens de examples/img/ para uma pasta no Drive, deixa públicas
(anyone-with-link) e grava a drive_url de cada uma no manifest.json (casando
pelo campo 'arquivo').

Uso:
    python3 upload_examples.py            # usa/ cria a pasta "better-instructions-examples"
    python3 upload_examples.py --folder <DRIVE_FOLDER_ID>

A URL gravada é a forma direta usável pelo Docs API insertInlineImage:
    https://drive.google.com/uc?id=<FILE_ID>
"""
import argparse
import json
import mimetypes
import os
import sys

from _common import get_services, MANIFEST_PATH, SCRIPT_DIR

IMG_DIR = os.path.join(SCRIPT_DIR, "..", "examples", "img")
FOLDER_NAME = "better-instructions-examples"


def ensure_folder(drive, folder_id):
    if folder_id:
        return folder_id
    q = (f"name='{FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder' "
         "and trashed=false")
    res = drive.files().list(q=q, fields="files(id,name)").execute()
    files = res.get("files", [])
    if files:
        return files[0]["id"]
    meta = {"name": FOLDER_NAME, "mimeType": "application/vnd.google-apps.folder"}
    folder = drive.files().create(body=meta, fields="id").execute()
    return folder["id"]


def make_public(drive, file_id):
    drive.permissions().create(
        fileId=file_id,
        body={"role": "reader", "type": "anyone"},
    ).execute()


def main():
    from googleapiclient.http import MediaFileUpload

    ap = argparse.ArgumentParser()
    ap.add_argument("--folder", default=None, help="Drive folder ID (opcional)")
    args = ap.parse_args()

    docs, drive = get_services()
    folder_id = ensure_folder(drive, args.folder)

    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = json.load(f)

    if not os.path.isdir(IMG_DIR):
        sys.exit(f"ERRO: pasta {IMG_DIR} não existe. Coloque as imagens lá.")

    # cache p/ não subir o mesmo arquivo 2x (uma imagem pode estar em várias tags)
    uploaded_urls = {}
    uploaded = 0
    missing_files = []

    for entry in manifest["examples"]:
        images = entry.get("images", [])
        urls = []
        for fname in images:
            if fname in uploaded_urls:
                urls.append(uploaded_urls[fname])
                continue
            path = os.path.join(IMG_DIR, fname)
            if not os.path.isfile(path):
                missing_files.append(fname)
                continue
            mime = mimetypes.guess_type(path)[0] or "image/png"
            media = MediaFileUpload(path, mimetype=mime)
            meta = {"name": fname, "parents": [folder_id]}
            f = drive.files().create(body=meta, media_body=media,
                                     fields="id").execute()
            fid = f["id"]
            make_public(drive, fid)
            url = f"https://drive.google.com/uc?id={fid}"
            uploaded_urls[fname] = url
            urls.append(url)
            uploaded += 1
            print(f"OK  [{entry['tag']}] {fname} -> {url}")
        entry["image_urls"] = urls

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"\n{uploaded} imagem(ns) subida(s). Pasta Drive: {folder_id}")
    if missing_files:
        print("Arquivos listados no manifest mas ausentes em img/:",
              ", ".join(sorted(set(missing_files))))
    sem_nada = [e["tag"] for e in manifest["examples"]
                if not e.get("image_urls") and not e.get("video_refs")]
    if sem_nada:
        print("Tags ainda sem nenhum exemplo (imagem ou vídeo):",
              ", ".join(sem_nada))


if __name__ == "__main__":
    main()
