# Como criar uma skill de modelagem tão boa quanto a "Criativos BumbumFlix"

> Guia para um terceiro — humano **ou** IA — reconstruir, do zero, uma skill do mesmo calibre da
> `criativos-bumbumflix`. Não é teoria genérica: cada princípio aqui foi extraído por engenharia
> reversa de uma skill real que está em produção, escrevendo anúncios de Meta Ads indistinguíveis
> dos que um copywriter humano escreve à mão. A engine de instruções dela (a skill
> `better-instructions`) está neste mesmo repositório como estudo de caso vivo — leia o código junto.

---

## 0. O que é uma "skill" (modelo mental)

Uma **skill** (Agent Skill) é uma pasta que ensina um agente de IA a executar UMA tarefa
especializada com qualidade de especialista, de forma repetível. No mínimo ela tem um arquivo
`SKILL.md`; no máximo ela vira um pequeno software com scripts, dados de referência e testes.

```
minha-skill/
├── SKILL.md              ← obrigatório: frontmatter (name + description) + o "cérebro"
├── references/           ← conhecimento lido sob demanda (o "livro de consulta")
├── scripts/              ← determinismo: o que um script faz melhor que o modelo
├── examples/             ← calibradores (exemplos reais + banco de imagens)
└── tests/                ← fixtures que travam o comportamento contra regressão
```

O erro de quem começa é achar que a skill é "um prompt grande". Não é. Uma skill de verdade é uma
**arquitetura de decisão**: ela decide o que o modelo deve carregar na cabeça, quando, e o que ele
NÃO deve tentar fazer de cabeça (delega pra um script). A diferença entre uma skill medíocre e a
`criativos-bumbumflix` está inteira nessas decisões — não no assunto.

**A tese central desta skill (copie a mentalidade):**
> "O valor não está no TEMA — está na VOZ, na DIGESTIBILIDADE e na SEQUÊNCIA DE BLOCOS. Imitar só o
> assunto e errar essas três coisas produz um resultado genérico de IA."

Troque "voz/digestibilidade/blocos" pelas 3 coisas que definem qualidade no *seu* domínio. Toda a
skill existe pra proteger essas 3 coisas. Descubra quais são as suas antes de escrever qualquer linha.

---

## 1. Comece pela pergunta de modelagem, não pelo prompt

Antes de escrever, responda em uma frase: **"O que faz o resultado bom parecer feito por um humano
especialista, e não por uma IA?"**

Na `criativos-bumbumflix` a resposta foi decomposta em três eixos mensuráveis:
1. **Voz** — pt-BR falado de verdade (contrações, diminutivos, gramática de fala proposital).
2. **Digestibilidade** — uma ideia por frase, leitura de 5ª série, tudo "visível no espelho".
3. **Blocos psicológicos** — a sequência persuasiva (hook → quebra de crença → mecanismo → prova → CTA).

Repare que os três são **anti-genérico**. É por isso que a skill dedica um arquivo inteiro
(`dna-estilo.md`) só a listar o que a IA faz por padrão e que precisa ser *proibido*: "Além disso",
"No entanto", tríades perfeitinhas, a estrutura "Não é X. É Y.". **Uma boa skill de modelagem é
metade receita, metade lista de proibições.** O modelo já sabe fazer o genérico; seu trabalho é
bloquear o genérico.

> **Regra de ouro extraída da skill:** para cada padrão que você QUER, escreva também o anti-padrão
> correspondente que denuncia a máquina. A `dna-estilo.md` §7 e §9 são puro "checklist negativo".

---

## 2. Anatomia do `SKILL.md`

### 2.1 O frontmatter é a coisa mais importante do arquivo

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

O `description` **não é uma descrição — é um classificador de disparo.** É o único texto que o agente
lê pra decidir, entre dezenas de skills, se ESTA é a certa pra o pedido atual. Por isso a descrição da
`criativos-bumbumflix` faz três coisas que você deve copiar:

1. **Diz o que faz e pra quem** (oferta, nicho, estilo) — desambiguação.
2. **Enumera os inputs que aceita** (concorrente, vídeo, link, transcrição, ideia solta, do zero) —
   assim o agente reconhece a skill mesmo quando o pedido não parece óbvio.
