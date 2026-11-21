from datetime import date, datetime

from cadastro import PERFIL_ALUNO, carregar_cadastros
from presenca import carregar_registros


def alunos_que_assinaram_hoje() -> list[dict]:
    """Retorna apenas os alunos que assinaram a presença no dia atual."""
    hoje = date.today()

    assinaturas = {}
    for registro in carregar_registros():
        try:
            momento = datetime.fromisoformat(registro["data_hora"])
        except (ValueError, KeyError):
            continue
        if momento.date() == hoje and registro["assinou"] == "sim":
            assinaturas.setdefault(registro["usuario"], momento)  # mantém a 1ª assinatura

    cadastros = carregar_cadastros()
    linhas = []
    for email, momento in assinaturas.items():
        cadastro = cadastros.get(email)
        if cadastro is None or cadastro.get("perfil", PERFIL_ALUNO) != PERFIL_ALUNO:
            continue
        linhas.append({
            "nome": cadastro["nome_completo"],
            "faculdade": cadastro.get("faculdade", ""),
            "hora": momento.strftime("%H:%M"),
        })
    return sorted(linhas, key=lambda linha: linha["nome"].lower())


def exibir_lista_hoje() -> None:
    linhas = alunos_que_assinaram_hoje()
    print(f"\n=== ALUNOS QUE ASSINARAM HOJE - {date.today().strftime('%d/%m/%Y')} ===")
    if not linhas:
        print("Nenhum aluno assinou a lista hoje.")
        return

    for i, linha in enumerate(linhas, start=1):
        print(f"{i:>2}. {linha['nome']} ({linha['faculdade']}) - assinou às {linha['hora']}")
    print(f"\nTotal: {len(linhas)} aluno(s).")
