# Como criar a sua própria skill de criativos (do jeito que a `criativos-bumbumflix` foi criada)

> **Para quem é este guia:** um copywriter — humano ou IA — que quer ter uma skill igual à
> `criativos-bumbumflix`, mas para a **sua** oferta, o **seu** expert e a **sua** voz. Aqui você não
> vai aprender "como criar uma skill genérica"; você vai aprender, arquivo por arquivo e passo por
> passo, **exatamente como a skill `criativos-bumbumflix` foi construída**, e o que você tem que
> escrever no lugar de cada peça pra montar a versão da sua operação.
>
> No fim, um agente de IA (Claude, etc.) lendo a SUA skill vai escrever criativos indistinguíveis dos
> que **você** escreve à mão — porque a skill não sabe "copywriting genérico", ela sabe a **sua letra**.

---

## A ideia que faz essa skill funcionar (leia antes de tudo)

A `criativos-bumbumflix` não é "um prompt que escreve anúncio". É uma **máquina que reproduz um
copywriter específico** (o João). O segredo dela está numa frase, que é a primeira coisa escrita no
`SKILL.md`:

> "O valor de um criativo do João não está no TEMA — está na **VOZ** (pt-BR falado de verdade), na
> **DIGESTIBILIDADE** (uma ideia por frase, zero complexidade) e na **SEQUÊNCIA DE BLOCOS
> PSICOLÓGICOS** que ele monta. Imitar só o assunto e errar essas três coisas produz um anúncio
> genérico de IA."

**Toda a skill existe pra proteger essas 3 coisas.** É por isso que ela tem arquivos separados pra
voz (`dna-estilo.md`), pra estrutura persuasiva (`blocos.md`) e pra os fatos da oferta (`oferta.md`) —
e é por isso que ela funciona.

**Seu primeiro trabalho, antes de escrever qualquer arquivo:** responda, pra a sua operação, a
mesma pergunta —
> "O que faz um criativo MEU parecer escrito por mim, e não por uma IA?"

Escreva as suas 3 respostas. Podem ser as mesmas do João (voz/digestibilidade/blocos) ou outras
(ex.: "humor seco", "prova social agressiva", "storytelling em 1ª pessoa"). Essas 3 coisas viram a
tese da sua skill. Sem isso definido, você vai construir uma máquina de anúncio genérico com um tema
diferente — que é exatamente o que a skill do João foi feita pra NÃO ser.

---

## O mapa da skill: o que tem dentro e por que

Abra a pasta da `criativos-bumbumflix`. É isto:

```
criativos-bumbumflix/
├── SKILL.md                       ← o cérebro: quando disparar + o processo de 8 passos
└── references/                    ← o conhecimento, lido sob demanda
    ├── oferta.md                  ← a FICHA FACTUAL (tudo que pode ser afirmado; fora daqui = alucinação)
    ├── dna-estilo.md              ← a VOZ (léxico, ritmo, regras de fala, anti-padrões de IA)
    ├── blocos.md                  ← a ESTRUTURA (20 tipos de hook + 5 esqueletos de body)
    ├── corpus/*.md                ← 58 criativos REAIS do João, verbatim (o calibrador de voz)
    ├── corpus-index.txt           ← índice do corpus por formato/speaker
    ├── fatias-performance.md      ← o que dá dinheiro hoje (ranking de público, 30 dias)
    └── hooks-log.md               ← log das últimas entregas (anti-repetição)
```

Cada arquivo tem um trabalho. A regra de ouro da arquitetura: **o `SKILL.md` decide, as `references/`
sabem.** O `SKILL.md` fica enxuto e diz ao agente QUANDO abrir cada referência — em vez de despejar
tudo de uma vez (o que estoura a memória do agente) ou não dar contexto nenhum (o que faz ele
inventar). Isso se chama **divulgação progressiva** e é o que separa uma skill de um prompt gigante.

Nas próximas seções, vamos construir cada peça — na ordem em que **você** deve construí-las (que não é
a ordem em que o agente as lê).

---