3. **Lista frases-gatilho literais entre aspas** + a cláusula mágica **"mesmo sem citar o nome da
   skill"**. Isso captura o usuário que descreve a tarefa em vez de nomear a ferramenta.

> **Teste do disparo:** escreva 10 formas diferentes de um usuário pedir a tarefa (algumas oblíquas,
> tipo "rouba esse ângulo aqui"). A descrição precisa disparar em todas as 10 sem disparar em tarefas
> vizinhas. Se disparar demais, adicione fronteiras; se de menos, adicione gatilhos. Este é o loop de
> tuning mais barato e mais ignorado.

### 2.2 O corpo do `SKILL.md` é um processo, não um ensaio

Abra a `criativos-bumbumflix/SKILL.md`: o corpo é **Passo 0 → Passo 8**, numerado, cada passo com uma
decisão e um artefato de saída. Não é "dicas"; é um **algoritmo executável por um agente**. Padrões a
copiar:

- **Passo 0 = classificar o input.** Toda skill de modelagem começa perguntando "o que estou recebendo
  e o que preciso preservar disso?". Cinco tipos de input → cinco políticas de preservação diferentes.
- **Passos com pré-condição obrigatória.** O Passo 0.5 ("input é vídeo? ASSISTA antes de modelar") é um
  gate: a skill se recusa a modelar de ouvido. Marque explicitamente o que é **OBRIGATÓRIO** vs opcional.
- **Ordem contra-intuitiva quando ela importa.** A skill manda escrever o BODY (Passo 4) ANTES dos hooks
  (Passo 5), porque o corpo é compartilhado pelas 5 variações. A ordem é uma decisão de design, não acaso.
- **Um passo de revisão dedicado** (Passo 6) com checklist explícito: naturalidade, digestibilidade,
  anti-IA, fatos, coerência. O modelo *sempre* pula auto-revisão se você não a transformar num passo.
- **Formato de saída canônico** no fim, literal, com placeholders. Não deixe o formato "implícito".

### 2.3 Tabela de "quando ler cada referência"

A `criativos-bumbumflix` abre com uma tabela: *arquivo | o que tem | quando ler*. Isso é
**divulgação progressiva** (progressive disclosure) explícita: o `SKILL.md` fica enxuto e diz ao
agente qual arquivo carregar em qual momento, em vez de despejar tudo. Sem essa tabela, ou o modelo
lê tudo (estoura contexto) ou não lê nada (alucina). Copie o formato tal e qual.

---

## 3. Divulgação progressiva: o `SKILL.md` decide, as `references/` sabem

O `SKILL.md` é o **roteiro**; as `references/` são a **enciclopédia**. Regra prática observada:

| Se o conteúdo é… | Vai para… | Por quê |
|---|---|---|
| Decisão/processo/ordem/gate | `SKILL.md` | É o que o agente sempre precisa |
| Conhecimento consultável, denso, estável | `references/*.md` | Só carrega quando o passo exige |
| Fonte da verdade factual (não pode alucinar) | `references/*.md` marcado "SEMPRE, antes de escrever" | Fato que não está aqui não entra no output |
| Texto/estrutura que precisa ser idêntico toda vez | `scripts/` (renderizado por código) | Modelo não deve digitar de cabeça |

Veja como a `criativos-bumbumflix` fatiou o conhecimento:
- `oferta.md` — **a ficha factual** (o expert, provas, números, inimigos). A regra é dura: *"fato que
  não está aqui não entra na copy"*. É o antídoto contra alucinação — a skill inteira gira em torno de
  ter uma fonte de verdade fechada.
- `dna-estilo.md` — voz, léxico, ritmo, e o checklist negativo anti-IA.
- `blocos.md` — a taxonomia (20 tipos de hook catalogados, 5 esqueletos de corpo, estruturas por formato).
- `corpus/` + `corpus-index.txt` — **58 exemplos reais, verbatim**, indexados por formato. A instrução:
  *"leia 2–3 do MESMO formato imediatamente antes de escrever — é o calibrador de voz mais forte que
  existe"*. Exemplos reais batem qualquer descrição de estilo.
