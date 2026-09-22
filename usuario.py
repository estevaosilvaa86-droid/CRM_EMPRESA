import hashlib
from banco import conectar


def gerar_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def fazer_login():
    print("\n===== LOGIN =====")

    usuario = input("Usuário: ").strip()
    senha = input("Senha: ").strip()

    conn = conectar()

    if conn is None:
        return None

    cursor = conn.cursor()

    try:
        senha_hash = gerar_hash(senha)

        cursor.execute(
            """
            SELECT cargo
            FROM usuarios
            WHERE usuario = %s AND senha = %s
            """,
            (usuario, senha_hash)
        )

        resultado = cursor.fetchone()

        if resultado:
            return resultado[0]

        return None

    except Exception as erro:
        print(f"Erro no login: {erro}")
        return None

    finally:
        cursor.close()
        conn.close()


def cadastrar_usuario():
    print("\n===== CADASTRAR USUÁRIO =====")

    nome = input("Nome: ").strip()
    usuario = input("Usuário: ").strip()
    senha = input("Senha: ").strip()
    cargo = input("Cargo (admin/vendedor): ").strip().lower()

    if not nome or not usuario or not senha:
        print("Preencha todos os campos!")
        return

    if cargo not in ("admin", "vendedor"):
        print("Cargo inválido!")
        return

    conn = conectar()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        senha_hash = gerar_hash(senha)

        cursor.execute(
            """
            INSERT INTO usuarios
            (nome, usuario, senha, cargo)
            VALUES (%s, %s, %s, %s)
            """,
            (
                nome,
                usuario,
                senha_hash,
                cargo
            )
        )

        conn.commit()

        print("Usuário cadastrado com sucesso!")

    except Exception as erro:
        conn.rollback()
        print(f"Erro ao cadastrar usuário: {erro}")

    finally:
        cursor.close()
        conn.close()


def criar_admin():
    """
    Garante que o administrador exista.
    Se já existir, redefine a senha para 123456.
    """

    conn = conectar()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT id
            FROM usuarios
            WHERE usuario = %s
            """,
            ("admin",)
        )

        admin = cursor.fetchone()

        senha_hash = gerar_hash("123456")

        if admin is None:

            cursor.execute(
                """
                INSERT INTO usuarios
                (nome, usuario, senha, cargo)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    "Administrador",
                    "admin",
                    senha_hash,
                    "admin"
                )
            )

            conn.commit()

            print("\nAdministrador criado com sucesso!")
            print("Usuário: admin")
            print("Senha: 123456")

        else:

            cursor.execute(
                """
                UPDATE usuarios
                SET senha = %s,
                    cargo = %s
                WHERE usuario = %s
                """,
                (
                    senha_hash,
                    "admin",
                    "admin"
                )
            )

            conn.commit()

            print("\nAdministrador configurado com sucesso!")
            print("Usuário: admin")
            print("Senha: 123456")

    except Exception as erro:
        conn.rollback()
        print(f"Erro ao configurar administrador: {erro}")

    finally:
        cursor.close()
        conn.close()