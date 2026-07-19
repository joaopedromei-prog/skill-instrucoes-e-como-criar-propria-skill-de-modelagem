# Como melhorar (o modo de agir)

O reasoning que a skill segue para transformar o rascunho do João em instrução canônica. Determinístico: **mesmo input → mesma saída**. A flexibilidade mora só nos slots.

## Os 5 passos, por ad

### 1. Detectar conceitos (casar gatilhos)
Leia as instruções de gravação e edição do ad. Para cada trecho, procure um **gatilho** nos glossários ([edição](glossario-edicao.md), [gravação](glossario-gravacao.md)). Um trecho pode disparar mais de um template (ex. "legenda minimalista branca e música baixinha" → `legenda-minimalista` + `musica-de-fundo`).

### 2. Preencher slots
Para cada template detectado, leia o que o João frisou e preencha os slots:
- Achou modificador explícito ("colorida", "preta", "de baixo pra cima", "0,5s") → usa esse valor.
- Não achou → usa o **default** (o valor marcado com `*`).
- Valor fora da lista do slot → use o mais próximo e registre no relatório que foi adaptado.

Mapa de modificadores comuns:
- Cores: branca / preta / amarela / colorida / cinza / neutra.
- Posição: centro / centro-baixo / rodapé / topo.
- Intensidade: leve / médio / forte; baixa / média / alta.
- Duração: "0,5s", "1 a 2 segundos", "rápido".

### 3. Emitir o texto canônico — SEMPRE por `render.py`
**A fonte da verdade do texto é o `scripts/templates.json`, emitido pelo `scripts/render.py`. Nunca escreva a prosa canônica à mão** (nem copie dos glossários — eles são guia humano). Rode `render.py <template> --slots k=v`. Os slots, condicionais (`{slot=valor→…}`) e a linha de ref são resolvidos pelo código. Os glossários servem só pra você decidir **qual** template e **quais** slots.

### 4. Anexar o exemplo — SEMPRE que existir
**Regra firme:** toda instrução cujo template tem **imagem** ou **link de referência** DEVE carregá-lo na própria instrução. O editor precisa da referência pra entender, e cada criativo vai pra um editor diferente.
- O `render.py` já **embute o link de ref no texto** automaticamente (quando o template tem `video_refs`), com `— o que olhar` (`ref_label`).
- **Imagem: mecanismo principal é o marcador `[[img:tag]]`** dentro do `replace_with`, no fim da instrução correspondente (ex.: a legenda termina com `\n[[img:legenda-min-branca]]`). O `write_instructions.py` insere a imagem **logo abaixo daquela instrução** — não no fim da seção. Use **`render.py --with-img`** pra já vir com o marcador. O campo `images` do plano é só **fallback** de compatibilidade.
- **Cada criativo é único e independente:** nunca escreva "ver ad X" / "igual ao de cima". Repita o link/imagem em cada criativo que precisar.
- Tag sem imagem nem link → escreva a instrução e registre no relatório "falta exemplo de X" (ver `references/exemplos-pendentes.md`).

### 5. Preservar a direção criativa específica
Tudo que o João escreveu e que **nenhum slot cobre** (ex. "ela saiu do P pro M em 2 semanas", "seguir a ref do Ad5.3", uma fala específica) é **mantido na íntegra**. A skill troca o termo vago pela versão canônica; não apaga intenção criativa.

**Respeite a separação em TÓPICOS (não funda).** Se o copy separou direções em **linhas/tópicos diferentes**, cada uma vira **uma instrução própria** no resultado — nunca cole duas direções distintas numa frase só. Ex.: no rascunho
> Ancorar gráfico 3D quando ele falar "três porções"
> No "bunda quadrada", ancorar silhueta quadrada vs redonda
> CTA: seta no botão Saiba Mais

são **3 tópicos** → saem como **3 instruções separadas** (uma linha em branco entre elas), não uma só "Ancoragens: … ; … ; …". Juntar tópicos distintos é erro.

### 6. NUNCA apagar a referência que o copy colocou (regra dura)
O copy quase sempre cola uma **referência** de criativo num conceito. Ela vem em **3 formas**, e as duas mais comuns são **invisíveis** ao texto puro:
1. **Smart chip (`richLink`)** — o mais comum: um chip tipo `BUMFB Ad5.13 - G74 F UGC+REACT … (STORIE).mp4` linkando o **vídeo do criativo de referência** no Drive. **Não é texto nem imagem** — é um elemento `richLink`. Some sem deixar rastro no dump de texto.
2. **Imagem embutida** (print de ref).
3. **Hyperlink** numa palavra (às vezes sem texto visível).

