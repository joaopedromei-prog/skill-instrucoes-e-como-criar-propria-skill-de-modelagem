# Como criar a sua própria skill de criativos (a psicologia e o método)

> **Para quem é este guia:** um copywriter — humano ou IA — que quer ter uma skill de criativos como a
> `criativos-bumbumflix`, mas **100% com a própria cara**: a sua oferta, o seu expert, a sua voz.
>
> **O que este guia NÃO faz:** ele não te entrega a voz de ninguém pra copiar. Não tem aqui o léxico, o
> ritmo, as gírias, os fatos de oferta ou os criativos de outra pessoa pra você imitar. Isso seria
> transformar você num replicador de outro copywriter — o oposto do objetivo. **A voz da sua skill sai
> dos SEUS criativos.**
>
> **O que este guia FAZ:** transfere a **psicologia** e o **método** — a arquitetura de uma skill que
> reproduz um copywriter específico, e o passo a passo pra você (ou o seu Claude, lendo este
> repositório) extrair a SUA voz do SEU material e montar a SUA skill. No fim, um agente de IA lendo a
> sua skill escreve criativos indistinguíveis dos que **você** escreve à mão — porque a skill aprendeu
> a **sua** letra, não a de outro.

Sempre que aparecer `[entre colchetes]` abaixo, é um espaço que **você preenche com o seu material**.

---

## A ideia que faz uma skill dessas funcionar (leia antes de tudo)

Uma skill de criativos de alto nível não é "um prompt que escreve anúncio". É uma **máquina que
reproduz um copywriter específico**. E ela só funciona por causa de uma tese, que precisa estar escrita
logo no começo da skill:

> "O valor de um criativo não está no TEMA — está em **[as 2 a 4 coisas que fazem um criativo SEU
> parecer seu]**. Imitar só o assunto e errar essas coisas produz um anúncio genérico de IA."

Numa skill de referência, essas coisas foram **voz** (o jeito falado próprio), **digestibilidade** (uma
ideia por frase, leitura fácil) e **sequência de blocos psicológicos**. As suas podem ser essas ou
outras — humor seco, prova social agressiva, storytelling em 1ª pessoa, autoridade técnica, o que for.

**Seu primeiro trabalho, antes de escrever qualquer arquivo:** responda —
> "O que faz um criativo MEU parecer escrito por MIM, e não por uma IA (nem por outro copywriter)?"

Escreva as suas 2 a 4 respostas. Elas viram a tese da sua skill, e cada uma vai ganhar um arquivo que a
protege. Sem isso definido, você constrói uma máquina de anúncio genérico com um tema diferente — que é
exatamente o que uma boa skill foi feita pra NÃO ser.

---

## O mapa da skill: as peças e o trabalho de cada uma

Uma skill de criativos madura tem esta forma (a `criativos-bumbumflix`, neste caso de referência, segue
exatamente ela):

```
[nome-da-sua-skill]/
├── SKILL.md                  ← o cérebro: quando disparar + o processo passo a passo
└── references/               ← o conhecimento, lido sob demanda
    ├── oferta.md             ← a FICHA FACTUAL: tudo que pode ser afirmado (fora daqui = alucinação)
    ├── dna-estilo.md         ← a VOZ: léxico, ritmo, regras de fala + checklist negativo anti-IA
    ├── blocos.md             ← a ESTRUTURA: taxonomia de hooks + esqueletos de body
    ├── corpus/*.md           ← os SEUS criativos reais, verbatim (o calibrador de voz)
    ├── corpus-index.txt      ← índice do corpus por formato/speaker
    ├── performance.md        ← o que dá resultado hoje (ranking de público/ângulo)
    └── entregas-log.md       ← log das últimas entregas (anti-repetição)
```

**A regra de ouro da arquitetura: o `SKILL.md` decide, as `references/` sabem.** O `SKILL.md` fica
enxuto e diz ao agente QUANDO abrir cada referência — em vez de despejar tudo de uma vez (o que estoura
a memória do agente) ou não dar contexto nenhum (o que faz ele inventar). Isso se chama **divulgação
progressiva** e é o que separa uma skill de um prompt gigante.

