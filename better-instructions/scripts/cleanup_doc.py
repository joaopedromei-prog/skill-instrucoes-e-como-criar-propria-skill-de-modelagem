"""Limpa um tab: (1) remove imagens duplicadas adjacentes (mesma sourceUri, juntas),
(2) colapsa parágrafos em branco consecutivos em um só e (3) tira numeração órfã
(o '1.' fantasma que sobra de lista numerada antiga). Útil depois de re-execuções
que acumularam imagens/linhas repetidas ou deixaram bullets soltos.

Atua só nos parágrafos de nível superior do corpo (não mexe em tabelas).

Uso:
    python3 cleanup_doc.py <fileId> --tab <tabId> [--dry-run] [--gap 100]
"""
import argparse

from _common import get_services, get_tab

LOC = None


def loc_rng(start, end, tab_id):
    d = {"startIndex": start, "endIndex": end}
    if tab_id:
        d["tabId"] = tab_id
    return d


def body_paragraphs(tab):
    """Lista (start, end, text, image_ids[]) dos parágrafos do corpo."""
    out = []
    for se in tab.get("documentTab", {}).get("body", {}).get("content", []):
        p = se.get("paragraph")
        if not p:
            continue
        text, imgs = "", []
        for el in p.get("elements", []):
            tr = el.get("textRun")
            if tr:
                text += tr.get("content", "")
            io = el.get("inlineObjectElement")
            if io:
                imgs.append((el.get("startIndex"), io["inlineObjectId"]))
        out.append({"start": se["startIndex"], "end": se["endIndex"],
                    "text": text, "imgs": imgs, "bullet": "bullet" in p})
    return out


def find_orphan_bullet(tab):
    """Acha um parágrafo VAZIO que ainda carrega marcador de lista (bullet/número)
    — sobra de lista numerada antiga, que renderiza um '1.' fantasma. Retorna
    (start,end) do parágrafo pra tirar o bullet."""
    for p in body_paragraphs(tab):
        if p["bullet"] and not p["imgs"] and p["text"].strip() == "":
            return p["start"], p["end"]
    return None


def src_of(tab, oid):
    o = tab["documentTab"].get("inlineObjects", {}).get(oid, {})
    emb = o.get("inlineObjectProperties", {}).get("embeddedObject", {})
    return emb.get("imageProperties", {}).get("sourceUri")


def find_dup_image_para(tab, gap):
    """Acha um parágrafo de imagem que é duplicata adjacente (mesma sourceUri,
    perto da imagem anterior). Retorna (start,end) do parágrafo a apagar."""
    imgs = []
    for para in body_paragraphs(tab):
        for idx, oid in para["imgs"]:
            imgs.append((idx, oid, para["start"], para["end"]))
    imgs.sort()
    prev = None
    for idx, oid, ps, pe in imgs:
        src = src_of(tab, oid)
        if prev and src and src == prev[0] and idx - prev[1] < gap:
            return ps, pe
        prev = (src, idx)
    return None


def find_extra_blank(tab):
    """Acha um parágrafo em branco EXTRA logo após um cabeçalho de instruções
    ("Instruções para o editor de vídeo:" / "...Murilo:"). Mantém só 1 linha em
    branco depois do cabeçalho. NÃO mexe no espaçamento do resto do doc."""
    paras = body_paragraphs(tab)
    for i, p in enumerate(paras):
        if not p["text"].strip().startswith("Instruções para o"):
            continue
        empties = []
        j = i + 1
        while j < len(paras):
            q = paras[j]
            if not q["imgs"] and q["text"].strip() == "":
                empties.append(q)
                j += 1
            else:
                break
        if len(empties) > 1:
            e = empties[0]  # apaga o primeiro extra; mantém 1
            return e["start"], e["end"]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file_id")
    ap.add_argument("--tab", default=None)
    ap.add_argument("--gap", type=int, default=100)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    docs, _ = get_services()

    def fetch():
        doc = docs.documents().get(
            documentId=args.file_id, includeTabsContent=True).execute()
        return get_tab(doc, args.tab)

    def delete(start, end):
        docs.documents().batchUpdate(documentId=args.file_id, body={"requests": [
            {"deleteContentRange": {"range": loc_rng(start, end, args.tab)}}]}).execute()

    def debullet(start, end):
        docs.documents().batchUpdate(documentId=args.file_id, body={"requests": [
            {"deleteParagraphBullets": {"range": loc_rng(start, end, args.tab)}}]}).execute()

    imgs_removed, blanks_removed, bullets_cleared = 0, 0, 0

    # fase 1: imagens duplicadas
    while True:
        tab = fetch()
        hit = find_dup_image_para(tab, args.gap)
        if not hit:
            break
        if args.dry_run:
            print(f"(dry) apagaria imagem duplicada em {hit}")
            break
        delete(*hit)
        imgs_removed += 1

    # fase 2: linhas em branco consecutivas
    while True:
        tab = fetch()
        hit = find_extra_blank(tab)
        if not hit:
            break
        if args.dry_run:
            print(f"(dry) colapsaria linha em branco em {hit}")
            break
        delete(*hit)
        blanks_removed += 1

    # fase 3: numeração órfã (1. fantasma de lista numerada antiga)
    while True:
        tab = fetch()
        hit = find_orphan_bullet(tab)
        if not hit:
            break
        if args.dry_run:
            print(f"(dry) tiraria numeração órfã em {hit}")
            break
        debullet(*hit)
        bullets_cleared += 1

    print(f"Imagens duplicadas removidas: {imgs_removed} · "
          f"linhas em branco colapsadas: {blanks_removed} · "
          f"numeração órfã limpa: {bullets_cleared}")


if __name__ == "__main__":
    main()
