# Formato da casa (como o João estrutura cada ad no doc)

Extraído do `CRIATIVOS BUMBUM FB.pdf` (ad 6 em diante). **Preserve este layout** ao reescrever — a skill só melhora o conteúdo das instruções, não muda a estrutura.

## Estrutura de um ad

1. **Título do ad** em destaque: `AD6`, `AD7`, etc.
2. **Código do criativo** (nome do hook, geralmente grifado em amarelo), formato:
   `BUMFB | Ad6.1 - G25 | F CXP | SP1 | Edt Matheus`
   = Marca | Ad.Hook - IDdoHook | Formato | **SPx (quem grava)** | Editor.

   > **Código SPx = quem grava CADA HOOK:** **SP1 = Murilo**; **SP≠1 (SP0, SP19, SP22…) = externo / UGC / voz feminina**. Os nomes dos hooks ficam **grifados em amarelo** no doc.
   > **Mas o sinal definitivo de gravação é a seção "Instruções para o Murilo"** (regra única — ver `como-melhorar.md` / SKILL §7): se for **"Nenhuma"**, Murilo não grava nada; se houver qualquer instrução, ele grava ao menos o body e exige cenário + microfone + takes pra parte dele. **O SP não anula o body** — em caso misto (hooks SP≠1 mas seção do Murilo com instruções), o checklist vale só pra parte do Murilo.

   > **Código F XXX = formato do criativo** (use pra preencher o `formato` obrigatório da edição):
   > - `F CNM` → Cinematográfico + narração feminina
   > - `F REACT` → React
   > - `F CXP` → Caixinha de pergunta
   > - `F UGC` → UGC
   > - `F TP` → Teleprompter — UGC do próprio Murilo gravando, **lendo a copy no teleprompter**, mas o vídeo tem que ficar orgânico e dinâmico (cara de TikTok, natural — nada de leitura robótica). **Murilo grava** → exige cenário + microfone + takes na seção dele.
   > - `F LEG` → foco em legenda ("leia a legenda")
   > - `F TD` → Tela dividida · `F EST` → Estático
   > Código desconhecido → inferir o formato pelas instruções.
3. **Tabela de 2 colunas:**
   - Coluna esquerda: **ROTEIRO** (a copy/fala).
   - Coluna direita: **INSTRUÇÕES DE GRAVAÇÃO** (texto costuma estar em vermelho).
4. **Dois blocos**, abaixo ou ao lado:
   - **Instruções para o editor de vídeo**.
   - **Instruções para o Murilo** (quando não há, escreve "Nenhuma").
   > O **input** do copy às vezes vem numerado — tudo bem. Mas a **saída reescrita é sempre em blocos limpos, SEM numeração** (ver "Formato de SAÍDA" abaixo).
5. **Referências** no topo: vídeo (📹 `video - xxxx.mp4`), links de TikTok/Instagram/Drive (clicáveis, em azul).
6. **Caixinha de pergunta** (quando o formato é CXP): caixa branca com o texto da pergunta dentro do ROTEIRO.

## Onde cada melhoria entra

| Conceito do João | Onde aparece no doc | Bloco |
|---|---|---|
| Legenda, Headline invídeo, Música, Ritmo, Cortes/transições, Formato | "Instruções para o editor de vídeo" | EDIÇÃO |
| Cenário, Figurino, Ângulos, Tom, Enquadramento, Lip sync, Microfone | "Instruções para o Murilo" / coluna INSTRUÇÕES DE GRAVAÇÃO | GRAVAÇÃO |
| Caixinha de perguntas | dentro do ROTEIRO + nota pro editor | EDIÇÃO |

## Convenção de emojis (fixa — um por conceito, pra escanear o doc)

| Emoji | Conceito | Emoji | Conceito |
|---|---|---|---|
| 🎬 | Formato | 📍 | Cenário |
| 📝 | Legenda | 🎤 | Áudio/microfone |
| 🔤 | Headline invídeo | 🎥 | Takes/câmera |
| ⚡ | Ritmo / atropelado | 👕 | Figurino |
| ✂️ | Cortes secos | 🖼️ | Enquadramento |
| 🎞️ | Edição dopaminérgica | 🎭 | Tom |
| 🎵 | Música | 🗣️ | Lip sync / narração |
| 💬 | Caixinha de pergunta | 🎯 | Ancoragem / direção do hook |
| ⚠️ | Ressalva (b-roll, confirmar) | 🔗 | Referência (link + o que olhar) |

Direção criativa solta que não tem template usa o emoji do conceito mais próximo desta tabela (ex.: ancoragem → 🎯). **Não invente emoji novo** — consistência deixa o doc escaneável.

## Formato de SAÍDA (decisão única — vale acima de qualquer outra menção)

A seção reescrita ("Instruções para o editor de vídeo" / "Instruções para o Murilo") sai em **blocos limpos, SEM numeração nem bullets**:
- **Cabeçalho preservado** ("Instruções para o editor de vídeo:" / "...Murilo:").
- **Uma linha em branco logo após o cabeçalho** (o `replace_with` começa com `\n`).
- **Uma instrução por bloco**, começando com o **emoji fixo** do conceito (tabela acima).
- **Uma linha em branco entre instruções**.
- **Referência/imagem dentro ou logo abaixo da instrução** correspondente: link na palavra (`[rótulo](url)`) e marcador `[[img:tag]]` no fim daquela instrução.
- O `write_instructions.py` remove bullets por padrão — não numere.

## Estilo de escrita a manter

- Imperativo direto, **liderando pelo resultado**: "O criativo não pode ter tempo morto: cortes…", "Áudio limpo: microfone…".
- **Um bloco por instrução, sem numeração.**
- Jargão da casa que NÃO deve ser traduzido nem apagado: **corte seco**, **lip sync**, **criativo atropelado**, **headline invídeo**, **caixinha de pergunta**, **react**, **UGC**.
- Quando há referência, manter o link e dizer **o que olhar** nela ("repare na velocidade e nos cortes").

## Bloco-modelo de SAÍDA (referência)

```
Instruções para o editor de vídeo:

🎬 Formato React + UGC feminino — tela com o vídeo reagido + expert reagindo, reação ancorada na cena. Spokesperson nova.
🔗 Ref.: [vídeo 1](url) — repare em como a reação ancora na cena reagida

📝 Legenda minimalista — limpa, sem competir com a imagem: fonte TikTok Sans / Instagram Sans, branca com borda fina preta, sem caixa/fundo.
[[img:legenda-min-branca]]

⚡ Ritmo de TikTok viral — o criativo não pode ter 1 segundo morto: cortes rápidos, sem silêncios, aceleração leve.
🔗 Ref.: [vídeo 1](url) — repare na velocidade e nos cortes secos emendando as falas

Instruções para o Murilo:

👕 Figurino pra passar físico forte + autoridade: regata preta, justa, valorizando shape e ombros/braços.
[[img:figurino-regata-preta]]

🎭 Tom conversa natural (leveza + autoridade) — falar como quem conta algo pra um amigo, olhar na câmera.
```
(Os textos vêm do `render.py`; aqui é só pra ver o **shape** da saída — blocos, emoji, linha em branco, ref/imagem na instrução.)
