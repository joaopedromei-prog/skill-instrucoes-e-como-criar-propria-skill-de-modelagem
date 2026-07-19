# Glossário de GRAVAÇÃO — guia humano

> **Fonte da verdade do texto = `scripts/templates.json` (via `scripts/render.py`).**
> Este glossário é **documentação humana**: conceito, quando usar / quando NÃO usar, gatilhos, slots e exemplo. **Não copie texto canônico daqui** — renderize por código.

> **⚠️ OBRIGATÓRIOS quando o Murilo grava:** `cenario`, `microfone-lapela` (mão ou lapela) e `takes`. Regra única do Murilo: se a seção "Instruções para o Murilo" for **"Nenhuma"**, ele não grava → não exigir. Qualquer instrução na seção → exigir os 3 pra parte dele. Ver [como-melhorar.md](como-melhorar.md).

---

## cenario  ·  obrigatório (cenário)
- **Conceito:** onde gravar. **Nunca assuma** — sem indicação, sai `⚠️ CONFIRMAR cenário`.
- **Quando usar:** todo ad que o Murilo grava. **Quando NÃO:** Murilo não grava.
- **Gatilhos:** "cenário", "ambiente", "local de gravação", "onde gravar".
- **Slots:** `status` = {confirmar*, definido}; `local` = {academia, casa (quarto/sala/garagem), externa}. Copy disse o local → `status=definido,local=…`; não disse → default `confirmar`.
- **Exemplo:** `cenario-academia` / `cenario-casa`.

## microfone-lapela  ·  obrigatório (microfone)
- **Conceito:** captação de áudio (sem áudio bom o criativo morre).
- **Quando usar:** todo ad que o Murilo grava. **Quando NÃO:** Murilo não grava.
- **Gatilhos:** "microfone", "lapela", "áudio limpo", "mic na mão".
- **Slots:** `posicao` = {mão*, lapela}. "Na regata/preso na roupa" → `lapela`.
- **Exemplo:** `microfone-mao-ref` / `microfone-lapela-ref`.

## takes  ·  obrigatório (takes)
- **Conceito:** como gravar os takes pra dar opção de corte ao editor.
- **Quando usar:** todo ad que o Murilo grava. **Quando NÃO:** Murilo não grava.
- **Gatilhos:** "takes", "como gravar os takes", "vários aparelhos", "opções de corte".
- **Slots:** `variedade` = {vários aparelhos/ângulos*, take único de frente}.
- **Exemplo:** `angulos-camera-ref` (vídeo).

## figurino-regata
- **Conceito:** figurino do expert (regata) pra passar físico forte + autoridade.
- **Quando usar:** copy menciona regata/figurino do Murilo. **Quando NÃO:** spokesperson feminina (→ `figurino-roupa-treino`).
- **Gatilhos:** "camisa regata", "regata", "machão".
- **Slots:** `cor` = {preta*, branca, cinza}; `caimento` = {justa*, normal}.
- **Exemplo:** por cor → `figurino-regata-preta` / `-branca` / `-cinza`.

## figurino-roupa-treino
- **Conceito:** figurino feminino de quem treina de verdade (não propaganda).
- **Quando usar:** spokesperson/avatar feminino. **Quando NÃO:** expert masculino (→ `figurino-regata`).
- **Gatilhos:** "roupa de treino", "look academia", "roupa que valorize o shape" (feminino).
- **Slots:** `peca` = {conjunto fitness*, top + legging, macaquinho}; `cor` = {neutra*}.
- **Exemplo:** `figurino-treino-fem`.

## angulos-camera
- **Conceito:** variedade de ângulos pra dar opção de corte.
- **Quando usar:** copy pede múltiplos ângulos/câmera acompanhando. **Quando NÃO:** redundante com `takes` — combine se o copy não distingue.
- **Gatilhos:** "ângulos", "múltiplos ângulos", "câmera acompanha", "de baixo pra cima", "frontal e lateral".
- **Slots:** `variedade` = {múltiplos*, frontal fixo}.
- **Exemplo:** `angulos-camera-ref` (vídeo).

## enquadramento
- **Conceito:** altura/plano da câmera pra criar conexão com quem assiste.
- **Quando usar:** copy fala em enquadramento/altura da câmera. **Quando NÃO:** sem menção.
- **Gatilhos:** "enquadramento", "altura da câmera", "como se olhasse de frente".
- **Slots:** `altura` = {altura dos olhos*, leve de baixo pra cima}; `plano` = {meio-corpo*, corpo inteiro, close}.
- **Exemplo:** `enquadramento-ref`.

## tom
- **Conceito:** tom de fala e comunicação não-verbal.
- **Quando usar:** copy pede tom/naturalidade/leveza+autoridade. **Quando NÃO:** sem menção.
- **Gatilhos:** "tom", "tom de conversa", "naturalidade", "leveza e autoridade", "comunicação não-verbal".
- **Slots:** `registro` = {conversa natural (leveza + autoridade)*, mais enérgico, mais sério}.
- **Exemplo:** `tom-ref` (vídeo).

## lip-sync
- **Conceito:** voz gerada depois e sincronizada (ou narração voz over).
- **Quando usar:** copy menciona lip sync/dublagem/áudio gravado depois. **Quando NÃO:** áudio gravado ao vivo.
- **Gatilhos:** "lip sync", "lipsync", "dublagem", "áudio gravado depois", "narração".
- **Slots:** `tipo` = {lip sync*, só narração}.
- **Exemplo:** `lip-sync-ref` (vídeo).

## direcao-do-hook
- **Conceito:** moldura pra direção específica de como falar o hook (preserve o que o copy escreveu).
- **Quando usar:** copy dá direção específica do hook. **Quando NÃO:** sem direção específica.
- **Gatilhos:** "direção do hook", "como falar o hook", "pergunta real", "pausa e solta".
- **Slots:** (livre — preserve a direção do copy).
- **Exemplo:** (sem imagem).
