# Glossário de EDIÇÃO — guia humano

> **Fonte da verdade do texto = `scripts/templates.json` (via `scripts/render.py`).**
> Este glossário é **documentação humana**: conceito, quando usar / quando NÃO usar, gatilhos, slots e exemplo. **Não copie texto canônico daqui** — sempre renderize por código (`render.py <template> --slots …`).

> **⚠️ OBRIGATÓRIOS em TODA edição:** `ritmo` (`ritmo-tiktok-viral` ou `criativo-atropelado`), `legenda` (`legenda-minimalista`; se não tem legenda, escrever "sem legenda" + motivo) e `formato` (do código **F XXX** do hook). `b-roll-realista` sempre que houver take de terceiro. Ver checklist em [como-melhorar.md](como-melhorar.md).

Para adicionar template novo: crie o verbete em `scripts/templates.json` (texto + triggers + slots + example) e documente aqui. Se tiver imagem/vídeo, cadastre no `manifest.json` com `ref_label`.

---

## legenda-minimalista
- **Conceito:** legenda limpa que não compete com a imagem (default de legenda).
- **Quando usar:** legenda padrão do criativo. **Quando NÃO:** copy pede tipografia/palavras-chave em destaque (→ `legenda-interativa-tipografia`) ou não há legenda (→ escrever "sem legenda").
- **Gatilhos:** "legenda minimalista", "legenda mínima/limpa/simples", "legenda dinâmica".
- **Slots:** `cor` = {branca*}.
- **Exemplo:** `legenda-min-branca` (imagem).

## legenda-leia-a-legenda
- **Conceito:** card "Leia a legenda 👇" que empurra o usuário pra descrição.
- **Quando usar:** copy manda ler a legenda/descrição. **Quando NÃO:** legenda comum.
- **Gatilhos:** "leia a legenda", "leia a descrição", "manda ler a legenda".
- **Slots:** `cor` = {preta-fundo-branco*, branca-fundo-preto}; `momento` = {no meio do criativo*, no início, no fim}.
- **Exemplo:** `leia-legenda-preta` / `leia-legenda-branca`.

## legenda-interativa-tipografia
- **Conceito:** legenda com movimento — tamanhos/fontes/cores/posições variando.
- **Quando usar:** copy pede **explicitamente** tipografia, palavras-chave em destaque, estilo Isadora Nogueira. **Quando NÃO:** só "dinâmica" sozinha = minimalista.
- **Gatilhos:** "legenda interativa", "tipografia(s)", "palavra(s)-chave em destaque", "estilo Isadora Nogueira".
- **Slots:** (nenhum).
- **Exemplo:** `legenda-interativa-tipografia` (vídeo).

## headline-invideo
- **Conceito:** texto ancorado na tela nos pontos de ênfase.
- **Quando usar:** copy pede headline/título na tela, frase de choque. **Quando NÃO:** texto comum de legenda.
- **Gatilhos:** "headline invídeo", "headline ancorada/simples", "texto/título na tela".
- **Slots:** `estilo` = {letra-branca-borda-preta*, fundo-branco-letra-preta, fundo-vermelho-letra-branca}.
- **Exemplo:** por estilo → `headline-invideo-letra-branca` / `-fundo-branco` / `-fundo-vermelho` (imagens).

## musica-de-fundo
- **Conceito:** trilha de fundo abaixo da voz.
- **Quando usar:** copy menciona música/trilha. **Quando NÃO:** copy pede "sem música" (slot `usar=não`).
- **Gatilhos:** "música", "música de fundo", "trilha", "som de fundo", "sem música".
- **Slots:** `usar` = {sim*, não}; `energia` = {média-alta*, baixa, alta}.
- **Exemplo:** (conceito de áudio, sem imagem).

## ritmo-tiktok-viral  ·  obrigatório (ritmo)
- **Conceito:** ritmo acelerado, sem tempo morto. **Sempre carrega a ref de velocidade.**
- **Quando usar:** ritmo padrão (default de ritmo). **Quando NÃO:** copy pede "atropelado" (→ `criativo-atropelado`). Escolha **um** dos dois, nunca os dois.
- **Gatilhos:** "ritmo de TikTok viral", "ritmo viral", "rápido e dinâmico", "acelerar o vídeo", "manter o ritmo".
- **Slots:** `aceleracao` = {leve (1.1–1.2x)*, sem aceleração}.
- **Exemplo:** `ritmo-viral-ref` (3 vídeos + `ref_label`).

