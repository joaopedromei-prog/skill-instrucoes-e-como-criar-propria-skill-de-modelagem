"""Helpers compartilhados: auth + leitura de estrutura do Google Doc.

Requer: pip install google-api-python-client google-auth google-auth-oauthlib
Arquivos esperados nesta pasta:
  - credentials.json  (OAuth Client tipo Desktop, baixado do Google Cloud Console)
  - token.json        (gerado por setup_auth.py)
"""
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CRED_PATH = os.path.join(SCRIPT_DIR, "credentials.json")
TOKEN_PATH = os.path.join(SCRIPT_DIR, "token.json")
MANIFEST_PATH = os.path.join(SCRIPT_DIR, "..", "examples", "manifest.json")

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
]


def get_creds():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CRED_PATH):
                sys.exit(
                    "ERRO: falta credentials.json em scripts/. "
                    "Siga scripts/SETUP.md para criar o OAuth Client."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CRED_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return creds


def get_services():
    from googleapiclient.discovery import build

    creds = get_creds()
    docs = build("docs", "v1", credentials=creds)
    drive = build("drive", "v3", credentials=creds)
    return docs, drive


def get_tab(doc, tab_id=None):
    """Retorna o objeto tab (com .documentTab.body) pelo tabId, ou o primeiro tab."""
    tabs = doc.get("tabs", [])
    if not tabs:
        # doc sem tabs explícitos: usa o body raiz
        return {"tabId": None, "documentTab": {"body": doc.get("body", {})}}
    if tab_id is None:
        return tabs[0]
    flat = []

    def walk(tlist):
        for t in tlist:
            flat.append(t)
            walk(t.get("childTabs", []))

    walk(tabs)
    for t in flat:
        if t.get("tabProperties", {}).get("tabId") == tab_id:
            return t
    sys.exit(f"ERRO: tabId {tab_id} não encontrado. Tabs: "
             + ", ".join(x.get("tabProperties", {}).get("tabId", "?") for x in flat))


def char_width(ch):
    """Largura do char em unidades UTF-16 (índice do Docs API). Emojis fora do
    BMP (ex. 🔗 🎬 🍑) ocupam 2 unidades; o resto, 1."""
    return 2 if ord(ch) > 0xFFFF else 1


def collect_chars(tab):
    """Anda pelo conteúdo do tab (parágrafos + tabelas) e devolve uma lista de
    (char, docs_index) em ordem de documento, contando índices em UTF-16."""
    chars = []

    def handle_elements(elements):
        for el in elements:
            tr = el.get("textRun")
            if not tr:
                continue
            content = tr.get("content", "")
            start = el.get("startIndex", 0)
            u = 0
            for ch in content:
                chars.append((ch, start + u))
                u += char_width(ch)

    def handle_content(content):
        for se in content:
            if "paragraph" in se:
                handle_elements(se["paragraph"].get("elements", []))
            elif "table" in se:
                for row in se["table"].get("tableRows", []):
                    for cell in row.get("tableCells", []):
                        handle_content(cell.get("content", []))

    body = tab.get("documentTab", {}).get("body", {})
    handle_content(body.get("content", []))
    return chars


def find_range(chars, anchor):
    """Acha o anchor no texto. Retorna (start_index, end_index) em índices do
    Docs API, ou None. end_index é exclusivo (pronto p/ deleteContentRange)."""
    full = "".join(c for c, _ in chars)
    pos = full.find(anchor)
    if pos == -1:
        return None
    start_index = chars[pos][1]
    last_ch, last_idx = chars[pos + len(anchor) - 1]
    end_index = last_idx + char_width(last_ch)
    return start_index, end_index


def count_occurrences(chars, anchor):
    """Quantas vezes o anchor aparece no texto (para checar unicidade)."""
    return "".join(c for c, _ in chars).count(anchor)


# Título de ad real: "AD 38" ou "AD38" no início da linha (espaço opcional).
# Case-sensitive "AD" + início de linha NÃO casa códigos de hook como "Ad38.1"
# (minúsculo e no meio da linha após "BUMFB | ").
AD_RE = re.compile(r"(?m)^\s*AD\s*\d+")


def find_ad_region(chars, ad_label):
    """Recorta os chars de um ad: do título (ex. 'AD 38') até o próximo 'AD N'.
    Retorna a sublista de chars (que carregam seus índices do Docs), ou None."""
    full = "".join(c for c, _ in chars)
    m = re.search(re.escape(ad_label), full)
    if not m:
        return None
    nxt = AD_RE.search(full, m.end())
    end = nxt.start() if nxt else len(full)
    return chars[m.start():end]


URL_RE = re.compile(r"https?://[^\s]+")
_TRAIL = ").,;:]}>\"'"


def find_url_spans(text):
    """Acha URLs em `text`. Retorna (start, end, url) com pontuação final removida."""
    spans = []
    for m in URL_RE.finditer(text):
        s, e = m.start(), m.end()
        url = m.group()
        while url and url[-1] in _TRAIL:
            url = url[:-1]
            e -= 1
        if url:
            spans.append((s, e, url))
    return spans


def build_linkify_requests_from_chars(chars, tab_id):
    """Deixa clicável toda URL presente na lista de chars dada (pode ser uma
    região recortada). Link azul sublinhado, estilo padrão do Google Docs."""
    full = "".join(c for c, _ in chars)
    reqs = []
    for s, e, url in find_url_spans(full):
        start_index = chars[s][1]
        last_ch, last_idx = chars[e - 1]
        end_index = last_idx + char_width(last_ch)
        rng = {"startIndex": start_index, "endIndex": end_index}
        if tab_id:
            rng["tabId"] = tab_id
        reqs.append({
            "updateTextStyle": {
                "range": rng,
                "textStyle": {
                    "link": {"url": url},
                    "underline": True,
                    "foregroundColor": {"color": {"rgbColor": {
                        "red": 0.066, "green": 0.333, "blue": 0.8}}},
                },
                "fields": "link,underline,foregroundColor",
            }
        })
    return reqs


def build_linkify_requests(tab, tab_id):
    """Linkifica o tab inteiro (conveniência para linkify_doc.py)."""
    return build_linkify_requests_from_chars(collect_chars(tab), tab_id)


def image_uri(tab, oid):
    """URI reinserível de uma imagem inline: sourceUri (preferida) ou contentUri."""
    o = tab.get("documentTab", {}).get("inlineObjects", {}).get(oid, {})
    img = (o.get("inlineObjectProperties", {})
            .get("embeddedObject", {}).get("imageProperties", {}))
    return img.get("sourceUri") or img.get("contentUri")


def refs_in_range(tab, start, end):
    """Referências do COPY dentro de [start, end): imagens inline, hyperlinks e
    SMART CHIPS (richLink — ex.: link pro vídeo do criativo de referência — e
    chips de pessoa). Usado pelo write_instructions pra NÃO destruir referência
    que o copy colocou (links/chips/imagens que o parser de texto não enxerga).
    Retorna (images, links): images=[{oid,uri}], links=[{text,url}].
    Os smart chips entram em `links` (text=título do chip, url=uri do arquivo)."""
    images, links = [], []

    def handle_elements(elements):
        for el in elements:
            idx = el.get("startIndex")
            in_range = idx is not None and start <= idx < end
            tr = el.get("textRun")
            if tr and in_range:
                lk = tr.get("textStyle", {}).get("link", {})
                url = lk.get("url")
                if url:
                    links.append({"idx": idx, "text": tr.get("content", "").strip(),
                                  "url": url})
            # smart chip de arquivo/URL (richLink) — referência clássica do copy
            rl = el.get("richLink")
            if rl and in_range:
                rp = rl.get("richLinkProperties", {})
                if rp.get("uri"):
                    links.append({"idx": idx, "text": rp.get("title", "referência"),
                                  "url": rp["uri"], "chip": True})
            # chip de pessoa (raro como ref, mas preserva o e-mail)
            pr = el.get("person")
            if pr and in_range:
                pp = pr.get("personProperties", {})
                if pp.get("email"):
                    links.append({"idx": idx, "text": pp.get("name") or pp["email"],
                                  "url": "mailto:" + pp["email"], "chip": True})
            io = el.get("inlineObjectElement")
            if io and in_range:
                oid = io.get("inlineObjectId")
                images.append({"idx": idx, "oid": oid, "uri": image_uri(tab, oid)})

    def handle_content(content):
        for se in content:
            if "paragraph" in se:
                handle_elements(se["paragraph"].get("elements", []))
            elif "table" in se:
                for row in se["table"].get("tableRows", []):
                    for cell in row.get("tableCells", []):
                        handle_content(cell.get("content", []))

    body = tab.get("documentTab", {}).get("body", {})
    handle_content(body.get("content", []))
    # dedup links iguais
    seen, uniq = set(), []
    for l in links:
        if l["url"] not in seen:
            seen.add(l["url"]); uniq.append(l)
    return images, uniq


def load_manifest():
    import json
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        return json.load(f)


def manifest_by_tag(manifest):
    return {e["tag"]: e for e in manifest.get("examples", [])}