- `fatias-performance.md` + `hooks-log.md` — **estado que evolui**: ranking por dinheiro dos últimos 30
  dias, e um log das últimas entregas pra evitar repetição. Skill não é só estática; ela lembra.

> **Princípio:** conhecimento que você citaria "de vez em quando" não vai no `SKILL.md`. Ele vira uma
> referência com uma linha na tabela dizendo QUANDO abri-la. O `SKILL.md` deve caber confortável na
> cabeça do agente numa leitura.

---

## 4. Determinismo: o que um script faz, o modelo não improvisa

Este é o salto de qualidade que separa a `criativos-bumbumflix` de um prompt bonitinho. Sempre que a
saída precisa ser **idêntica, canônica ou validável**, ela é gerada/checada por **código**, não pelo
julgamento do modelo. A engine disso é a skill `better-instructions` (neste repo). Estude o padrão:

- **Fonte única da verdade em dados, não em prosa.** `scripts/templates.json` guarda o texto canônico
  de cada tipo de instrução, seus gatilhos, slots e obrigatórios. A regra: *"Nunca escreva o texto
  canônico à mão — sempre `render.py`"*. Assim, 200 anúncios saem com a MESMA formatação, e mudar o
  padrão é editar 1 arquivo, não reeducar o modelo.
- **Renderizar por código, validar por código.** `render.py` emite o texto; `qa_plan.py` valida o
  plano ANTES de escrever (erro = exit 1); `qa_doc.py` dá um selo ✅/❌ por item no fim. O modelo propõe;
  o script dispõe.
- **Dry-run antes de qualquer escrita destrutiva/externa.** Toda ação que toca um recurso de fora
  (Google Doc) tem `--dry-run` como default e só escreve de verdade após "ok" explícito. Rollback
  automático se falhar no meio.
- **Hierarquia antiburro.** A `better-instructions` abre com 7 "regras não negociáveis" numeradas por
  prioridade ("não perder nada do copy" > "não inventar quando há template" > ...). Quando o modelo
  tiver que escolher, ele segue a hierarquia, não o gosto do momento.

> **Heurística de fronteira:** *"O modelo deve improvisar isto, ou um script resolveria melhor?"* Voz e
> persuasão → modelo. Numeração sequencial, formatação, validação de completude, links/imagens → script.
> A `criativos-bumbumflix` escreve a copy (modelo) e delega gravação/edição + upload pra scripts.

---

## 5. Separação de responsabilidades entre skills

A `criativos-bumbumflix` **não** faz as instruções de gravação/edição ela mesma. No Passo 7 ela
**delega** pra `better-instructions` (a "única fonte da verdade" desse pedaço) e no Passo 8 usa o
`upload_ad.py` dela pra subir no doc. Duas skills, uma cadeia:

```
criativos-bumbumflix  → escreve a COPY (voz, blocos, hooks)  [julgamento do modelo]
        └─ chama →  better-instructions → renderiza INSTRUÇÕES canônicas + sobe no doc  [determinismo]
        └─ chama →  assistir-criativo → transforma VÍDEO em timeline+frames antes de modelar
```

