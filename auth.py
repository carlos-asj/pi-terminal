import hashlib
import json
from pathlib import Path

USUARIOS_PATH = Path(__file__).parent / "dados" / "usuarios.json"


def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def carregar_usuarios() -> dict:
    with open(USUARIOS_PATH, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def autenticar(usuario: str, senha: str) -> bool:
    usuarios = carregar_usuarios()
    return usuarios.get(usuario) == hash_senha(senha)