As próximas seções constroem cada peça — na ordem em que **você** deve construí-las (que não é a ordem
em que o agente as lê).

---

## PARTE 1 — Junte o SEU corpus (comece sempre por aqui)

Tudo depois é análise do seu corpus. Sem ele, o `dna-estilo.md` e o `blocos.md` viram opinião; com ele,
viram fato observado. **A voz da sua skill nasce daqui — dos seus criativos, não dos de ninguém.**

**O que fazer:**
1. Junte **20 a 60 criativos SEUS** que você considera excelentes e representativos. Quanto mais,
   melhor a calibração. Salve cada um como um arquivo `.md` **verbatim** — o texto exato, sem
   "melhorar", sem editar. É o material bruto do qual toda a sua voz será destilada.
2. Junte **alguns criativos de colegas ou concorrentes que soam DIFERENTE de você.** Eles são o
   material de **contraste**: é olhando o que você NÃO faz que a sua voz fica nítida. (Uma boa
   `dna-estilo.md` tem uma seção inteira de "o que eu NÃO faço, ao contrário de fulano".)
3. Nomeie os arquivos com um padrão que já carregue metadados — por exemplo, codificando no nome do
   arquivo: oferta, número, **formato** e **quem grava/fala**. Isso alimenta o índice.
4. Escreva o `corpus-index.txt`: uma linha por criativo, agrupado por formato. A instrução que ele
   habilita no `SKILL.md` é o **calibrador de voz mais forte que existe**: *"leia 2–3 criativos do
   MESMO formato que você vai escrever, imediatamente antes de escrever"*. Um exemplo real seu vale
   mais que mil adjetivos descrevendo o seu estilo.

> **Por que isto primeiro:** você não consegue escrever as regras da sua voz sem ter o material pra
> observar. As Partes 2 a 4 são, literalmente, você (ou o seu Claude) lendo o seu corpus e anotando
> os padrões que se repetem.

---

## PARTE 2 — A ficha factual (`oferta.md`): o arquivo que impede a IA de mentir

A regra deste arquivo, que precisa estar escrita nele: **"É a fonte de verdade — fato que não está
aqui não entra na copy."** Ele existe pra que o agente nunca invente número, prazo, preço, credencial
ou prova que você não pode sustentar.

Estrutura pra reproduzir (o conteúdo é 100% seu):

| Seção | O que você escreve nela |
|---|---|
| **O expert / a marca** | Quem é, e o que ele legitimamente pode afirmar (credenciais reais, fama real) |
| **A persona (avatar)** | O seu público: as dores nas palavras DELE, as rotinas, os desejos, e as objeções → com a resposta que você dá pra cada uma |
| **Mecanismo do PROBLEMA** | O "vilão invisível" da sua oferta (por que a pessoa falha), com as frases exatas que você usa |
| **Mecanismo da SOLUÇÃO** | O seu método, com o nome próprio que você deu a ele e os componentes fixos |
| **Produto / funil** | Pra onde o criativo manda a pessoa (aula, VSL, página), preço, garantia |
| **Provas** | Antes/depois, casos e nomes reais — **e só os reais** |
| **Inimigos / falsos vilões** | O que a sua copy ataca. Regra psicológica: nunca ataque a pessoa; ataque o que a orientou errado (a culpa vai pra fora, não pra ela) |
| **Claims e limites** | O que você pode prometer sem passar do ponto (compliance) |

**Duas regras de ouro:**
- **Nenhum fato fora da ficha.** Se um ângulo pede um dado que não existe aqui, o agente escolhe outro
  caminho ou pergunta a você. É isto que mantém a copy honesta e aprovável.
- **Marque os números instáveis.** Se um dado varia entre criativos antigos (nº de casos, minutos,
  prazos), o agente deve escolher UMA versão canônica e nunca misturar duas no mesmo criativo.

Escreva tudo **verbatim** — as frases exatas que você usa pra nomear a dor, o mecanismo, a promessa. O
agente vai reusar essas frases; se você parafrasear "bonito", ele escreve genérico.

