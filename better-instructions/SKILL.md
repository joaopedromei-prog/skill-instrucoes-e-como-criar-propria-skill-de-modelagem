---
name: better-instructions
description: Padroniza instruções de GRAVAÇÃO e EDIÇÃO de criativos BumbumFlix (Meta Ads) num Google Doc. Lê os ads, detecta conceitos nas instruções rascunhadas, renderiza templates canônicos via scripts/render.py, preserva as referências do copy e valida o resultado no formato da casa. Use quando o usuário apontar um Google Doc de criativos e pedir "melhora/padroniza/clareia as instruções", "passa o better no ad X", "better-instructions", ou colar instruções soltas de gravação/edição pedindo upgrade.
---

# Better Instructions

Transforma instruções soltas de gravação/edição em **instruções canônicas** (mesma estrutura por conceito) e escreve de volta no Google Doc, preservando o formato da casa e as referências do copy.

## 1. Quando usar
(Google Doc de criativos) + (instruções de gravação ou edição) + (pedido de melhorar / padronizar / clarear). Gatilhos: "melhora as instruções", "passa o better no ad X", "better-instructions", colar instruções soltas pedindo upgrade.

## 2. Regras NÃO negociáveis (hierarquia antiburro)
1. **Não perder nada do copy** — texto, números, falas e **referências** são sagrados.
2. **Não escrever sem preservar refs** — smart chips / imagens / links do copy (campo `copy_refs`) têm que aparecer na instrução.
3. **Não inventar quando há template** — frase nova só pra o que nenhum template cobre.
4. **Não assumir o que o copy não disse** — ex.: cenário sem indicação vira `⚠️ CONFIRMAR cenário`.
5. **Não deixar obrigatório faltando** — edição: ritmo/legenda/formato; gravação: cenário/microfone/takes.
6. **Não escrever no doc sem dry-run/preview.** Default = prévia + confirmação. Só escreve direto se o usuário disser explicitamente "escreve direto", "aplica direto", "pode escrever no doc" ou equivalente. **Sempre `--dry-run` antes da escrita real.**
7. **Não depender do bom senso do agente quando um script resolve** — renderize por código, valide por script.

## 3. Fontes da verdade
- **`scripts/templates.json` é a ÚNICA fonte da verdade**: texto canônico, triggers, slots, obrigatórios, exemplos/tags e refs do template. **Nunca escreva o texto canônico à mão — sempre `scripts/render.py`.**
- `examples/manifest.json` — banco de exemplos (tag → imagem / vídeo / `ref_label`).
- `references/glossario-*.md` — **guia humano** (conceito, quando usar/não usar, gatilhos, slots, exemplo). Documentação, não fonte de texto.
- `references/formato-da-casa.md` — layout do ad e formato de saída.
- `references/como-melhorar.md` — o passo a passo do reasoning. **Leia antes de agir.**

## 4. Workflow
0. **Pré-req:** `scripts/token.json` (OAuth). Sem ele, só leitura. Ver `scripts/SETUP.md`.
1. **Ler:** `scripts/.venv/bin/python scripts/parse_ads.py <fileId> --tab <tabId> [--ad "AD 38"]` → JSON por ad com `editor_instr`, `murilo_instr`, `murilo_grava`, `hooks` (SP/formato) e **`copy_refs`**. Trabalhe **ad a ad**. **Sempre olhe `copy_refs`.**
2. **Renderizar:** detecte conceitos pelos gatilhos → defina slots → `scripts/render.py <template> --slots k=v [--merge "específico do copy"] [--with-img]`. `--merge` costura o específico do copy **antes** da linha de ref. `--with-img` já devolve o texto com o marcador `[[img:tag]]`.
3. **Montar o bloco** da seção no formato da casa (blocos limpos, **sem numeração** — ver `formato-da-casa.md`).
4. **Prévia + confirmação:** mostre o diff por ad (original → canônico + exemplos). **Só escreva depois do "ok"**, salvo comando explícito de escrever direto.
5. **Validar o plano:** `scripts/qa_plan.py plano.json` (bloqueia se houver erro).
6. **Escrever:** `scripts/write_instructions.py <fileId> --tab <tabId> --plan plano.json --dry-run` primeiro; depois sem `--dry-run`.
7. **QA final:** `scripts/qa_doc.py <fileId>` → selo ✅/❌ por ad.

## 5. Política de escrita (formato de saída)
- **Substitui a seção inteira** (anchor = conteúdo atual da seção, do `parse_ads.py`; `replace_with` = bloco novo). Não empilha.
- **Blocos limpos, SEM numeração/bullets.** Uma instrução por bloco; emoji fixo no início (tabela em `formato-da-casa.md`); **uma linha em branco entre instruções**; **uma linha em branco após o cabeçalho** (o `replace_with` começa com `\n`).
- **Imagem via `[[img:tag]]`** dentro do `replace_with`, no fim da instrução correspondente — é o **mecanismo principal** (posiciona a imagem embaixo da instrução certa). O campo `images` do plano é só fallback. `render.py --with-img` já devolve o marcador.
- **Refs como link na palavra** (`[rótulo](url)`), nunca URL crua — o render já formata.
- **Nunca** deixe marcadores tipo `[obrigatório...]` no doc — isso vai só no relatório.

## 6. Definition of Done (checklist obrigatório)
- **Edição (todo ad):** ritmo (+ ref), legenda (ou "sem legenda" + motivo), formato. Ressalva `b-roll-realista` sempre que houver take de terceiro (React/CNM, UGC com cenas externas, "b-roll", "cenas de mulher").
- **Gravação:** ver regra do Murilo (§7).
- Confirme rodando `qa_doc.py` — todo item tem que dar ✅.

## 7. Regra única SP / Murilo
- **`Instruções para o Murilo: Nenhuma`** → Murilo não grava nada → **não** aplicar checklist de gravação.
- **Qualquer instrução nessa seção** → Murilo grava pelo menos parte → garantir **cenário + microfone/áudio + takes** pra parte dele.
- **SPx** (do nome do hook `BUMFB | AdX.Y - Gnn | F XXX | SPx | …`) diz quem grava cada hook: **SP1 = Murilo**; **SP≠1 = externo / UGC / voz feminina**. Em caso misto (hooks SP≠1 mas a seção do Murilo tem instruções), aplique o checklist só à parte do Murilo (o body). **A seção do Murilo manda; o SP não anula o body.**

## 8. Comandos essenciais
- `render.py --list [--section edicao|gravacao]` — templates + gatilhos + slots.
- `render.py <template> --slots k=v [--merge "..."] [--with-img]` — texto canônico.
- `parse_ads.py <fileId> --tab <tab>` — ads + `copy_refs`.
- `qa_plan.py plano.json` — valida o plano **antes** de escrever (erro = exit 1).
- `write_instructions.py <fileId> --tab <tab> --plan plano.json [--dry-run] [--strict-refs]`.
- `qa_doc.py <fileId> [--ad "AD 66"]` — selo Definition of Done por ad.
- `cleanup_doc.py <fileId> --tab <tab>` — conserta cruft de re-execução (imagem duplicada, numeração órfã).

## 9. Gotchas críticos
- `fileId` ≠ `tabId` (o `tab=t.xxxx` da URL é o `tabId`).
- **Âncora exata** (aspas curvas, acentos, espaços, typos). Pegue do `parse_ads.py`, não digite de cabeça.
- Imagem só entra se a URL for pública (anyone-with-link) e png/jpg.
- **Rode cada ad uma vez.** Re-rodar compõe cruft → passe `cleanup_doc.py` depois.
- Não toque em `token.json` / `credentials.json` (segredos, fora do git).
