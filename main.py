from auth import autenticar
from cadastro import (
    PERFIL_ALUNO,
    PERFIL_MOTORISTA,
    carregar_cadastros,
    codigo_motorista_valido,
    email_disponivel,
    email_valido,
    obter_perfil,
    registrar_usuario,
)
from motorista import exibir_lista_hoje
from presenca import registrar_presenca, validar_qrcode

MAX_TENTATIVAS_QRCODE = 3
MAX_TENTATIVAS_CODIGO_MOTORISTA = 3


def exibir_menu() -> str:
    print("=== MENU ===")
    print("1 - Login")
    print("2 - Registro")
    print("3 - Sair")
    while True:
        opcao = input("Escolha uma opção: ").strip()
        if opcao in ("1", "2", "3"):
            return opcao
        print("Opção inválida. Digite 1, 2 ou 3.\n")


def login() -> str | None:
    print("\n=== LOGIN ===")
    print("(Deixe o e-mail em branco e pressione Enter para voltar ao menu)\n")
    while True:
        usuario = input("E-mail: ").strip()
        if not usuario:
            return None
        senha = input("Senha: ").strip()
        if autenticar(usuario, senha):
            nome = carregar_cadastros().get(usuario, {}).get("nome_completo", usuario)
            print(f"\nBem-vindo(a), {nome}!\n")
            return usuario
        print("Usuário ou senha inválidos. Tente novamente.\n")


def solicitar_campo_obrigatorio(rotulo: str) -> str:
    while True:
        valor = input(rotulo).strip()
        if valor:
            return valor
        print("Este campo é obrigatório.\n")


def escolher_perfil() -> str:
    print("\nTipo de cadastro:")
    print("1 - Aluno")
    print("2 - Motorista")
    while True:
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            return PERFIL_ALUNO
        if opcao == "2":
            return PERFIL_MOTORISTA
        print("Opção inválida. Digite 1 ou 2.\n")


def autorizar_motorista() -> bool:
    """Evita que qualquer pessoa crie conta de motorista e veja a lista de alunos."""
    for _ in range(MAX_TENTATIVAS_CODIGO_MOTORISTA):
        codigo = input("Código de autorização de motorista: ").strip()
        if codigo_motorista_valido(codigo):
            return True
        print("Código inválido.\n")
    print("Número máximo de tentativas atingido. Cadastro cancelado.")
    return False


def registro() -> str | None:
    print("\n=== REGISTRO ===")
    perfil = escolher_perfil()
    if perfil == PERFIL_MOTORISTA and not autorizar_motorista():
        return None


    nome_completo = solicitar_campo_obrigatorio("Nome completo: ")

    while True:
        email = solicitar_campo_obrigatorio("E-mail: ")
        if not email_valido(email):
            print("E-mail inválido. Tente novamente.\n")
            continue
        if not email_disponivel(email):
            print("Este e-mail já está cadastrado. Tente novamente.\n")
            continue
        break

    faculdade = solicitar_campo_obrigatorio("Faculdade: ") if perfil == PERFIL_ALUNO else ""
    telefone = solicitar_campo_obrigatorio("Telefone: ")

    while True:
        senha = solicitar_campo_obrigatorio("Crie uma senha: ")
        confirmacao = solicitar_campo_obrigatorio("Confirme a senha: ")
        if senha == confirmacao:
            break
        print("As senhas não coincidem. Tente novamente.\n")

    registrar_usuario(nome_completo, email, faculdade, telefone, senha, perfil)
    print(f"\nCadastro realizado com sucesso! Bem-vindo(a), {nome_completo}!\n")
    return email


def perguntar_assinatura() -> bool:
    while True:
        resposta = input("Deseja assinar a lista de presença? (s/n): ").strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("Resposta inválida. Digite 's' para sim ou 'n' para não.\n")


def solicitar_qrcode() -> bool:
    tentativas_restantes = MAX_TENTATIVAS_QRCODE
    while tentativas_restantes > 0:
        codigo = input("Informe o código do QR Code do ônibus: ").strip()
        if validar_qrcode(codigo):
            print("\n✅ Assinatura confirmada com sucesso!")
            return True
        tentativas_restantes -= 1
        if tentativas_restantes > 0:
            print(f"\n❌ Código inválido. Tente novamente ({tentativas_restantes} tentativa(s) restante(s)).\n")
    print("\n❌ Código inválido. Assinatura não registrada.")
    return False


def fluxo_aluno(usuario: str) -> None:
    if perguntar_assinatura():
        assinatura_confirmada = solicitar_qrcode()
        registrar_presenca(usuario, assinatura_confirmada)
    else:
        print("\nOk, assinatura não realizada.")
        registrar_presenca(usuario, False)


def fluxo_motorista() -> None:
    while True:
        print("=== MENU DO MOTORISTA ===")
        print("1 - Ver lista de alunos de hoje")
        print("2 - Voltar ao menu principal")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            exibir_lista_hoje()
        elif opcao == "2":
            return
        else:
            print("Opção inválida. Digite 1, 2 ou 3.")
        print()


def main() -> None:
    while True:
        try:
            opcao = exibir_menu()
            if opcao == "3":
                print("\nAté logo!")
                break

            usuario = login() if opcao == "1" else registro()
            if usuario is None:
                continue

            if obter_perfil(usuario) == PERFIL_MOTORISTA:
                fluxo_motorista()
            else:
                fluxo_aluno(usuario)

        except (EOFError, KeyboardInterrupt):
            print("\n\nEncerrando o programa.")
            break
        except Exception as erro:
            print(f"\n⚠️  Ocorreu um erro inesperado: {erro}")
            print("Vamos continuar. Tente novamente.")

        print("\n" + "-" * 40 + "\n")


if __name__ == "__main__":
    main()