---

## PARTE 3 — O DNA de estilo (`dna-estilo.md`): a SUA voz virada regra

Este é o coração da imitação — e o ponto onde fica claríssimo que a skill tem que ser **sua**: aqui vai
a **sua** voz, destilada do **seu** corpus, e de mais ninguém. É o arquivo mais longo e o mais
importante. Estrutura pra reproduzir, com o que VOCÊ extrai do seu material em cada seção:

1. **Voz e persona por speaker.** Quem fala nos seus criativos? (o expert? uma narradora? um cliente
   em depoimento?) Pra cada speaker, liste os vocativos e o tom exatos — extraídos do corpus. Anote a
   **direção da intimidade** de cada um (fala "de cima pra baixo" como professor? "de igual pra igual"
   como amigo?). `[seus speakers, seus vocativos verbatim]`
2. **Léxico característico.** Monte uma TABELA dos seus termos-assinatura, com **frequência** (conte no
   corpus) e um **exemplo verbatim** de cada. Inclua as suas gírias, os diminutivos/aumentativos que
   você usa, as referências culturais que você ancora. É a impressão digital do seu vocabulário.
   `[seus termos, contados no seu corpus]`
3. **Ritmo e sintaxe.** Regras replicáveis, numeradas, cada uma com exemplo. Extraia AS SUAS: qual o
   tamanho médio de frase? Você usa reticências? CAPS pra ênfase? pergunta retórica + resposta? diálogo
   simulado com a leitora? repetição em rajada? escadas/gradações? `[seus padrões de ritmo]`
4. **Naturalidade falada.** As contrações e "erros" propositais que fazem soar como fala de verdade no
   seu registro (regional, coloquial, formal — o que for o seu). `[seu registro]`
5. **Digestibilidade.** Como VOCÊ simplifica: usa analogia antes do conceito? traduz termo técnico?
   números de bolso? prova mostrada em vez de argumentada? `[seus recursos de clareza]`
6. **Fronteiras — o que você NÃO faz.** Aqui a sua voz fica única, por contraste com os criativos de
   contraste que você juntou na Parte 1: liste o que outro copywriter faz e você não (uma construção,
   um tipo de fecho, uma gíria, um recurso). `[o que te distingue]`
7. **Anti-padrões de IA — provavelmente a seção mais valiosa da skill inteira.** Aqui você lista tudo
   que uma IA faz por padrão e que **denuncia a máquina na hora**. Metade da skill é receita; a outra
   metade é esta lista de proibições. Esta parte é **psicologia universal de "como soar humano"** — vale
   pra qualquer voz, então pode usar esta lista de partida e ajustar ao seu caso:
   - Conectivos de redação: "Além disso", "No entanto", "Vale ressaltar", "Por outro lado", "Em
     primeiro lugar", "Dessa forma".
   - Períodos subordinados longos e encadeados (a IA empilha oração; fala real quebra em frases curtas).
   - Tratamento neutro, sem vocativo (a IA é educada e distante; voz real é íntima).
   - Português correto demais (zero marca de oralidade, concordância impecável) quando o seu registro é
     falado.
   - CTA de e-commerce: "Garanta já", "Não perca essa oportunidade", "Acesse agora", "Transforme sua
     vida".
   - Urgência com relógio e justificativa ("apenas hoje", "só até meia-noite", "pra ser justo").
   - Vocabulário de wellness/coach genérico: "jornada", "empoderada", "melhor versão de si mesma".
   - Emoji decorativo (✨🚀🔥 espalhados sem função).
   - **A pior de todas → a antítese "Não é X. É Y."** (ex.: "Não é [causa comum]. É [seu mecanismo].")
     e os conectores scriptados tipo "E isso tem nome:". Isso liga o alarme de ChatGPT
     instantaneamente. Sintetize a mesma ideia numa frase corrida.
   - Travessão (— / –) no meio da copy: cara de texto de IA. Use reticências, vírgula ou quebra de
     frase.
   - Simetria excessiva: tríades perfeitinhas, paralelismos redondos demais pra serem falados.

