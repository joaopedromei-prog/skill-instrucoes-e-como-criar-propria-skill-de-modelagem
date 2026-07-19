"""Gera token.json (OAuth) com escopos de Docs + Drive. Roda uma vez.

Uso:
    python3 setup_auth.py

Pré-requisito: scripts/credentials.json (OAuth Client tipo Desktop). Ver SETUP.md.
Abre o navegador para você logar com a conta que tem acesso ao Google Doc.
"""
from _common import get_services


def main():
    docs, drive = get_services()  # dispara o fluxo OAuth se necessário
    about = drive.about().get(fields="user(emailAddress)").execute()
    email = about.get("user", {}).get("emailAddress", "?")
    print(f"OK — autenticado como {email}. token.json criado em scripts/.")


if __name__ == "__main__":
    main()