Lições:
- **Uma skill, uma responsabilidade.** Se um pedaço da tarefa tem regras próprias e reaproveitáveis,
  ele vira skill separada e é *chamada*, não copiada. (A `criativos-bumbumflix` aponta pros arquivos da
  `better-instructions` em vez de duplicar o conteúdo: *"aponte pra elas, não copie o conteúdo pra cá —
  são a fonte"*.)
- **Pré-processadores viram skills também.** Modelar um vídeo exige *ver* o vídeo; então existe uma
  skill (`assistir-criativo`) que vira o vídeo em timeline + frames, e a `criativos-bumbumflix` a
  invoca como etapa obrigatória. Não peça ao usuário o que outra skill consegue produzir.

---

## 6. Feedback do dono, codificado como regra

O que faz a skill "soar como o João" e não como uma IA genérica é que **os erros que o João já
corrigiu estão escritos como regras**, com rastreabilidade. Exemplos reais do `SKILL.md`:

- *"O erro nº 1 desta skill é mapear a espinha e depois escrever um criativo genérico da casa 'sobre o
  mesmo tema' — feedback real do João, corrigido no calibre Ad98 (`blocos.md` §8.8)."*
- *"Dois erros simétricos a evitar (feedbacks reais): abandonar o ângulo nos .2–.5 e repetir o stunt
  nos 5."*
- Um **log anti-repetição** (`hooks-log.md`): tipos de hook e frases que o dono já rejeitou ficam
  proibidos nas próximas 3 entregas; depois de entregar, registra-se a entrega no log.

> **Padrão:** toda vez que o dono disser "não era isso, era assim", não conserte só aquela entrega —
> **escreva a regra** no `SKILL.md` ou numa referência, com o caso que a originou. A skill vira um
> destilado de correções. É isso que a torna difícil de replicar por fora: é experiência acumulada.

---

## 7. Fallbacks: a entrega nunca trava

Skill de produção precisa degradar com elegância. A `criativos-bumbumflix` cobriga:
- Se o pipeline de vídeo falhar → *só então* peça a transcrição ao usuário (nunca invente o conteúdo).
- Se `render.py` não tiver template pro conceito → escreva a melhor instrução livre "no shape da casa"
  e siga — *"a entrega do criativo nunca trava por causa de instrução"*.
- Se a escrita no doc falhar no meio → rollback automático do bloco parcial.

> **Regra:** para cada dependência externa (script, API, outra skill), escreva o que acontece quando
> ela falha. Uma skill que trava no primeiro erro não sobrevive ao uso real.

---

## 8. Passo a passo para construir a SUA skill

1. **Nomeie a tarefa e as 3 coisas que definem qualidade nela.** (§1) Se não conseguir nomear as 3,
   você ainda não entende o domínio o suficiente pra automatizá-lo.
2. **Junte o corpus.** Colete 20–60 exemplos reais e excelentes do resultado que você quer. Sem corpus,
   não há calibração — só opinião. Indexe-os por tipo/formato.
3. **Dissecar o corpus em taxonomia.** Extraia os padrões repetíveis (na skill: 20 tipos de hook, 5
   esqueletos de corpo). Nomeie cada um. Isso vira sua `blocos.md`.
4. **Escreva a ficha factual** (`oferta.md`): tudo que o modelo pode afirmar, verbatim, com a regra
   "fora daqui é alucinação". Marque números que variam pra ele nunca misturar duas versões.
5. **Escreva o DNA de estilo** (`dna-estilo.md`): voz, léxico, ritmo — e o **checklist negativo**
   anti-IA. Metade receita, metade proibição. (§1)
6. **Desenhe o processo** no `SKILL.md`: Passo 0 (classificar input) → ... → passo de revisão → formato
   de saída canônico. Marque gates OBRIGATÓRIOS. (§2.2)
7. **Escreva a `description`** como classificador de disparo: o que faz + inputs aceitos + frases-gatilho
   literais + "mesmo sem citar o nome da skill". Teste com 10 pedidos. (§2.1)
8. **Mova pra scripts tudo que precisa ser idêntico/validável.** Fonte única em `templates.json`,
   `render.py` pra emitir, `qa_*.py` pra validar, `--dry-run` pra ações externas. (§4)
9. **Adicione fallbacks e o log de feedback.** (§6, §7)
10. **Escreva testes/fixtures** que travem os casos difíceis (na `better-instructions`: fixtures de ad
    com b-roll faltando, plano inválido, etc.) pra pegar regressão quando você editar a skill.
11. **Rode, colete correções do dono, vire cada correção em regra.** Itere. Uma skill boa é a 5ª versão.

---

## 9. Checklist de qualidade (a skill está "pronta"?)

- [ ] O `description` dispara em pedidos oblíquos e não vaza pra tarefas vizinhas.
- [ ] Existe uma **fonte de verdade factual** e a regra "fora daqui não entra" está escrita.
- [ ] Existe um **checklist negativo** (o que denuncia a IA) explícito.
- [ ] O corpo do `SKILL.md` é um **processo numerado** com gates obrigatórios e um passo de revisão.
- [ ] Há uma **tabela de "quando ler cada referência"** (divulgação progressiva).
- [ ] Tudo que precisa ser idêntico/validável é **gerado/checado por script**, não de cabeça.
- [ ] Ações externas têm **dry-run + confirmação + rollback**.
- [ ] Há **fallbacks** pra cada dependência; a entrega nunca trava.
- [ ] O **formato de saída** está escrito literal, com placeholders.
- [ ] Correções do dono viram **regras rastreáveis**, não conserto pontual.
- [ ] Um terceiro (humano ou IA) consegue seguir o `SKILL.md` e chegar perto do resultado do dono.

---

## 10. Estudo de caso anotado — a `criativos-bumbumflix` mapeada nestes princípios

| Princípio deste guia | Onde aparece na skill real |
|---|---|
| §1 As 3 coisas que definem qualidade | Abertura do `SKILL.md`: voz / digestibilidade / blocos |
| §1 Checklist negativo anti-IA | `dna-estilo.md` §7 e §9 · Passo 6.3 do `SKILL.md` |
| §2.1 `description` como classificador | Frontmatter com ~15 frases-gatilho + "mesmo sem citar o nome" |
| §2.2 Processo numerado com gates | Passos 0→8; Passo 0.5 "ASSISTA antes de modelar (obrigatório)" |
| §2.2 Ordem de design deliberada | Passo 4 (BODY) antes do Passo 5 (hooks) |
| §2.3 Tabela "quando ler cada referência" | Seção "Referências" do `SKILL.md` |
| §3 Fonte de verdade factual | `oferta.md` — "fato que não está aqui não entra na copy" |
| §3 Corpus como calibrador | `corpus/` (58 ads) + `corpus-index.txt` |
| §3 Estado que evolui | `fatias-performance.md` (30 dias) + `hooks-log.md` |
| §4 Determinismo por script | `better-instructions`: `templates.json` + `render.py` + `qa_*.py` |
| §4 Dry-run + rollback | Passo 8 upload / `write_instructions.py --dry-run` |
| §5 Uma skill, uma responsabilidade | Delega gravação/edição → `better-instructions`; vídeo → `assistir-criativo` |
| §6 Feedback codificado | "erro nº 1... feedback real do João, Ad98"; `hooks-log.md` |
| §7 Fallbacks | Passo 0.5 fallback; Passo 7 "a entrega nunca trava" |

---

## 11. Armadilhas comuns (o que NÃO fazer)

- **Despejar tudo no `SKILL.md`.** Estoura contexto e o agente ignora. Use `references/` + a tabela.
- **Descrever estilo em vez de mostrar exemplos.** Um corpus verbatim calibra mais que mil adjetivos.
- **Deixar o formato de saída implícito.** Ele deriva; escreva-o literal.
- **Pedir ao modelo o que um script faz melhor** (numeração, formatação, validação de completude).
- **Esquecer o checklist negativo.** Sem ele, o genérico da IA volta na primeira frase.
- **Não versionar / não testar.** Sem fixtures, cada edição pode quebrar um caso que você já resolveu.
- **Tratar correção como conserto pontual** em vez de virar regra. A skill para de melhorar.
- **Vazar segredos.** Nunca versione credenciais/tokens. A `better-instructions` mantém
  `credentials.json` e `token.json` no `.gitignore` e o código só os lê de fora do repositório.

---

### Fecho

Uma skill excelente não é um prompt inteligente — é uma **arquitetura que protege as poucas coisas
que definem qualidade no domínio**, empurra o determinismo pra scripts, guarda a verdade factual num
lugar fechado, e transforma cada correção do dono numa regra. Faça isso e um terceiro — pessoa ou IA —
consegue reproduzir o resultado do especialista. Foi exatamente assim que a `criativos-bumbumflix`
foi construída, e é isso que a `better-instructions` neste repositório demonstra em código.
