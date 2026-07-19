# skill-instrucoes-e-como-criar-propria-skill-de-modelagem

Dois entregáveis num repositório só:

1. **[`COMO-CRIAR-UMA-SKILL.md`](COMO-CRIAR-UMA-SKILL.md)** — um guia detalhado, para um copywriter
   (humano **ou** IA), de **como criar a sua própria skill de criativos** — com a SUA oferta, o SEU
   expert e a SUA voz. Transfere só a **psicologia e o método**: a arquitetura da skill
   (`oferta.md` como ficha factual anti-alucinação, `dna-estilo.md` como voz virada regra + checklist
   negativo anti-IA, `blocos.md` como taxonomia de hooks + esqueletos de body, o corpus como
   calibrador, o `SKILL.md` como cérebro-orquestrador, o determinismo empurrado pra scripts) e o passo
   a passo pra você (ou o seu Claude) **destilar a SUA voz do SEU material**. Ele **não carrega a voz,
   o léxico nem os criativos de ninguém** — a cara da skill sai dos criativos de quem a constrói. No
   fim, um agente lendo a sua skill escreve criativos indistinguíveis dos que **você** escreve à mão.
   Leia primeiro.

2. **[`better-instructions/`](better-instructions/)** — a skill que **faz as instruções de gravação e
   edição** dos criativos (a engine que a `criativos-bumbumflix` chama no seu Passo 7). Está aqui
   inteira, como estudo de caso vivo do guia acima: você lê o princípio e vê o código que o implementa.

## O que é a `better-instructions`

Transforma instruções soltas de gravação/edição de anúncios num texto **canônico** (mesma estrutura
por conceito) e escreve de volta num Google Doc, preservando o formato da casa. O coração dela:

- `scripts/templates.json` — **fonte única da verdade**: texto canônico, gatilhos, slots e obrigatórios.
- `scripts/render.py` — emite o texto canônico (nunca se escreve à mão).
- `scripts/qa_plan.py` / `scripts/qa_doc.py` — validam antes e depois de escrever.
- `references/glossario-gravacao.md` / `glossario-edicao.md` — guia humano por conceito.
- `references/formato-da-casa.md` / `como-melhorar.md` — layout e o passo a passo do raciocínio.

Comece por [`better-instructions/SKILL.md`](better-instructions/SKILL.md).

## Segurança

Este repositório **não** contém segredos. As credenciais OAuth do Google (`scripts/token.json`,
`scripts/credentials.json`) ficam no `.gitignore` e são lidas apenas de fora do controle de versão —
veja [`better-instructions/scripts/SETUP.md`](better-instructions/scripts/SETUP.md) para configurá-las
localmente. Nenhum dado de aluna ou credencial viva foi versionado.

## Rodar a engine localmente

```bash
cd better-instructions
python3 scripts/render.py --list                 # ver templates, gatilhos e slots
python3 scripts/render.py <template> --slots k=v  # emitir texto canônico
python3 -m pytest tests/                           # rodar os testes de lógica (sem Google Docs)
```