**Essa referência é sagrada: jamais pode sumir quando você reescreve a seção.**
- Antes de reescrever, **sempre** olhe o campo **`copy_refs`** do `parse_ads.py` — ele lista links, **smart chips** e imagens por seção (o `refs_in_range` enxerga `richLink`/`person`/hyperlink/imagem; o texto puro não).
- Traga a referência **clara dentro da instrução** do conceito a que ela pertence: `🔗 Ref. do copy (criativo de referência): [título do chip](url) — o que olhar nela`.
- O `write_instructions.py` é a rede de segurança: detecta links/chips/imagens do copy no trecho a sobrescrever e **carrega-os** pro texto novo. Imagem sem URL reinserível → ele **pula e avisa** (não destrói). Nunca use `--force` por cima de uma ref sem garantir que foi preservada.
- **Se um chip já foi apagado** (run antigo): o **título do chip é o nome do arquivo no Drive** — dá pra recuperar o link buscando no Drive (`drive.files().list(q="name contains 'Ad5.13 - G74'")`). A API do Docs **não recria smart chip**, então reinsira como **link clicável** com o título do arquivo (mesma referência, clicável).

## Exemplos de transformação

**Entrada do João:** `legenda minimalista`
→ template `legenda-minimalista`, `cor=branca` (default), `posicao=centro-baixo` (default)
→ emite o texto canônico com branca + centro-baixo
→ anexa `legenda-min-branca`.

**Entrada:** `legenda minimalista colorida lá embaixo`
→ `cor=colorida`, `posicao=rodapé`
→ texto canônico com colorida + rodapé
→ anexa `legenda-min-colorida`.

**Entrada:** `camisa regata branca, fala no tom de conversa`
→ `figurino-regata` (`cor=branca`) + `tom` (`registro=conversa natural`)
→ dois blocos canônicos, anexa `figurino-regata-branca` (+ `tom-ref` se houver).

**Entrada:** `ritmo de TikTok viral, seguir a ref do Ad5.3`
→ `ritmo-tiktok-viral` (defaults) + preserva "seguir a ref do Ad5.3"
→ texto canônico de ritmo + a linha de referência mantida.

## Checklist OBRIGATÓRIO de gravação

Antes de finalizar um ad, decida se **o Murilo grava** aquele criativo:

**Sinal definitivo:** a seção **"Instruções para o Murilo"**.
- Se diz **"Nenhuma"** → Murilo **não grava nada** → não mexer nas instruções de gravação.
- Se tem instruções → Murilo **grava** (pelo menos parte) → aplicar o checklist abaixo à parte que ele grava.

**O que o SPx significa (por hook):** pegue o SPx do nome do hook (`BUMFB | AdX.Y - Gnn | F XXX | SPx | …`). **SP1 = quem grava aquele hook é o Murilo**; **SP≠1 (SP0, SP19…) = spokesperson externo / voz feminina / UGC** naquele hook.
- Caso **misto** (comum): hooks **SP≠1** (voz feminina) **mas** a seção do Murilo tem instruções → ele grava só o **body**. Continue exigindo o checklist para a parte que ele grava (o body), não para os hooks externos.
- Só pule a gravação por inteiro quando a seção do Murilo for **"Nenhuma"**.

**Quando o Murilo grava**, as instruções de gravação (da parte dele) **são obrigadas a conter os 3 elementos**. Se faltar qualquer um, **a skill adiciona** usando o template e o default:

1. **Cenário** → se o copywriter **disse** onde gravar, renderize `cenario` com `status=definido` e `local=<o que ele disse>`. Se **não disse**, renderize `cenario` no default (`status=confirmar`) → entra um **⚠️ CONFIRMAR cenário** em vez de assumir academia. Nunca invente o cenário.
2. **Microfone — mão ou lapela** → template `microfone-lapela` (default: **microfone na mão**, estilo entrevista).
3. **Como gravar os takes** → template `takes` (default: gravar a copy inteira em vários aparelhos/ângulos, dando opção de corte).

Se o João já especificou algum desses, use o que ele disse (preenchendo o slot). Só complete o que estiver faltando. No relatório, liste o que foi **adicionado por obrigatoriedade** vs. o que já existia.

> Atenção: hooks dentro do mesmo ad podem ter SPx diferentes. Se houver hooks SP1 e não‑SP1 misturados, aplique a obrigatoriedade só à parte SP1.

## Checklist OBRIGATÓRIO de edição

Vale para **todo** ad (edição sempre existe). As instruções de edição são obrigadas a declarar:

1. **Ritmo** → template `ritmo-tiktok-viral` (default) ou `criativo-atropelado` se o João pediu atropelado. Sempre dizer o ritmo.
2. **Estilo de legenda** → o **default é `legenda-minimalista`** (branca). Só use `legenda-interativa-tipografia` quando o copy **explicitamente** pedir legenda com tipografia/tamanhos/cores variados ou **palavras-chave em destaque** (não basta "dinâmica" — "dinâmica" sozinha = minimalista). Se o criativo **não** usa legenda (ex.: CXP com caixinha, ou narração que conduz), escrever **"sem legenda"** e o porquê.
3. **Formato** → template `formato`. Pegue do **código `F XXX`** do nome do hook (ver `formato-da-casa.md`); se não houver código, infira das instruções.

