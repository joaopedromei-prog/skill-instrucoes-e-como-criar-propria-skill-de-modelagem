"""Aplica as instruções melhoradas no Google Doc via batchUpdate.

Segurança e robustez:
- ESCOPO POR AD: cada edição pode trazer "ad" (ex. "AD 38"); a âncora é buscada
  só dentro daquele ad, evitando editar o ad errado por frase repetida.
- UNICIDADE: se a âncora aparecer mais de uma vez no escopo, a edição é pulada.
- IDEMPOTÊNCIA: se o texto novo já estiver presente, a edição é pulada.
- LOG DE REVERSÃO: o texto original substituído é salvo em scripts/revert_log.jsonl
  (só texto, alguns KB) — dá pra desfazer manualmente.
- LINKIFY ESCOPADO: só os ads tocados têm URLs linkificadas (não o tab inteiro).
- IMAGENS: no máximo --max-images (default 1), dimensionadas por ALTURA (pequenas).

PROCESSA UMA EDIÇÃO POR VEZ e re-busca o doc entre elas (índices deslocam).

Uso:
    python3 write_instructions.py <fileId> --plan plano.json [--tab <tabId>]
                                  [--max-images 1] [--img-height 140] [--dry-run]

Formato do plano:
{
  "edits": [
    {
      "ad": "AD 38",                 # escopo (recomendado)
      "anchor": "texto exato a substituir",
      "replace_with": "texto canônico (render.py)",
      "images": ["headline-invideo-letra-branca"]
    }
  ]
}
"""
import argparse
import json
import os
import re

from _common import (get_services, get_tab, collect_chars, find_range,
                     count_occurrences, find_ad_region, load_manifest,
                     manifest_by_tag, build_linkify_requests,
                     build_linkify_requests_from_chars, char_width, SCRIPT_DIR,
                     refs_in_range)


def u16len(s):
    """Comprimento de s em unidades UTF-16 (índice do Docs API)."""
    return sum(char_width(c) for c in s)

REVERT_LOG = os.path.join(SCRIPT_DIR, "revert_log.jsonl")


def loc(index, tab_id):
    d = {"index": index}
    if tab_id:
        d["tabId"] = tab_id
    return d


def rng(start, end, tab_id):
    d = {"startIndex": start, "endIndex": end}
    if tab_id:
        d["tabId"] = tab_id
    return d


LINK_BLUE = {"color": {"rgbColor": {"red": 0.066, "green": 0.333, "blue": 0.8}}}
# [[img:tag]] = imagem do manifest · [[imgurl:URL]] = imagem por URL crua
# (referência do copy, reinserida) · [rótulo](url) = link na palavra
TOKEN_RE = re.compile(
    r"\[\[imgurl:(https?://[^\]]+)\]\]"   # 1: imagem por URL crua
    r"|\[\[img:([^\]]+)\]\]"              # 2: imagem por tag do manifest
    r"|\[([^\]]+)\]\((https?://[^)]+)\)"  # 3-4: link na palavra
)


def parse_tokens(md):
    """Texto plano + links [rótulo](url) + marcadores de imagem.
    Retorna (plain, links[(off,len,url)], imgs[(off, spec)]) em offsets Python,
    onde spec é {"tag": ...} (manifest) ou {"url": ...} (URL crua)."""
    plain, links, imgs, last = "", [], [], 0
    for m in TOKEN_RE.finditer(md):
        plain += md[last:m.start()]
        if m.group(1) is not None:               # imagem por URL crua
            imgs.append((len(plain), {"url": m.group(1)}))
        elif m.group(2) is not None:             # imagem por tag do manifest
            imgs.append((len(plain), {"tag": m.group(2)}))
        else:                                     # link na palavra
            label, url = m.group(3), m.group(4)
            links.append((len(plain), len(label), url))
            plain += label
        last = m.end()
    plain += md[last:]
    return plain, links, imgs


def _img_reqs(base, urls, tab_id, h):
    """Imagens LADO A LADO: inseridas consecutivas, sem quebra entre elas."""
    return [{"insertInlineImage": {
                "location": loc(base + k, tab_id), "uri": u,
                "objectSize": {"height": {"magnitude": h, "unit": "PT"}}}}
            for k, u in enumerate(urls)]


