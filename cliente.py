from banco import conectar


def cadastrar_cliente():
    print("\n===== CADASTRAR CLIENTE =====")

    nome = input("Nome: ").strip()
    telefone = input("Telefone: ").strip()
    email = input("Email: ").strip()

    if not nome:
        print("O nome é obrigatório!")
        return

    conn = conectar()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO clientes (nome, telefone, email)
            VALUES (%s, %s, %s)
            """,
            (nome, telefone, email)
        )

        conn.commit()

        print("Cliente cadastrado com sucesso!")

    except Exception as erro:
        conn.rollback()
        print(f"Erro ao cadastrar cliente: {erro}")

    finally:
        cursor.close()
        conn.close()


def listar_clientes():
    conn = conectar()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT id, nome, telefone, email
            FROM clientes
            ORDER BY id DESC
            """
        )

        clientes = cursor.fetchall()

        print("\n===== CLIENTES =====")

        if not clientes:
            print("Nenhum cliente cadastrado.")
            return

        for cliente in clientes:
            print(
                f"ID: {cliente[0]} | "
                f"Nome: {cliente[1]} | "
                f"Telefone: {cliente[2]} | "
                f"Email: {cliente[3]}"
            )

    finally:
        cursor.close()
        conn.close()


def buscar_cliente():
    nome = input("\nNome para buscar: ").strip()

    conn = conectar()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT id, nome, telefone, email
            FROM clientes
            WHERE nome LIKE %s
            ORDER BY nome
            """,
            ("%" + nome + "%",)
        )

        resultados = cursor.fetchall()

        if resultados:
            print("\n===== RESULTADOS =====")

            for cliente in resultados:
                print(
                    f"ID: {cliente[0]} | "
                    f"Nome: {cliente[1]} | "
                    f"Telefone: {cliente[2]} | "
                    f"Email: {cliente[3]}"
                )
        else:
            print("Cliente não encontrado!")

    finally:
        cursor.close()
        conn.close()


def editar_cliente():
    id_cliente = input("ID do cliente: ").strip()

    nome = input("Novo nome: ").strip()
    telefone = input("Novo telefone: ").strip()
    email = input("Novo email: ").strip()

    conn = conectar()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE clientes
            SET nome = %s,
                telefone = %s,
                email = %s
            WHERE id = %s
            """,
            (
                nome,
                telefone,
                email,
                id_cliente
            )
        )

        if cursor.rowcount == 0:
            print("Cliente não encontrado!")
        else:
            conn.commit()
            print("Cliente atualizado com sucesso!")

    except Exception as erro:
        conn.rollback()
        print(f"Erro ao editar cliente: {erro}")

    finally:
        cursor.close()
        conn.close()


def excluir_cliente():
    id_cliente = input("ID do cliente: ").strip()

    conn = conectar()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id FROM clientes WHERE id = %s",
            (id_cliente,)
        )

        cliente = cursor.fetchone()

        if not cliente:
            print("Cliente não encontrado!")
            return

        confirmacao = input(
            "Tem certeza que deseja excluir? (s/n): "
        ).strip().lower()

        if confirmacao != "s":
            print("Operação cancelada.")
            return

        cursor.execute(
            "DELETE FROM clientes WHERE id = %s",
            (id_cliente,)
        )

        conn.commit()

        print("Cliente excluído com sucesso!")

    except Exception as erro:
        conn.rollback()
        print(f"Erro ao excluir cliente: {erro}")

    finally:
        cursor.close()
        conn.close()