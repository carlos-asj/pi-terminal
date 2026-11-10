import csv
import json
from datetime import datetime
from pathlib import Path

QRCODE_PATH = Path(__file__).parent / "dados" / "qrcode_valido.json"
REGISTROS_PATH = Path(__file__).parent / "registros" / "lista_presenca.csv"


def _carregar_codigo_valido() -> str:
    with open(QRCODE_PATH, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return dados["codigo"]


def validar_qrcode(codigo_informado: str) -> bool:
    return codigo_informado.strip() == _carregar_codigo_valido()


def registrar_presenca(usuario: str, assinou: bool) -> None:
    REGISTROS_PATH.parent.mkdir(parents=True, exist_ok=True)
    arquivo_existe = REGISTROS_PATH.exists()
    with open(REGISTROS_PATH, "a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        if not arquivo_existe:
            escritor.writerow(["usuario", "data_hora", "assinou"])
        escritor.writerow(
            [usuario, datetime.now().isoformat(timespec="seconds"), "sim" if assinou else "nao"]
        )
