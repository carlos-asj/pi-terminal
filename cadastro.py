import json
import re
from pathlib import Path

from auth import USUARIOS_PATH, carregar_usuarios, hash_senha

CADASTROS_PATH = Path(__file__).parent / "dados" / "cadastros.json"
CODIGO_MOTORISTA_PATH = Path(__file__).parent / "dados" / "codigo_motorista.json"

PERFIL_ALUNO = "aluno"
PERFIL_MOTORISTA = "motorista"

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def email_valido(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))


def email_disponivel(email: str) -> bool:
    return email not in carregar_usuarios()


def carregar_cadastros() -> dict:
    if not CADASTROS_PATH.exists():
        return {}
    with open(CADASTROS_PATH, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def obter_perfil(email: str) -> str:
    """Cadastros antigos (sem o campo 'perfil') são tratados como alunos."""
    return carregar_cadastros().get(email, {}).get("perfil", PERFIL_ALUNO)


def codigo_motorista_valido(codigo_informado: str) -> bool:
    """Confere o código de autorização exigido para criar conta de motorista."""
    if not CODIGO_MOTORISTA_PATH.exists():
        raise FileNotFoundError(
            f"Arquivo {CODIGO_MOTORISTA_PATH.name} não encontrado em 'dados/'. "
            "Crie-o com o conteúdo: {\"codigo\": \"SEU_CODIGO\"}"
        )
    with open(CODIGO_MOTORISTA_PATH, "r", encoding="utf-8") as arquivo:
        return codigo_informado.strip() == json.load(arquivo)["codigo"]


def registrar_usuario(
    nome_completo: str,
    email: str,
    faculdade: str,
    telefone: str,
    senha: str,
    perfil: str = PERFIL_ALUNO,
) -> None:
    usuarios = carregar_usuarios()
    usuarios[email] = hash_senha(senha)
    with open(USUARIOS_PATH, "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=2, ensure_ascii=False)

    cadastros = carregar_cadastros()
    cadastros[email] = {
        "nome_completo": nome_completo,
        "email": email,
        "faculdade": faculdade,
        "telefone": telefone,
        "perfil": perfil,
    }
    CADASTROS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CADASTROS_PATH, "w", encoding="utf-8") as arquivo:
        json.dump(cadastros, arquivo, indent=2, ensure_ascii=False)
