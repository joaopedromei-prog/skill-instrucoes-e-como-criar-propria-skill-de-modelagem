# Exemplos pendentes (banco de referência)

Tags do `examples/manifest.json` que ainda não têm exemplo visual. Quando uma instrução usa uma dessas tags, ela sai **sem imagem/ref** — registre no relatório "falta exemplo de X" e, quando der, cadastre o exemplo.

Como cadastrar: imagem em `examples/img/` + `upload_examples.py` (preenche `image_urls`); ou link de vídeo direto no `manifest.json` (`video_refs`) **sempre com `ref_label`** (o que olhar na ref).

## 🔴 Prioridade alta (conceitos muito usados, sem NENHUM exemplo)
Imagem estática ajudaria muito o editor/Murilo:
- `cenario-academia` — print de um bom enquadramento de academia.
- `microfone-mao-ref` — Murilo com mic na mão estilo entrevista.
- `enquadramento-ref` — meio-corpo, altura dos olhos, 9:16.
- `tom-ref` — vídeo de referência de tom natural.
- `figurino-regata-preta` / `figurino-regata-branca` / `figurino-regata-cinza` — referência de caimento.
- `formato-ugc` — exemplo de UGC orgânico (formato default, hoje sem nada).
- `formato-tela-dividida` — split screen.

## 🟡 Sem imagem estática (têm só vídeo) — opcional
Já carregam `🔗 Ref.:` em vídeo; uma imagem estática seria bônus:
`formato-react`, `formato-cxp`, `cxp-nativa`, `formato-cinematografico`, `criativo-atropelado-ref`, `ritmo-viral-ref`, `dopaminergico-ref`, `corte-seco-ref`, `voz-feminina-ref`, `lip-sync-ref`, `b-roll-realista`, `legenda-interativa-tipografia`.

## ⚪ Baixa prioridade (conceitos raros, sem exemplo)
`leia-legenda-preta`, `leia-legenda-branca`, `figurino-treino-fem`, `cenario-casa`, `angulos-camera-ref`, `microfone-lapela-ref`.

> Mantenha esta lista em dia: ao adicionar um exemplo, tire a tag daqui. Pra ver o estado atual a qualquer momento: `python3 -c "import json;[print(e['tag']) for e in json.load(open('examples/manifest.json'))['examples'] if not e.get('image_urls') and not e.get('video_refs')]"`.
