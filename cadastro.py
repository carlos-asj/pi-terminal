import json
import re
from pathlib import Path

from auth import USUARIOS_PATH, carregar_usuarios, hash_senha

CADASTROS_PATH = Path(__file__).parent / "dados" / "cadastros.json"

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def email_valido(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))


def email_disponivel(email: str) -> bool:
    return email not in carregar_usuarios()


def _carregar_cadastros() -> dict:
    if not CADASTROS_PATH.exists():
        return {}
    with open(CADASTROS_PATH, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def registrar_usuario(nome_completo: str, email: str, faculdade: str, telefone: str, senha: str) -> None:
    usuarios = carregar_usuarios()
    usuarios[email] = hash_senha(senha)
    with open(USUARIOS_PATH, "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=2, ensure_ascii=False)

    cadastros = _carregar_cadastros()
    cadastros[email] = {
        "nome_completo": nome_completo,
        "email": email,
        "faculdade": faculdade,
        "telefone": telefone,
    }
    CADASTROS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CADASTROS_PATH, "w", encoding="utf-8") as arquivo:
        json.dump(cadastros, arquivo, indent=2, ensure_ascii=False)