## PARTE 1 — Junte o seu corpus (comece por aqui, sempre)

**A `criativos-bumbumflix` foi destilada de 58 criativos reais do João + 11 de outros copywriters da
casa (pra contraste).** Sem esse corpus, o `dna-estilo.md` e o `blocos.md` seriam opinião. Com ele,
são fato observado. O corpus é a fundação; tudo depois é análise dele.

**O que fazer para a sua skill:**
1. Junte **20 a 60 criativos seus** que você considera excelentes e representativos. Quanto mais,
   melhor a calibração. Salve cada um como um arquivo `.md` verbatim (texto exato, sem "melhorar").
2. Junte **alguns criativos de colegas ou concorrentes** que soam DIFERENTE de você. Eles viram o
   material de contraste — é olhando o que você NÃO faz que a sua voz fica nítida. (Na skill do João,
   os copywriters "Cpy Phi" e "Cpy Fiss" servem exatamente pra isso — veja `dna-estilo.md` §6.)
3. Nomeie os arquivos com um padrão que já carregue metadados. O João usa:
   `BUMFB___Ad5.1_-_G21___F_REACT___SP3___Edt_Matheus.md` — que codifica oferta, número do ad, grupo,
   **formato** (`F REACT`), **quem grava** (`SP3`) e editor. Isso vira o `corpus-index.txt`.
4. Escreva o `corpus-index.txt`: uma linha por criativo, agrupado por formato, pra o agente escolher
   "2–3 exemplos do MESMO formato que vou escrever" antes de escrever. Essa instrução — *"leia 2–3 do
   mesmo formato imediatamente antes de escrever"* — é o **calibrador de voz mais forte que existe**.
   Exemplo real bate mil adjetivos descrevendo estilo.

> **Por que isto primeiro:** você não consegue escrever as regras da sua voz sem ter o material pra
> observar. Todo o resto deste guia é você lendo o seu próprio corpus e anotando os padrões.

---

## PARTE 2 — Escreva a ficha factual (`oferta.md`)

Este é o arquivo que **impede a IA de mentir**. A regra, escrita no `SKILL.md`, é dura:
*"É a fonte de verdade — fato que não está aqui não entra na copy."*

Veja como o `oferta.md` do João é organizado (copie a estrutura, troque o conteúdo):

| Seção | O que contém no `oferta.md` do João | O que VOCÊ escreve |
|---|---|---|
| **O expert** | Murilo, credenciais afirmadas ("+10 anos em treino feminino"), fama, jeito de falar | Seu expert/marca, o que ele legitimamente pode afirmar |
| **A persona (avatar)** | Dores verbatim, rotinas, desejos, objeções (objeção → resposta) | Seu público: dores nas palavras DELE, objeções e como você as responde |
| **Mecanismo do PROBLEMA** | "Síndrome da Bunda Morta" — todas as formas de descrever, estatísticas, causas | O "vilão invisível" da sua oferta, com as frases exatas que você usa |
| **Mecanismo da SOLUÇÃO** | "Sequência Ativadora" + "Truque da Contração", o que é, o que NÃO exige | O seu método nomeado, seus componentes fixos |
| **Produto / funil** | O que o CTA entrega (aula grátis), preço, garantia | Pra onde o seu criativo manda a pessoa |
| **Provas** | Antes/depois, alunas nomeadas (só estes nomes), prints | Suas provas reais — e só as reais |
| **Inimigos / falsos vilões** | Contar caloria, dieta, agachamento, procedimento, ficha genérica | O que a sua copy ataca (nunca a pessoa; sempre o que a orientou errado) |
| **Claims e limites** | O que a copy promete e os limites que ela respeita | O que você pode prometer sem passar do ponto |

**Duas regras de ouro deste arquivo, direto do João:**
- *"REGRA DE OURO: nenhum fato que não esteja na ficha. Nada de inventar número de alunas, prazos,
  preços ou credenciais."* Se um ângulo pede um fato que não existe, você escolhe outro caminho ou
  pergunta. É isto que mantém a copy honesta e aprovável.