**Ressalva de B-roll (obrigatória quando há B-rolls):** se o criativo usa takes/cenas que **não** são o expert gravando (formatos React, Cinematográfico/CNM, ou qualquer menção a takes/cenas/b-roll/“vídeos de mulher”), **adicione sempre** o template `b-roll-realista` — material realista do cotidiano de quem treina, nunca vulgar. Sem exceção.

Se o João já especificou algum item, use o dele e só complete o que falta. No relatório, liste o que foi **adicionado por obrigatoriedade**.

## Regras de decisão

- **Sempre que houver template, use o template.** Frase nova só para o que nenhum template cobre.
- **Um template, uma saída.** Não misture variações na mesma frase.
- **Mútua-exclusão (não empilhe templates redundantes).** Quando dois templates dizem quase a mesma coisa, emita **só um** (o mais específico) e absorva o detalhe do outro:
  - `ritmo-tiktok-viral` **ou** `criativo-atropelado` — escolha 1 de ritmo (nunca os dois).
  - `caixinha-de-perguntas` já cobre o `formato=CXP` — **não** emita os dois; use a caixinha e diga o formato numa frase.
  - `takes-dopaminergicos` / `corte-seco` / ritmo descrevem cadência parecida — se o copy não distingue, combine numa só.
- **Merge entra ANTES da linha de ref.** Ao costurar a especificidade do copy num texto que já termina em `🔗 Ref.:`, use `render.py --merge "..."` (ele põe o trecho no corpo, antes do link). **Nunca** concatene texto depois do `🔗 Ref.:` — gruda no link e fica ilegível.
- **Toda ref diz O QUE OLHAR.** O `ref_label` do manifest vira o "— repare em X" no fim da linha de ref. Ref nova no banco → já cadastre com `ref_label`.
- **Instrução lidera pelo RESULTADO.** Padrão: *[o que é pra entregar] → [como fazer] → [🔗 ref: o que olhar]*. Os textos canônicos já vêm assim; a direção criativa que você escrever segue o mesmo padrão.
- **Sem template?** Não invente um canônico silenciosamente: escreva a melhor instrução clara possível, marque no relatório como "candidato a template novo" e ofereça adicionar ao glossário.
- **Linguagem:** simples, imperativa, direta. Frases curtas. Português do João, mantendo o jargão da casa.

## Substituir mesclando (política de escrita no doc)

**SUBSTITUIR, não empilhar.** Reescreva a seção inteira de instruções (editor / Murilo) — não deixe a versão antiga em cima e adicione embaixo. O resultado final substitui o conteúdo original.

Para cada instrução do copywriter:
1. **Case com o template** e **mescle**: pegue o texto canônico do template (via `render.py`) e **costure dentro dele TODAS as especificidades** que o copywriter deu — sem perder nada. Ex.: se ele diz "avatar mulher com fenótipo brasileiro", o texto final de formato/lip-sync precisa carregar "avatar feminino, fenótipo brasileiro". Links e números do copywriter também entram.
2. **Não existe template pra aquilo?** Reescreva a instrução de forma clara, com emoji, preservando 100% do conteúdo.
3. **Itens obrigatórios que faltam** (gravação: cenário/microfone/takes · edição: ritmo/legenda/formato · ressalva de b-roll quando há B-roll) → entram como instruções novas na seção.

**Formato da seção reescrita:**
- Texto normal (sem numeração/bullets — o `write_instructions.py` tira os bullets).
- **Uma linha em branco (double enter) entre cada instrução.**
- **Uma linha em branco logo após o cabeçalho** ("Instruções para o editor de vídeo:" / "Instruções para o Murilo:") antes da 1ª instrução — componha o `replace_with` começando com `\n`.
- Cada instrução começa com o **emoji padrão** do template (já vem do `render.py`).
- A referência entra junto da instrução, **sempre** — como **link numa palavra** (markdown `[rótulo](url)`), nunca a URL crua. O `render.py` já formata assim (`🔗 Ref.: [vídeo 1](url) · … — o que olhar`) e o `write_instructions.py` aplica o link no rótulo.

**Como escrever (execução):** componha o bloco novo da seção inteira (cada instrução mesclada, separadas por linha em branco) e use como `anchor` no plano o **conteúdo atual completo daquela seção** (pegue do `parse_ads.py`), com `replace_with` = bloco novo. Assim a seção é trocada inteira, limpa.

**Nunca** deixe marcadores tipo `[obrigatório...]` no documento. O que mudou vai **só no relatório** pro João.

## Saída final por ad

Monte o bloco no [formato da casa](formato-da-casa.md): "Instruções para o editor de vídeo" (edição) + "Instruções para o Murilo" (gravação), em **blocos limpos SEM numeração/bullets**, cada conceito com seu texto canônico (do `render.py`) e o marcador `[[img:tag]]` no fim da instrução correspondente — o `write_instructions.py` resolve pra `insertInlineImage` logo abaixo dela.