> **Por que esta seção ganha a skill:** o modelo já sabe escrever o genérico persuasivo. Seu trabalho
> não é ensinar copy — é **bloquear os reflexos de IA** que destruiriam a sua voz. Sem o checklist
> negativo, o genérico volta na primeira frase.

**O hábito mais importante deste arquivo — "calibrações do dono".** Reserve uma seção final,
declarada como **PESO MÁXIMO (sobrepõe qualquer regra acima em caso de conflito)**, pras correções que
VOCÊ faz nos criativos que a skill gerar. Cada regra dessa seção existe porque um output real errou nela
e você corrigiu. Toda vez que a skill entregar algo torto e você ajustar, **não conserte só aquela
entrega — escreva a regra aqui**, com o caso que a originou. É isto que, com o tempo, torna a sua skill
impossível de copiar: ela vira o destilado de todas as suas correções pessoais. (Uma skill boa é a 5ª
versão, não a 1ª.)

---

## PARTE 4 — A arquitetura de blocos (`blocos.md`): a sua estrutura persuasiva

Se o `dna-estilo.md` é COMO você fala, o `blocos.md` é O QUE você diz, e em que ordem. Aqui a matéria
é **psicologia de persuasão** — que é transferível — aplicada aos SEUS criativos.

**Comece pela espinha em uma frase.** Qual é a sequência psicológica fixa dos seus criativos? A maioria
dos criativos de resposta direta segue alguma variação de:

> HOOK que segmenta pela dor/desejo → descarte dos falsos caminhos que a pessoa já tentou → revelação
> do mecanismo do PROBLEMA (por que ela falha, culpa externalizada) → nome do mecanismo da SOLUÇÃO →
> prova → CTA com urgência.

Escreva a SUA versão dessa espinha. Ela é o **contrato**: todo body vai percorrer esses blocos, nessa
ordem. (Modelar um criativo de referência = manter a espinha dele e trocar a voz/oferta/provas pelas
suas — a espinha sobrevive, as palavras morrem todas.)

Depois, duas grandes seções:

