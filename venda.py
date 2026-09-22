from banco import conectar


def registrar_venda():
    print("\n===== REGISTRAR VENDA =====")

    cliente_id = input("ID do cliente: ").strip()
    valor = input("Valor: ").strip()
    pagamento = input(
        "Pagamento (Pix/Dinheiro/Cartao): "
    ).strip()

    if not cliente_id or not valor or not pagamento:
        print("Preencha todos os campos!")
        return

    try:
        valor = float(valor.replace(",", "."))
    except ValueError:
        print("Valor inválido!")
        return

    if valor <= 0:
        print("O valor deve ser maior que zero!")
        return

    conn = conectar()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id FROM clientes WHERE id = %s",
            (cliente_id,)
        )

        cliente = cursor.fetchone()

        if not cliente:
            print("Cliente não encontrado!")
            return

        cursor.execute(
            """
            INSERT INTO vendas
            (cliente_id, valor, pagamento)
            VALUES (%s, %s, %s)
            """,
            (
                cliente_id,
                valor,
                pagamento
            )
        )

        conn.commit()

        print("Venda registrada com sucesso!")

    except Exception as erro:
        conn.rollback()
        print(f"Erro ao registrar venda: {erro}")

    finally:
        cursor.close()
        conn.close()


def listar_vendas():
    conn = conectar()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT
                vendas.id,
                clientes.nome,
                vendas.valor,
                vendas.pagamento
            FROM vendas
            INNER JOIN clientes
                ON vendas.cliente_id = clientes.id
            ORDER BY vendas.id DESC
            """
        )

        vendas = cursor.fetchall()

        print("\n===== VENDAS =====")

        if not vendas:
            print("Nenhuma venda registrada.")
            return

        for venda in vendas:
            print(
                f"ID: {venda[0]} | "
                f"Cliente: {venda[1]} | "
                f"Valor: R$ {float(venda[2]):.2f} | "
                f"Pagamento: {venda[3]}"
            )

    finally:
        cursor.close()
        conn.close()


def editar_venda():
    print("\n===== EDITAR VENDA =====")

    id_venda = input("ID da venda: ").strip()
    valor = input("Novo valor: ").strip()
    pagamento = input("Novo pagamento: ").strip()

    try:
        valor = float(valor.replace(",", "."))
    except ValueError:
        print("Valor inválido!")
        return

    if valor <= 0:
        print("O valor deve ser maior que zero!")
        return

    conn = conectar()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id FROM vendas WHERE id = %s",
            (id_venda,)
        )

        venda = cursor.fetchone()

        if not venda:
            print("Venda não encontrada!")
            return

        cursor.execute(
            """
            UPDATE vendas
            SET valor = %s,
                pagamento = %s
            WHERE id = %s
            """,
            (
                valor,
                pagamento,
                id_venda
            )
        )

        conn.commit()

        print("Venda atualizada com sucesso!")

    except Exception as erro:
        conn.rollback()
        print(f"Erro ao editar venda: {erro}")

    finally:
        cursor.close()
        conn.close()


def excluir_venda():
    print("\n===== EXCLUIR VENDA =====")

    id_venda = input("ID da venda: ").strip()

    conn = conectar()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id FROM vendas WHERE id = %s",
            (id_venda,)
        )

        venda = cursor.fetchone()

        if not venda:
            print("Venda não encontrada!")
            return

        confirmacao = input(
            "Tem certeza que deseja excluir? (s/n): "
        ).strip().lower()

        if confirmacao != "s":
            print("Operação cancelada.")
            return

        cursor.execute(
            "DELETE FROM vendas WHERE id = %s",
            (id_venda,)
        )

        conn.commit()

        print("Venda excluída com sucesso!")

    except Exception as erro:
        conn.rollback()
        print(f"Erro ao excluir venda: {erro}")

    finally:
        cursor.close()
        conn.close()