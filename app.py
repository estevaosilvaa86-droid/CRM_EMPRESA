from banco import conectar

from cliente import (
    cadastrar_cliente,
    listar_clientes,
    buscar_cliente,
    editar_cliente,
    excluir_cliente
)

from venda import (
    registrar_venda,
    listar_vendas,
    editar_venda,
    excluir_venda
)

from usuario import (
    fazer_login,
    criar_admin,
    cadastrar_usuario
)


def dashboard():
    conn = conectar()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT COUNT(*) FROM clientes"
        )
        clientes = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM vendas"
        )
        vendas = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COALESCE(SUM(valor), 0) FROM vendas"
        )
        faturamento = cursor.fetchone()[0]

        print("\n========== DASHBOARD ==========")
        print(f"Clientes cadastrados: {clientes}")
        print(f"Total de vendas: {vendas}")
        print(f"Faturamento: R$ {float(faturamento):.2f}")
        print("===============================")

    finally:
        cursor.close()
        conn.close()


def iniciar():
    criar_admin()

    cargo = fazer_login()

    if cargo is None:
        print("\nUsuário ou senha inválidos!")
        return

    print(f"\nLogin realizado com sucesso!")
    print(f"Cargo: {cargo}")

    while True:

        print("\n========== CRM EMPRESA ==========")
        print("1 - Cadastrar cliente")
        print("2 - Listar clientes")
        print("3 - Registrar venda")
        print("4 - Listar vendas")
        print("5 - Dashboard")
        print("6 - Editar cliente")
        print("7 - Excluir cliente")
        print("8 - Buscar cliente")
        print("9 - Editar venda")
        print("10 - Excluir venda")
        print("11 - Cadastrar usuário")
        print("0 - Sair")
        print("=================================")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_cliente()

        elif opcao == "2":
            listar_clientes()

        elif opcao == "3":
            registrar_venda()

        elif opcao == "4":
            listar_vendas()

        elif opcao == "5":
            dashboard()

        elif opcao == "6":
            if cargo != "admin":
                print("Acesso negado!")
            else:
                editar_cliente()

        elif opcao == "7":
            if cargo != "admin":
                print("Acesso negado!")
            else:
                excluir_cliente()

        elif opcao == "8":
            buscar_cliente()

        elif opcao == "9":
            if cargo != "admin":
                print("Acesso negado!")
            else:
                editar_venda()

        elif opcao == "10":
            if cargo != "admin":
                print("Acesso negado!")
            else:
                excluir_venda()

        elif opcao == "11":
            if cargo != "admin":
                print("Acesso negado!")
            else:
                cadastrar_usuario()

        elif opcao == "0":
            print("Encerrando o CRM...")
            break

        else:
            print("Opção inválida!")


if __name__ == "__main__":
    iniciar()