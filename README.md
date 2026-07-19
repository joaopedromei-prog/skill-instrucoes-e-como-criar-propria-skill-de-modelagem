# skill-instrucoes-e-como-criar-propria-skill-de-modelagem

Dois entregáveis num repositório só:

1. **[`COMO-CRIAR-UMA-SKILL.md`](COMO-CRIAR-UMA-SKILL.md)** — um guia detalhado, para um terceiro
   (humano **ou** IA), de como criar uma skill de modelagem tão boa quanto a `criativos-bumbumflix`.
   É engenharia reversa dos princípios de design de uma skill real em produção: divulgação progressiva,
   `description` como classificador de disparo, fonte única da verdade, determinismo por script,
   checklist negativo anti-IA, feedback do dono codificado como regra, fallbacks. Leia isto primeiro.

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