## corte-seco
- **Conceito:** troca de take sem transição.
- **Quando usar:** copy fala em cortes secos/dinâmicos. **Quando NÃO:** já coberto por ritmo/atropelado — não empilhe se for redundante.
- **Gatilhos:** "corte seco", "cortes secos", "cortes dinâmicos".
- **Slots:** (nenhum).
- **Exemplo:** `corte-seco-ref` (vídeo).

## criativo-atropelado  ·  obrigatório (ritmo)
- **Conceito:** ritmo apertado, acelerado, cortes até dentro da fala.
- **Quando usar:** copy pede "atropelado". **Quando NÃO:** ritmo normal (→ `ritmo-tiktok-viral`). Um ou outro.
- **Gatilhos:** "criativo atropelado", "atropelado", "deixa/atropela o criativo".
- **Slots:** `velocidade` = {1.1x–1.2x*, 1.3x ou mais}.
- **Exemplo:** `criativo-atropelado-ref` (vídeo + `ref_label`).

## formato  ·  obrigatório (formato)
- **Conceito:** formato do criativo (do código **F XXX** do hook).
- **Quando usar:** sempre (todo ad declara formato). **Quando NÃO emitir junto:** se `tipo=CXP`, use `caixinha-de-perguntas` e diga o formato numa frase — não emita os dois.
- **Gatilhos:** "formato", "react", "UGC", "tela dividida", "CXP", "cinematográfico", "CNM", "teleprompter", "TP", "F TP".
- **Slots:** `tipo` = {UGC*, React, Tela dividida, CXP, React + UGC, Cinematográfico (CNM), Teleprompter (TP)}; `genero_spokesperson` = {feminino, masculino, —*}.
- **Teleprompter (TP):** `F TP` / "formato TP" = UGC do **próprio Murilo** gravando, só que **lendo a copy no teleprompter**; o vídeo ainda tem que ser **orgânico e dinâmico** (cara de TikTok, natural — nunca leitura robótica/travada). Como o **Murilo grava**, exija o checklist de gravação dele (cenário + microfone + takes).
- **Exemplo:** por tipo → `formato-ugc` / `formato-react` / `formato-tela-dividida` / `formato-cxp` / `formato-cinematografico` / `formato-teleprompter`.

## voz-feminina-narracao
- **Conceito:** narração em voz feminina estilo blogueira.
- **Quando usar:** F CNM, narração de mulher. **Quando NÃO:** expert falando (lip sync).
- **Gatilhos:** "voz feminina", "narração (ao fundo)", "voz de mulher", "F CNM".
- **Slots:** `dinamica` = {ritmo bom, sem pausa*, mais suave}.
- **Exemplo:** `voz-feminina-ref` (vídeo + `ref_label`).

## takes-dopaminergicos
- **Conceito:** troca rápida de takes pra segurar atenção.
- **Quando usar:** narração corre sobre muitos takes (CNM/UGC dopaminérgico). **Quando NÃO:** redundante com ritmo — combine se o copy não distingue.
- **Gatilhos:** "dopaminérgico", "takes cinematográficos", "vários aparelhos", "selecionar os takes".
- **Slots:** (nenhum).
- **Exemplo:** `dopaminergico-ref` (vídeo + `ref_label`).

## b-roll-realista  ·  obrigatório (b-roll)
- **Conceito:** ressalva fixa — b-roll só com material realista de mulher que treina, nunca vulgar.
- **Quando usar:** **sempre** que houver take/cena que não é o expert (React, CNM, "cenas de mulher", "takes de apoio", "vídeos externos"). **Quando NÃO:** criativo 100% expert gravando.
- **Gatilhos:** "b-roll", "takes de apoio", "cenas de mulher", "vídeos de apoio", "cenas externas".
- **Slots:** (nenhum — ressalva fixa, com `video_refs` do que QUEREMOS e `anti_refs` do que EVITAR).
- **Exemplo:** `b-roll-realista` (vídeos + anti-refs).

## caixinha-de-perguntas
- **Conceito:** sticker nativo de caixinha de pergunta do Instagram.
- **Quando usar:** formato CXP (use este, não `formato=CXP` em paralelo). **Quando NÃO:** outros formatos.
- **Gatilhos:** "caixinha de perguntas", "caixinha de pergunta", "CXP".
- **Slots:** `tipo` = {nativa do Instagram*, ilustrada}.
- **Exemplo:** `cxp-nativa` / `cxp-ilustrada` (vídeo).