**1. Taxonomia de hooks.** Leia o seu corpus e agrupe os seus hooks **por MECÂNICA psicológica** (não
por tema). Dê um nome e um código a cada tipo, e cole 3–5 exemplos SEUS verbatim de cada. As mecânicas
de hook mais comuns em resposta direta (use como lista de partida pra classificar os seus) são:
   - **Pattern-interrupt / contraintuitivo** — afirma o oposto do senso comum pra quebrar o scroll.
   - **Pergunta-armadilha** — enuncia a crença "óbvia" e demole ("...certo? ERRADO.").
   - **Gate If/Then** — bifurca a audiência ("se você quer X, fica; se aceita Y, pula").
   - **Auto-diagnóstico segmentador** — pergunta binária sobre o corpo/vida da pessoa; ela se
     responde e "entra".
   - **Curiosidade / fofoca / segredo** — tom de "vou te contar uma coisa".
   - **Antes/depois testemunhal** — "essa era eu até...".
   - **Ceticismo → teste** — a pessoa assume a objeção nº1 (desconfiança) e vira enredo ("testei pra
     ver se era golpe").
   - **Prova social / autoridade emprestada** — número, celebridade, "analisei os 100 mais virais".
   - **Personificação / pattern absurdo** — objeto ou parte do corpo fala em 1ª pessoa.
   - **Objeção preventiva** — já responde no hook o que a pessoa ia rebater.
   - **Humor / meme / oportunismo cultural** — referência de cultura pop ou data.
   - **Promessa direta com prazo + remoção de sacrifício.**

   Essa é a psicologia; os **exemplos e a redação são 100% seus**, tirados do seu corpus. O resultado é
   um baralho que o agente embaralha pra montar 5 variações de hook de um grupo **sem repetir a mesma
   mecânica cinco vezes**.

**2. Anatomia do body.** Identifique os seus 3–5 formatos de corpo recorrentes (ex.: "expert
explicando", "depoimento de cliente", "antes/depois", "ping-pong de objeções", "linha do tempo /
future pacing"). Para cada um, monte uma tabela *bloco → função psicológica → tamanho típico →
frase-modelo (sua, verbatim)*. É esse mapa que faz o agente escrever um corpo com o seu ritmo, e não um
texto genérico.

E documente **como as 5 variações de um grupo se relacionam** — em geral há 3 padrões: (a) mesma
mecânica trocando só a variável (dor/persona/prazo); (b) ângulos diferentes atacando o mesmo body; (c)
empilhamento de ganchos novos sobre um body já validado.

---

## PARTE 5 — O estado que evolui (`performance.md` + `entregas-log.md`)

Uma skill de produção não é só estática — ela **lembra**. Dois arquivos pequenos, de alto impacto:

- **`performance.md`** — o ranking dos públicos/ângulos que dão resultado hoje, + "como refazer a
  análise quando os dados envelhecerem". Quando você pede "faz o criativo pro público que dá mais
  resultado", o agente decide por DADO, não por achismo. Você atualiza isto periodicamente com os
  SEUS números.
- **`entregas-log.md`** — o log das últimas entregas (que tipos de hook e públicos já saíram). A regra:
  *os tipos e ângulos das últimas 2–3 entregas ficam proibidos no grupo novo* — pra a operação não
  inundar de anúncios parecidos. Depois de entregar, o agente registra a entrega aqui. É um
  **anti-repetição com memória** que um prompt sozinho nunca teria.

---

## PARTE 6 — O `SKILL.md`: o cérebro que orquestra tudo

Com as referências prontas, escreva o `SKILL.md`. Três partes.

### 6.1 O frontmatter — o classificador de disparo (a coisa mais importante do arquivo)

```yaml
---
name: [nome-da-sua-skill]
description: >-
  [O que faz e pra quem: sua oferta, seu nicho, seu estilo.] [Os inputs que aceita: criativo de
  concorrente, vídeo, link, transcrição, ideia solta, do zero.] USE sempre que o usuário pedir
  "[frase-gatilho 1]", "[frase-gatilho 2]", "[frase-gatilho 3]"... — mesmo sem citar o nome da skill.
---
```

O `description` **não descreve — ele decide se a skill dispara.** É o único texto que o agente lê pra
escolher, entre dezenas de skills, se é ESTA. Ele precisa fazer três coisas:
1. **O que faz e pra quem** (desambiguação).
2. **Os inputs que aceita** — pra o agente reconhecer a skill mesmo quando o pedido não é óbvio.
3. **Frases-gatilho literais entre aspas** + a cláusula **"mesmo sem citar o nome da skill"** — pra
   pegar quem descreve a tarefa em vez de nomear a ferramenta.

> **Teste do disparo:** escreva 10 formas diferentes de pedir a tarefa (algumas oblíquas). A descrição
> precisa disparar nas 10 sem disparar em tarefas vizinhas. Ajuste os gatilhos até acertar. É o tuning
> mais barato e mais ignorado.

### 6.2 A tabela "quando ler cada referência"

Logo depois, uma tabela *arquivo | o que tem | quando ler*. É a divulgação progressiva explícita — diz
ao agente qual referência carregar em qual momento (ex.: *"`oferta.md` e `dna-estilo.md`: SEMPRE, antes
de escrever"*; *"`corpus`: 2–3 do mesmo formato, imediatamente antes de escrever"*).

### 6.3 O processo numerado (o algoritmo que o agente executa)

O corpo do `SKILL.md` é uma sequência de passos, cada um com uma decisão e um artefato. Um esqueleto
que funciona bem (adapte à sua operação):

- **Passo 0 — Classificar o input** e decidir o que preservar. Cada tipo de entrada (concorrente,
  vídeo, transcrição, ideia, do zero) tem uma política de preservação diferente. Toda skill de
  modelagem começa perguntando "o que estou recebendo e o que preciso manter disso?".
- **Passo 0.5 — Gates obrigatórios.** Se um tipo de input exige um pré-processamento (ex.: vídeo →
  **ASSISTIR antes de modelar**, chamando outra skill que vira o vídeo em timeline + frames), marque
  isso em CAIXA ALTA como OBRIGATÓRIO. A skill deve se recusar a trabalhar "de ouvido".
- **Passo 1 — Extrair a estrutura invisível do input** (mapear em blocos psicológicos). Deixe escrito
  que **essa espinha é CONTRATO, não inspiração** — o body vai percorrer exatamente esses blocos. E
  registre o **erro nº1**: mapear a espinha e depois escrever um genérico "sobre o mesmo tema".
- **Passo 2 — Escolher narrador e formato ANTES de escrever** (a voz muda tudo) e escolher o público
  por DADO (`performance.md`), não por achismo.
- **Passo 3 — Transpor os blocos pra sua oferta** (com `oferta.md` aberto). Uma tabela *bloco do input
  → equivalente da sua casa*. Aqui vive a REGRA DE OURO: nenhum fato fora da ficha.
- **Passo 4 — Escrever o BODY primeiro** (ele é compartilhado pelas variações de hook, então vem
  antes). Ordem deliberada de design, não acaso.
- **Passo 5 — Escrever as variações de hook**, cada uma de um tipo diferente da taxonomia, com a regra
  anti-repetição consultando o `entregas-log.md`.
- **Passo 6 — Passe de revisão OBRIGATÓRIO** com checklist explícito: naturalidade, digestibilidade,
  anti-IA, fatos, coerência hook→body, viabilidade visual. O modelo SEMPRE pula a auto-revisão se você
  não a transformar num passo com checklist.
- **Passo 7+ — Instruções de gravação/edição e publicação** (ver Parte 7 sobre delegar isso a scripts).

No fim, o **formato de saída canônico**, escrito literal, com placeholders. Nunca deixe o formato
implícito — o modelo diverge.

---

## PARTE 7 — Determinismo: o que um script faz, o modelo não improvisa

Este é o salto que separa uma skill séria de um prompt bonito. **Sempre que a saída precisa ser
idêntica, canônica ou validável, gere/valide por CÓDIGO — não pelo julgamento do modelo.**

Neste repositório, a skill **`better-instructions`** é a demonstração viva desse princípio: é a engine
que padroniza as instruções de gravação/edição de um criativo. Estude o padrão dela (o código está
todo aqui):
- **Fonte única da verdade em dados** (um `templates.json`): o texto canônico de cada tipo de saída
  mora ali. A regra: *"nunca escreva o texto canônico à mão — sempre renderize por script"*. Assim,
  centenas de entregas saem com a MESMA formatação, e mudar o padrão é editar 1 arquivo.
- **Renderizar por código, validar por código**: um script emite; outro valida ANTES de escrever
  (erro = para); outro dá um selo ✅/❌ no fim. O modelo propõe; o script dispõe.
- **Dry-run + rollback pra ações externas**: escrever num Google Doc (ou qualquer recurso de fora) tem
  `--dry-run` por padrão e só grava de verdade depois do "ok"; se falhar no meio, faz rollback sozinho.

> **Heurística de fronteira:** *"o modelo deve improvisar isto, ou um script resolveria melhor?"* Voz e
> persuasão → modelo. Numeração sequencial, formatação, checagem de completude, links/imagens,
> publicação → script.

**Você não precisa começar com scripts.** Comece só com `SKILL.md` + `references/`. Quando perceber
que o agente erra sempre na MESMA coisa mecânica (formatação, numeração, um checklist que ele esquece),
aí promova aquilo pra um script. Foi assim que a `better-instructions` nasceu — de um pedaço da skill
de criativos que precisava ser determinístico e virou ferramenta própria.

---

## PARTE 8 — Fallbacks: a entrega nunca trava

Skill de produção degrada com elegância. Padrões:
- Se um pré-processamento falhar (ex.: download de vídeo bloqueado) → *só então* peça o material ao
  usuário; **nunca invente o que estava no vídeo**.
- Se não houver template/recurso pro caso → produza a melhor saída livre "no formato da casa" e siga;
  a entrega do criativo nunca trava por causa de um acessório.
- Se uma escrita externa falhar no meio → rollback automático.

Pra cada dependência (script, outra skill, API), escreva o que acontece quando ela falha.

---

## Passo a passo resumido (a sua sequência de construção)

1. **Nomeie as 2 a 4 coisas** que fazem um criativo parecer SEU e não de IA (nem de outro). É a tese.
2. **Junte o SEU corpus:** 20–60 criativos seus + alguns de contraste. Indexe. (Parte 1)
3. **Escreva `oferta.md`:** a ficha factual, verbatim, com "fora daqui = alucinação". (Parte 2)
4. **Escreva `dna-estilo.md`:** SUA voz destilada do SEU corpus + o **checklist negativo anti-IA** +
   a seção de calibrações do dono. (Parte 3)
5. **Escreva `blocos.md`:** a espinha em 1 frase + a SUA taxonomia de hooks + os SEUS esqueletos de
   body. (Parte 4)
6. **Escreva `performance.md` + `entregas-log.md`:** o estado que evolui. (Parte 5)
7. **Escreva `SKILL.md`:** frontmatter-classificador + tabela de referências + processo numerado com
   gates e passo de revisão + formato de saída canônico. (Parte 6)
8. **Rode, colete SUAS correções, vire cada uma em REGRA** no `dna-estilo.md`. Repita. (Parte 3)
9. **Quando algo mecânico errar sempre, promova pra script** (fonte única + render + validação).
   (Parte 7)
10. **Adicione fallbacks.** (Parte 8)

---

## Checklist de qualidade — a sua skill está pronta?

- [ ] Você nomeou as 2 a 4 coisas que definem a SUA voz, e a skill tem um arquivo protegendo cada uma.
- [ ] O `description` dispara em pedidos oblíquos e não vaza pra tarefas vizinhas (teste dos 10).
- [ ] `oferta.md` é a fonte de verdade fechada, com a regra "fora daqui não entra" escrita.
- [ ] `dna-estilo.md` foi destilado dos SEUS criativos e tem um **checklist negativo anti-IA** explícito.
- [ ] `blocos.md` tem a espinha em 1 frase, a SUA taxonomia de hooks e os SEUS esqueletos de body.
- [ ] O corpus são os SEUS criativos, indexados, com a instrução "leia 2–3 do mesmo formato antes de
      escrever".
- [ ] O `SKILL.md` é um **processo numerado** com gates OBRIGATÓRIOS e um passo de revisão dedicado.
- [ ] Há uma **tabela "quando ler cada referência"**, um **log anti-repetição** e uma fonte de dados
      de performance.
- [ ] Suas correções viram **regras rastreáveis** (não conserto pontual).
- [ ] O formato de saída está escrito literal, com placeholders.
- [ ] Um agente lendo a sua skill escreve um criativo que VOCÊ assinaria sem retocar — na SUA voz.

---

## O erro que mata a skill (não cometa)

A tentação é montar toda essa estrutura e, na hora H, deixar a IA escrever "copy persuasiva genérica"
com as suas palavras salpicadas por cima. Não é isso. A skill inteira existe pra forçar o agente a
percorrer a SUA espinha, na SUA voz, com os SEUS fatos — e a bloquear os reflexos de IA a cada frase.
Se a sua skill não faz isso, ela é um prompt com tema; se faz, ela é uma máquina que escreve como você.

---

### Fecho

Você tem aqui a psicologia e o método de uma skill que reproduz um copywriter — sem levar a voz de
ninguém junto. O caminho é sempre o mesmo: um corpus SEU destilado em regras de voz e estrutura, uma
ficha factual que impede alucinação, um cérebro que orquestra em passos com gates, o determinismo
empurrado pra scripts, e cada correção sua virando regra. A `better-instructions` neste repositório é a
prova em código de que a parte determinística funciona. O resto — a voz — é você que traz. Agora é a
sua vez.