def build_requests(start, end, replace_with, image_urls, by_tag, tab_id,
                   img_height, strip_bullets=True):
    requests = []
    if replace_with is not None:
        plain, links, imgpts = parse_tokens(replace_with)
        requests.append({"deleteContentRange": {"range": rng(start, end, tab_id)}})
        requests.append({"insertText": {"location": loc(start, tab_id),
                                        "text": plain + "\n"}})
        # linka cada palavra/termo na sua URL (offsets em UTF-16)
        for off, length, url in links:
            s = start + u16len(plain[:off])
            requests.append({"updateTextStyle": {
                "range": rng(s, s + u16len(plain[off:off + length]), tab_id),
                "textStyle": {"link": {"url": url}, "underline": True,
                              "foregroundColor": LINK_BLUE},
                "fields": "link,underline,foregroundColor"}})
        # imagens dos marcadores, no ponto certo (de trás pra frente p/ não
        # deslocar os offsets ainda não inseridos)
        total = 0
        for off, spec in sorted(imgpts, key=lambda x: x[0], reverse=True):
            if "url" in spec:                    # imagem por URL crua (ref do copy)
                urls = [spec["url"]]
            else:                                # imagem por tag do manifest
                urls = (by_tag.get(spec["tag"]) or {}).get("image_urls", [])
            base = start + u16len(plain[:off])
            requests += _img_reqs(base, urls, tab_id, img_height)
            total += len(urls)
        p = start + u16len(plain) + 1 + total
        if strip_bullets:
            requests.append({"deleteParagraphBullets": {"range": rng(start, p, tab_id)}})
    else:
        # edição só-imagem: insere lado a lado logo após a âncora
        requests.append({"insertText": {"location": loc(end, tab_id), "text": "\n"}})
        requests += _img_reqs(end + 1, image_urls, tab_id, img_height)
    return requests


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file_id")
    ap.add_argument("--plan", required=True)
    ap.add_argument("--tab", default=None)
    ap.add_argument("--img-per-tag", type=int, default=0,
                    help="imagens por tag em edição só-imagem (0 = todas)")
    ap.add_argument("--img-height", type=float, default=140.0)
    ap.add_argument("--keep-bullets", action="store_true",
                    help="não remover numeração/bullets dos trechos inseridos")
    ap.add_argument("--no-carry-refs", action="store_true",
                    help="NÃO preservar referências (links/imagens) do copy que "
                         "estejam no trecho substituído (padrão: preserva)")
    ap.add_argument("--force", action="store_true",
                    help="sobrescrever mesmo quando há imagem de referência do "
                         "copy que não dá pra reinserir (risco de perdê-la)")
    ap.add_argument("--strict-refs", action="store_true",
                    help="modo estrito: em vez de carregar refs do copy sozinho, "
                         "PULA a edição e lista as refs pra você costurar à mão")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    with open(args.plan, encoding="utf-8") as f:
        plan = json.load(f)
    edits = plan.get("edits", [])
    by_tag = manifest_by_tag(load_manifest())

    docs, _ = get_services()

    applied, skipped, touched_ads, full_linkify = 0, [], set(), False

    for edit in edits:
        ad = edit.get("ad")
        label = edit.get("label", ad or "?")
        anchor = edit["anchor"]
        replace_with = edit.get("replace_with")
        tags = edit.get("images", [])

        # resolve imagens -> urls (1 por tag por default; cada conceito mostra a sua)
        urls = []
        for t in tags:
            e = by_tag.get(t)
            tag_urls = (e or {}).get("image_urls", [])
            if tag_urls:
                n = args.img_per_tag
                urls.extend(tag_urls if n <= 0 else tag_urls[:n])
            else:
                print(f"[{label}] nota: tag '{t}' não tem imagem (só link/conceito).")

        # re-busca o doc (índices atuais) e define o escopo
        doc = docs.documents().get(
            documentId=args.file_id, includeTabsContent=True).execute()
        tab = get_tab(doc, args.tab)
        chars = collect_chars(tab)
        scope = chars
        if ad:
            region = find_ad_region(chars, ad)
            if region is None:
                print(f"[{label}] ERRO: ad '{ad}' não encontrado — pulado.")
                skipped.append(label)
                continue
            scope = region

        # idempotência: texto novo já presente?
        scope_text = "".join(c for c, _ in scope)
        if replace_with and replace_with in scope_text:
            print(f"[{label}] já aplicado (texto novo já presente) — pulado.")
            continue

        # unicidade
        n = count_occurrences(scope, anchor)
        if n == 0:
            print(f"[{label}] âncora não encontrada — pulada: {anchor[:60]!r}")
            skipped.append(label)
            continue
        if n > 1:
            print(f"[{label}] âncora AMBÍGUA ({n}x no escopo) — pulada por "
                  f"segurança. Use uma âncora mais específica ou escopo por ad.")
            skipped.append(label)
            continue

        start, end = find_range(scope, anchor)

        # PRESERVAR REFERÊNCIAS DO COPY: links/imagens que o copy colocou dentro
        # do trecho que vamos sobrescrever não podem sumir. Carrega-os pro texto
        # novo (link na palavra + imagem reinserida) no fim da seção.
        if replace_with is not None and not args.no_carry_refs:
            imgs_copy, links_copy = refs_in_range(tab, start, end)
            lost_links = [l for l in links_copy if l["url"] not in replace_with]
            carry_imgs = [im for im in imgs_copy if im.get("uri")]
            no_uri = [im for im in imgs_copy if not im.get("uri")]
            # modo estrito: não carrega sozinho — lista e pula pra você decidir
            if args.strict_refs and (lost_links or carry_imgs or no_uri):
                print(f"[{label}] PULADO (--strict-refs): refs do copy no trecho que "
                      f"NÃO estão no texto novo — costure-as e rode de novo:")
                for l in lost_links:
                    tag = " [chip]" if l.get("chip") else ""
                    print(f"     🔗{tag} {l['text'][:60]!r} -> {l['url']}")
                for im in (carry_imgs + no_uri):
                    print(f"     🖼️ imagem -> {im.get('uri') or '(sem URL reinserível)'}")
                skipped.append(label)
                continue
            if no_uri and not args.force:
                print(f"[{label}] PULADO: {len(no_uri)} imagem(ns) de referência "
                      f"do copy sem URL reinserível — preserve manualmente ou use "
                      f"--force (perde a imagem).")
                skipped.append(label)
                continue
            extra = ""
            for l in lost_links:
                lbl = l["text"] or "referência"
                extra += f"\n\n📎 Referência do copy: [{lbl}]({l['url']})"
            for im in carry_imgs:
                extra += f"\n\n📎 Referência do copy:\n[[imgurl:{im['uri']}]]"
            if extra:
                replace_with = replace_with + extra
                print(f"[{label}] referências do copy preservadas: "
                      f"{len(lost_links)} link(s), {len(carry_imgs)} imagem(ns).")

        requests = build_requests(start, end, replace_with, urls, by_tag,
                                  args.tab, args.img_height,
                                  strip_bullets=not args.keep_bullets)

        if args.dry_run:
            print(f"[{label}] DRY-RUN — {len(requests)} request(s) em [{start},{end}), "
                  f"{len(urls)} imagem(ns).")
            continue

        # log de reversão (texto original substituído)
        if replace_with is not None:
            with open(REVERT_LOG, "a", encoding="utf-8") as logf:
                logf.write(json.dumps({
                    "file_id": args.file_id, "tab": args.tab, "ad": ad,
                    "original": anchor, "replaced_with": replace_with},
                    ensure_ascii=False) + "\n")

        docs.documents().batchUpdate(
            documentId=args.file_id, body={"requests": requests}).execute()
        print(f"[{label}] OK — instrução atualizada + {len(urls)} imagem(ns).")
        applied += 1
        if ad:
            touched_ads.add(ad)
        else:
            full_linkify = True

    # pós-passe nos ads tocados: linkify escopado + limpar numeração órfã.
    if not args.dry_run and applied:
        doc = docs.documents().get(
            documentId=args.file_id, includeTabsContent=True).execute()
        tab = get_tab(doc, args.tab)
        chars = collect_chars(tab)
        link_reqs, debullet_reqs = [], []
        if full_linkify:
            link_reqs = build_linkify_requests(tab, args.tab)
        for ad in touched_ads:
            region = find_ad_region(chars, ad)
            if not region:
                continue
            if not full_linkify:
                link_reqs += build_linkify_requests_from_chars(region, args.tab)
            # tira bullets/numeração órfã das duas seções de instrução do ad
            # (lista numerada antiga deixa um "1." vazio depois do nosso texto)
            rtext = "".join(c for c, _ in region)
            i = rtext.find("Instruções para o")
            j = rtext.find("ROTEIRO", i if i != -1 else 0)
            if i != -1 and j != -1:
                rngd = {"startIndex": region[i][1], "endIndex": region[j][1]}
                if args.tab:
                    rngd["tabId"] = args.tab
                debullet_reqs.append({"deleteParagraphBullets": {"range": rngd}})
        if link_reqs:
            docs.documents().batchUpdate(
                documentId=args.file_id, body={"requests": link_reqs}).execute()
            print(f"Links clicáveis aplicados: {len(link_reqs)} "
                  f"({'tab inteiro' if full_linkify else 'ads tocados'}).")
        if debullet_reqs:
            docs.documents().batchUpdate(
                documentId=args.file_id, body={"requests": debullet_reqs}).execute()
            print(f"Numeração órfã limpa em {len(debullet_reqs)} ad(s).")

    print(f"\nFeito: {applied} edição(ões) aplicada(s).", end="")
    if skipped:
        print(f" Puladas: {', '.join(skipped)}")
    else:
        print()


if __name__ == "__main__":
    main()