- *"Atenção ao APÊNDICE: alguns números variam entre criativos antigos — escolha UMA versão canônica e
  nunca misture duas no mesmo criativo."* (No João, o nº de alunas e os minutos mudam de ad pra ad.)
  Marque os números instáveis pra o agente nunca frankensteinar dois.

Escreva tudo **verbatim** — as frases exatas que você usa pra descrever a dor, o mecanismo, a promessa.
O agente vai reusar essas frases; se você parafrasear "bonito", ele escreve genérico.

---

## PARTE 3 — Escreva o DNA de estilo (`dna-estilo.md`): a sua voz virada regra

Este é o coração da imitação. O `dna-estilo.md` do João tem **~440 linhas** e é uma dissecação
cirúrgica da fala dele, toda ancorada em exemplos verbatim com o arquivo de origem. Estrutura que você
vai reproduzir pra a sua voz:

1. **Voz e persona por speaker (§1).** O João tem dois modos: o expert (Murilo, que fala "de cima pra
   baixo com carinho": *"minha filha", "lindona", "meu amor"*) e a narradora (a amiga, que fala "de
   igual pra igual": *"gente", "amiga", "meninas", "gatas"*). Liste os SEUS speakers e os vocativos
   exatos de cada um, com exemplos do corpus.
2. **Léxico característico (§2).** Uma TABELA dos termos da sua operação, com frequência e exemplo
   verbatim. No João: *bumbum na nuca* (20×), *empinado* (68×), *murcho* (37×), *Sequência Ativadora*
   (69×), *pra caramba* (18×), *troquei de CPF* (6×)... + diminutivos ("15 minutinhos", "8
   semaninhas"), aumentativos ("BUNDÃO"), referências culturais BR (Virginia, Gracyanne, Copa). O que
   são as SUAS palavras-assinatura? Conte no corpus.
3. **Ritmo e sintaxe (§3).** Regras replicáveis numeradas. As do João: uma ideia por frase; reticências
   como respiração; CAPS em UMA palavra por frase; pergunta retórica + resposta seca; diálogo simulado
   com a leitora ("Tá Murilo, então qual é a solução?"); repetição em rajada ("Errado! Errado!
   Errado!"); escadas de 3 degraus ("é uma merda / é bom / é perfeito"). Extraia as SUAS.
4. **Naturalidade falada (§4).** As contrações e "erros" propositais que fazem soar como fala real:
   *"tá", "pra", "tô", "né", "cê"*, mistura tu/você, concordância de fala ("a maioria delas fazem").
5. **Digestibilidade (§5).** Como você simplifica: analogia doméstica ANTES do conceito ("Você não toma
   café pra acordar? Então..."), termo técnico sempre traduzido, números de bolso ("4 exercícios", "1
   em cada 2"), prova mostrada e não argumentada.
6. **Fronteiras — o que você NÃO faz (§6).** Aqui entra o contraste com os outros copywriters. É onde
   a sua voz fica única: o João NÃO usa "Além disso", NÃO dá deadline de relógio, NÃO usa "kkkk",
   NÃO escreve aforismo lapidado demais (isso é o estilo do Fiss, não dele).
7. **Anti-padrões de IA (§7) — O ARQUIVO MAIS IMPORTANTE DA SKILL INTEIRA.** Aqui você lista tudo que
   uma IA faz por padrão e que **denuncia a máquina na hora**. Metade da skill é receita; a outra
   metade é esta lista de proibições. As do João valem pra quase qualquer nicho — copie e adapte:
   - Conectivos de redação: "Além disso", "No entanto", "Vale ressaltar", "Em primeiro lugar".
   - Períodos subordinados longos (a IA encadeia; você quebra em 3 frases curtas).
   - Tratamento neutro sem vocativo (a IA é educada; você é íntimo).
   - Português correto demais (zero "né", concordância perfeita).
   - CTA de e-commerce: "Garanta já", "Não perca essa oportunidade".
   - Urgência com relógio e justificativa ("apenas hoje", "pra ser justo").
   - Vocabulário de wellness: "jornada", "empoderada", "melhor versão de si".
   - Emoji decorativo (✨🚀🔥).
   - A pior de todas → **"Não é X. É Y."** ("Não é genética. É bumbum desligado.") e conectores
     scriptados ("E isso tem nome:"). Isto liga o alarme de ChatGPT instantaneamente. Sintetize numa
     frase corrida.
   - Travessão (— / –) na copy = cara de IA. Use reticências ou vírgula.

> **Por que este arquivo ganha a skill:** o modelo já sabe escrever o genérico persuasivo. Seu
> trabalho não é ensinar copy — é **bloquear os reflexos de IA** que destruiriam a sua voz. Sem o
> checklist negativo, o genérico volta na primeira frase.

**Detalhe de ouro que o João faz (copie o hábito):** a seção 9 do `dna-estilo.md` se chama
*"CALIBRAÇÕES DIRETAS DO JOÃO (feedback sobre outputs — PESO MÁXIMO)"*. Cada regra ali existe porque um
criativo gerado errou nela e o João corrigiu. É **feedback do dono virado regra permanente**. Toda vez
que a sua skill entregar algo errado e você corrigir, não conserte só aquela entrega — **escreva a
regra aqui**, com o caso que a originou. É isso que, com o tempo, torna a sua skill impossível de
copiar: ela vira o destilado de todas as suas correções.

---

## PARTE 4 — Escreva a arquitetura de blocos (`blocos.md`): a sua estrutura persuasiva

Se o `dna-estilo.md` é COMO você fala, o `blocos.md` é O QUE você diz, e em que ordem. O do João abre
com **"o sistema em uma frase"** — a espinha que nunca muda:

> HOOK que segmenta pela dor → BODY que descarta os falsos vilões → revela o mecanismo do problema →
> nomeia o mecanismo da solução → prova com antes/depois → CTA pra aula grátis com escassez suave.

**Escreva a sua espinha em uma frase.** Qual é a sequência psicológica fixa dos SEUS criativos? Essa
frase é o contrato: todo body vai percorrer esses blocos, nessa ordem.

Depois, o `blocos.md` do João tem duas grandes seções que você vai reproduzir:

**1. Taxonomia de hooks.** O João catalogou **20 tipos de hook** do corpus, cada um com nome,
mecânica psicológica e exemplos verbatim. Alguns:
- *H1 Pergunta-armadilha com "ERRADO!"* — afirma a crença óbvia, pausa, demole ("Agachamento é o
  melhor exercício pra glúteo, certo? ERRADO!").
- *H5 Gate If/Then* — "Se você quer X, não pula. Se quer continuar Y, pula né." (o mais reciclado).
- *H7 Caixinha de pergunta* — o print da dúvida do Instagram É o hook.
- *H8 Antes/depois testemunhal* — "Essa era eu até o ano passado...".
- *H13 Escada "é uma merda / é bom / é perfeito"*, *H15 Personificação* ("Eu sou a sua bunda"), *H20
  Humor/meme*... e por aí.

**Faça a sua taxonomia:** leia o seu corpus, agrupe os hooks por MECÂNICA (não por tema), dê um nome e
um código a cada tipo, e cole 3–5 exemplos verbatim de cada. Isso vira o baralho que o agente embaralha
pra montar as 5 variações de um grupo sem repetir a mesma mecânica cinco vezes.

**2. Anatomia do body.** O João mapeou **5 esqueletos de body** (Expert Didático, Depoimento,
Antes/Depois, Ping-pong de objeções, Timeline), cada um com uma tabela *bloco → função psicológica →
tamanho típico → frase-modelo verbatim*. Faça o mesmo: quais são os 3–5 formatos de corpo que você
repete? Destrinche cada um bloco a bloco.

E documente **como as 5 variações de um grupo se relacionam** — no João há 3 padrões (mesma mecânica
trocando a variável; ângulos diferentes pro mesmo body; empilhamento de gancho sobre body validado).

---

## PARTE 5 — O estado que evolui (`fatias-performance.md` + `hooks-log.md`)

Uma skill de produção não é só estática — ela **lembra**. Dois arquivos pequenos, alto impacto:

- **`fatias-performance.md`** — o ranking dos públicos que dão dinheiro nos últimos 30 dias, mais
  "como refazer a análise quando os dados envelhecerem". Quando o usuário pede "faz o criativo pra
  fatia que dá mais dinheiro", o agente decide por DADO, não por achismo. Você vai atualizar isto
  periodicamente. Faça o seu com os seus números.
- **`hooks-log.md`** — o log das últimas entregas: que tipos de hook e fatias já saíram. A regra
  (`blocos.md` §8.9): *tipos e fatias das últimas 3 entregas ficam proibidos no grupo novo* — pra a
  operação não inundar de anúncios parecidos. Depois de entregar, o agente registra a entrega aqui.
  É um **anti-repetição com memória**, que um prompt sozinho nunca teria.

---

## PARTE 6 — Escreva o `SKILL.md`: o cérebro que orquestra tudo

Agora que as referências existem, escreva o `SKILL.md`. Ele tem 3 partes.

### 6.1 O frontmatter — o classificador de disparo (a coisa mais importante)

```yaml
---
name: criativos-bumbumflix
description: >-
  Escreve e adapta criativos de Meta Ads para a oferta BumbumFlix... USE sempre que o usuário pedir
  pra "adaptar esse criativo", "transformar isso num criativo meu", "escrever criativo pro Murilo",
  "criar variações de hook", "roubar esse ângulo", "modelar esse vídeo"... — mesmo sem citar o nome
  da skill.
---
```

O `description` **não descreve — ele decide se a skill dispara.** É o único texto que o agente lê pra
escolher, entre dezenas de skills, se é ESTA. Faça as três coisas que o João faz:
1. **O que faz e pra quem** (a sua oferta, o seu nicho, o seu estilo).
2. **Os inputs que aceita** (criativo de concorrente, vídeo, link, transcrição, ideia solta, do zero) —
   pra o agente reconhecer a skill mesmo quando o pedido não é óbvio.
3. **Frases-gatilho literais entre aspas** + a cláusula mágica **"mesmo sem citar o nome da skill"** —
   pra pegar quem descreve a tarefa em vez de nomear a ferramenta.

> **Teste do disparo:** escreva 10 formas diferentes de pedir a tarefa (algumas oblíquas, tipo "rouba
> esse ângulo aqui"). A descrição precisa disparar nas 10 sem disparar em tarefas vizinhas. Ajuste os
> gatilhos até acertar. É o tuning mais barato e mais ignorado.

### 6.2 A tabela "quando ler cada referência"

Logo depois, uma tabela *arquivo | o que tem | quando ler*. É a divulgação progressiva explícita — ela
diz ao agente qual referência carregar em qual momento (ex.: *"`oferta.md` e `dna-estilo.md`: SEMPRE,
antes de escrever"*; *"`corpus`: 2–3 do mesmo formato, imediatamente antes de escrever"*). Copie o
formato tal e qual.

### 6.3 O processo numerado (o algoritmo)

O corpo do `SKILL.md` do João é **Passo 0 → Passo 8**, cada passo com uma decisão e um artefato. É um
algoritmo que o agente executa. Os passos (adapte à sua operação):

- **Passo 0 — Classificar o input** e decidir o que preservar. Cinco tipos de entrada (concorrente,
  vídeo, transcrição, ideia, do zero) → cinco políticas de preservação. Toda skill de modelagem começa
  perguntando "o que estou recebendo e o que preciso manter disso?".
- **Passo 0.5 — Input é vídeo? ASSISTA antes de modelar (OBRIGATÓRIO).** Um gate: a skill se recusa a
  modelar "de ouvido". Ela chama outra skill (`assistir-criativo`) que vira o vídeo em timeline +
  frames. Marque os seus gates obrigatórios em CAIXA ALTA.
- **Passo 1 — Extrair a estrutura invisível do input** (mapear em blocos psicológicos). A skill avisa:
  *"essa espinha é CONTRATO, não inspiração"* — o body vai percorrer exatamente esses blocos. E marca
  o erro nº1 (mapear a espinha e depois escrever genérico "sobre o mesmo tema"), com o feedback real
  que o originou.
- **Passo 2 — Escolher narrador e formato** ANTES de escrever, porque a voz muda tudo. Mais: escolher
  a **fatia de público** por dado (`fatias-performance.md`), não por achismo.
- **Passo 3 — Transpor os blocos pra sua oferta** (com `oferta.md` aberto). Uma tabela *bloco do input
  → vira o equivalente da casa*. Aqui mora a REGRA DE OURO: nenhum fato fora da ficha.
- **Passo 4 — Escrever o BODY primeiro** (é compartilhado pelas 5 variações de hook, então vem antes).
  Ordem deliberada de design, não acaso.
- **Passo 5 — Escrever as 5 variações de hook**, cada uma de um tipo diferente da taxonomia, com a
  regra anti-repetição consultando o `hooks-log.md`.
- **Passo 6 — Passe de revisão OBRIGATÓRIO** com checklist explícito: naturalidade, digestibilidade,
  anti-IA, fatos, coerência hook→body, visual. O modelo SEMPRE pula a auto-revisão se você não a
  transformar num passo com checklist.
- **Passo 7 — Instruções de gravação/edição** (delegadas à skill `better-instructions`, neste repo).
- **Passo 8 — Subir o ad pro Google Doc** (só quando o dono pede), com dry-run antes de escrever.

No fim, o **formato de saída canônico**, escrito literal com placeholders. Nunca deixe o formato
implícito — o modelo diverge.

---

## PARTE 7 — Determinismo: o que um script faz, o modelo não improvisa

Este é o salto que separa uma skill séria de um prompt bonito. **Sempre que a saída precisa ser
idêntica, canônica ou validável, gere/valide por CÓDIGO — não pelo julgamento do modelo.** É por isso
que as instruções de gravação/edição da `criativos-bumbumflix` são feitas por uma skill separada, a
`better-instructions` (que está inteira neste repositório como estudo de caso). Estude o padrão dela:

- **Fonte única da verdade em dados** (`scripts/templates.json`): o texto canônico de cada tipo de
  instrução mora ali. A regra: *"Nunca escreva o texto canônico à mão — sempre `render.py`."* Assim,
  200 anúncios saem com a MESMA formatação, e mudar o padrão é editar 1 arquivo.
- **Renderizar por código, validar por código**: `render.py` emite; `qa_plan.py` valida ANTES de
  escrever (erro = para); `qa_doc.py` dá selo ✅/❌ no fim. O modelo propõe; o script dispõe.
- **Dry-run + rollback pra ações externas**: escrever num Google Doc tem `--dry-run` por padrão e só
  grava de verdade depois do "ok"; se falhar no meio, faz rollback sozinho.

> **Heurística de fronteira:** *"o modelo deve improvisar isto, ou um script resolveria melhor?"* Voz e
> persuasão → modelo. Numeração sequencial, formatação, checagem de completude, links/imagens → script.
> A `criativos-bumbumflix` escreve a copy (modelo) e delega o resto pra scripts.

Você não precisa começar com scripts. Comece só com `SKILL.md` + `references/`. Quando perceber que o
agente erra sempre na MESMA coisa mecânica (formatação, numeração, um checklist que ele esquece), aí
promova aquilo pra um script. É assim que a `better-instructions` nasceu — de um pedaço da
`criativos-bumbumflix` que precisava ser determinístico.

---

## PARTE 8 — Fallbacks: a entrega nunca trava

Skill de produção degrada com elegância. A `criativos-bumbumflix`:
- Se o pipeline de vídeo falhar → *só então* pede a transcrição ao usuário (nunca inventa o conteúdo).
- Se não houver template pro conceito → escreve a melhor instrução livre "no shape da casa" e segue —
  *"a entrega do criativo nunca trava por causa de instrução."*
- Se a escrita no doc falhar no meio → rollback automático.

Pra cada dependência (script, outra skill, API), escreva o que acontece quando ela falha.

---

## Passo a passo resumido (a sua sequência de construção)

1. **Nomeie as 3 coisas** que fazem um criativo parecer SEU e não de IA. (a tese da skill)
2. **Junte o corpus:** 20–60 criativos seus + alguns de contraste. Indexe. (Parte 1)
3. **Escreva `oferta.md`:** a ficha factual, verbatim, com "fora daqui = alucinação". (Parte 2)
4. **Escreva `dna-estilo.md`:** voz, léxico, ritmo — e o **checklist negativo anti-IA**. (Parte 3)
5. **Escreva `blocos.md`:** a espinha em 1 frase + taxonomia de hooks + esqueletos de body. (Parte 4)
6. **Escreva `fatias-performance.md` + `hooks-log.md`:** o estado que evolui. (Parte 5)
7. **Escreva `SKILL.md`:** frontmatter-classificador + tabela de referências + processo numerado com
   gates e passo de revisão + formato de saída canônico. (Parte 6)
8. **Rode, colete correções, vire cada correção em REGRA** no `dna-estilo.md` §9. Repita. (Parte 3)
9. **Quando algo mecânico errar sempre, promova pra script** (fonte única + render + validação). (P.7)
10. **Adicione fallbacks.** (Parte 8)

Uma skill boa é a 5ª versão, não a 1ª. A `criativos-bumbumflix` chegou onde chegou porque cada
criativo que o João revisou virou uma regra nova.

---

## Checklist de qualidade — a sua skill está "pronta como a do João"?

- [ ] Você nomeou as 3 coisas que definem a sua voz, e a skill tem um arquivo protegendo cada uma.
- [ ] O `description` dispara em pedidos oblíquos e não vaza pra tarefas vizinhas (teste dos 10).
- [ ] `oferta.md` é a fonte de verdade fechada, com a regra "fora daqui não entra" escrita.
- [ ] `dna-estilo.md` tem um **checklist negativo** explícito do que denuncia a IA.
- [ ] `blocos.md` tem a espinha em 1 frase, a taxonomia de hooks e os esqueletos de body.
- [ ] O `SKILL.md` é um **processo numerado** com gates OBRIGATÓRIOS e um passo de revisão dedicado.
- [ ] Há uma **tabela "quando ler cada referência"**.
- [ ] O corpus está lá, indexado, com a instrução "leia 2–3 do mesmo formato antes de escrever".
- [ ] Existe um **log anti-repetição** e uma fonte de dados de performance.
- [ ] Correções do dono viram **regras rastreáveis** (não conserto pontual).
- [ ] O formato de saída está escrito literal, com placeholders.
- [ ] Um agente lendo a sua skill escreve um criativo que VOCÊ assinaria sem retocar.

---

## O erro que mata a skill (não cometa)

O `SKILL.md` do João avisa: *"O erro nº 1 desta skill é mapear a espinha e depois escrever um criativo
genérico da casa 'sobre o mesmo tema'."* Traduzindo pra você: a tentação é montar toda essa estrutura e,
na hora H, deixar a IA escrever "copy persuasiva genérica" com as suas palavras salpicadas por cima.
Não é isso. A skill inteira existe pra forçar o agente a percorrer a SUA espinha, na SUA voz, com os
SEUS fatos — e a bloquear os reflexos de IA a cada frase. Se a sua skill não faz isso, ela é um prompt
com tema; se faz, ela é uma máquina que escreve como você.

---

### Fecho

Você agora tem o mapa exato de como a `criativos-bumbumflix` foi construída: um corpus destilado em
regras de voz e estrutura, uma ficha factual que impede alucinação, um cérebro que orquestra em passos
com gates, o determinismo empurrado pra scripts, e cada correção do dono virando regra. Reproduza essa
arquitetura com o SEU material e você terá a sua própria máquina de criativos — uma que não escreve
"anúncios em geral", e sim os **seus**. A `better-instructions` neste repositório é a prova em código de
que dá pra fazer. Agora é a sua vez.
