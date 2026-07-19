# Setup (uma vez só)

Para a skill **escrever** no Google Doc e **subir imagens**, ela precisa de acesso OAuth ao Google Docs + Drive. Isto é manual e feito uma vez.

## 1. Instalar as libs (já feito — venv dedicado)

As libs ficam num venv em `scripts/.venv` (o Python do macOS é gerenciado/PEP 668, então não dá pra instalar global). Já está criado. Se precisar recriar:

```bash
cd ~/.claude/skills/better-instructions/scripts
python3 -m venv .venv
./.venv/bin/pip install google-api-python-client google-auth google-auth-oauthlib
```

> **Importante:** todos os comandos abaixo usam `./.venv/bin/python` (não `python3`).

## 2. Criar o OAuth Client no Google Cloud Console

1. Acesse https://console.cloud.google.com → crie/escolha um projeto.
2. Menu **APIs e serviços → Biblioteca**: ative **Google Docs API** e **Google Drive API**.
3. **APIs e serviços → Tela de consentimento OAuth**: tipo *Externo*, preencha o básico, adicione seu e‑mail (`thescalers01@gmail.com`) em **Usuários de teste**.
4. **APIs e serviços → Credenciais → Criar credenciais → ID do cliente OAuth → Tipo: App para computador (Desktop)**.
5. Baixe o JSON e salve como:
   `~/.claude/skills/better-instructions/scripts/credentials.json`

## 3. Gerar o token

```bash
cd ~/.claude/skills/better-instructions/scripts
./.venv/bin/python setup_auth.py
```

Abre o navegador; faça login com a conta que tem acesso ao Google Doc dos criativos. Isso cria `scripts/token.json`. Pronto.

> `credentials.json` e `token.json` são segredos — não compartilhar/commitar.

## 4. Popular o banco de exemplos

1. Coloque as imagens em `~/.claude/skills/better-instructions/examples/img/`, nomeando-as conforme o campo `arquivo` do `examples/manifest.json` (ex. `legenda-min-branca.png`). Pode renomear depois — só mantenha o casamento com o manifest.
2. Suba pro Drive e gere as URLs públicas:

```bash
cd ~/.claude/skills/better-instructions/scripts
./.venv/bin/python upload_examples.py
```

Isso cria a pasta `better-instructions-examples` no seu Drive, deixa as imagens públicas e grava a `drive_url` de cada uma no manifest.

## 5. Teste seguro

Antes de rodar no doc real, teste numa **cópia** (a skill faz isso via MCP `copy_file`, ou você duplica o doc na mão). Depois:

```bash
# ver os tabs do doc
./.venv/bin/python read_doc.py <fileId>
# ver o conteúdo de um tab
./.venv/bin/python read_doc.py <fileId> --tab <tabId>
# aplicar (dry-run primeiro!)
./.venv/bin/python write_instructions.py <fileId> --plan plano.json --tab <tabId> --dry-run
./.venv/bin/python write_instructions.py <fileId> --plan plano.json --tab <tabId>
```
