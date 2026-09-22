import customtkinter as ctk
from tkinter import messagebox
from decimal import Decimal, InvalidOperation
from datetime import datetime
import hashlib

from banco import conectar


# ============================================================
# BELO SABOR
# Interface Premium
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ============================================================
# CORES
# ============================================================

BG = "#07111F"
SIDEBAR = "#0A1626"
SURFACE = "#0E1B2D"
SURFACE_2 = "#122238"
SURFACE_HOVER = "#172A42"

RED = "#E63946"
RED_HOVER = "#F04B57"

WHITE = "#F8FAFC"
TEXT = "#D8E1EC"
MUTED = "#8190A5"
MUTED_2 = "#5F7086"

GREEN = "#28C76F"
BLUE = "#4C8DFF"
ORANGE = "#F5A623"

BORDER = "#1C3048"


# ============================================================
# FUNÇÕES
# ============================================================

def gerar_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def moeda(valor):

    try:

        valor = float(valor)

        return (
            f"R$ {valor:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    except Exception:

        return "R$ 0,00"


# ============================================================
# APLICAÇÃO
# ============================================================

class BeloSaborApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Belo Sabor")
        self.geometry("1400x850")
        self.minsize(1100, 700)

        self.configure(
            fg_color=BG
        )

        self.usuario_logado = None
        self.cargo = None

        self.nav_buttons = {}

        self.mostrar_login()
        self.after(100, self.centralizar_janela)

    # ========================================================
    # LIMPAR
    # ========================================================

    def limpar(self):

        for widget in self.winfo_children():
            widget.destroy()

    def centralizar_janela(self):

        self.update_idletasks()

        largura = self.winfo_width()
        altura = self.winfo_height()
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        pos_x = (largura_tela - largura) // 2
        pos_y = (altura_tela - altura) // 2

        self.geometry(
            f"{largura}x{altura}+{pos_x}+{pos_y}"
        )

    # ========================================================
    # LOGIN
    # ========================================================

    def mostrar_login(self):

        self.limpar()

        self.grid_rowconfigure(
            0,
            weight=1
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_columnconfigure(
            1,
            weight=0
        )

        # ----------------------------------------------------
        # FUNDO
        # ----------------------------------------------------

        container = ctk.CTkFrame(
            self,
            fg_color=BG,
            corner_radius=0
        )

        container.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # ----------------------------------------------------
        # MARCA
        # ----------------------------------------------------

        marca = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )

        marca.place(
            relx=0.15,
            rely=0.5,
            anchor="center"
        )

        ctk.CTkLabel(
            marca,
            text="BELO",
            text_color=WHITE,
            font=("Arial", 52, "bold")
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            marca,
            text="SABOR",
            text_color=RED,
            font=("Arial", 52, "bold")
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            marca,
            text="Gestão simples. Decisões melhores.",
            text_color=MUTED,
            font=("Arial", 17)
        ).pack(
            anchor="w",
            pady=(15, 0)
        )

        # ----------------------------------------------------
        # LINHA DECORATIVA
        # ----------------------------------------------------

        linha = ctk.CTkFrame(
            marca,
            width=75,
            height=4,
            fg_color=RED,
            corner_radius=5
        )

        linha.pack(
            anchor="w",
            pady=(25, 0)
        )

        # ----------------------------------------------------
        # LOGIN
        # ----------------------------------------------------

        box = ctk.CTkFrame(
            container,
            width=430,
            height=500,
            fg_color=SURFACE,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )

        box.place(
            relx=0.72,
            rely=0.5,
            anchor="center"
        )

        box.pack_propagate(False)

        ctk.CTkLabel(
            box,
            text="Acessar sistema",
            text_color=WHITE,
            font=("Arial", 28, "bold")
        ).pack(
            anchor="w",
            padx=45,
            pady=(50, 5)
        )

        ctk.CTkLabel(
            box,
            text="Entre com suas credenciais",
            text_color=MUTED,
            font=("Arial", 14)
        ).pack(
            anchor="w",
            padx=45,
            pady=(0, 35)
        )

        self.login_usuario = ctk.CTkEntry(
            box,
            width=340,
            height=48,
            corner_radius=9,
            fg_color=BG,
            border_color=BORDER,
            border_width=1,
            placeholder_text="Usuário",
            text_color=WHITE
        )

        self.login_usuario.pack(
            padx=45,
            pady=7
        )

        self.login_senha = ctk.CTkEntry(
            box,
            width=340,
            height=48,
            corner_radius=9,
            fg_color=BG,
            border_color=BORDER,
            border_width=1,
            placeholder_text="Senha",
            show="*",
            text_color=WHITE
        )

        self.login_senha.pack(
            padx=45,
            pady=7
        )

        self.login_senha.bind(
            "<Return>",
            lambda event: self.fazer_login()
        )

        self.login_erro = ctk.CTkLabel(
            box,
            text="",
            text_color=RED,
            font=("Arial", 12)
        )

        self.login_erro.pack(
            pady=(10, 3)
        )

        ctk.CTkButton(
            box,
            text="Entrar",
            width=340,
            height=48,
            corner_radius=9,
            fg_color=RED,
            hover_color=RED_HOVER,
            font=("Arial", 14, "bold"),
            command=self.fazer_login
        ).pack(
            padx=45,
            pady=15
        )

        ctk.CTkLabel(
            box,
            text="BELO SABOR  •  SISTEMA DE GESTÃO",
            text_color=MUTED_2,
            font=("Arial", 9)
        ).pack(
            side="bottom",
            pady=25
        )

    # ========================================================
    # LOGIN
    # ========================================================

    def fazer_login(self):

        usuario = self.login_usuario.get().strip()
        senha = self.login_senha.get().strip()

        if not usuario or not senha:

            self.login_erro.configure(
                text="Preencha usuário e senha."
            )

            return

        conn = conectar()

        if conn is None:

            self.login_erro.configure(
                text="Não foi possível conectar ao banco."
            )

            return

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT usuario, cargo
                FROM usuarios
                WHERE usuario = %s
                AND senha = %s
                """,
                (
                    usuario,
                    gerar_hash(senha)
                )
            )

            resultado = cursor.fetchone()

            if resultado:

                self.usuario_logado = resultado[0]
                self.cargo = resultado[1]

                self.mostrar_sistema()

            else:

                self.login_erro.configure(
                    text="Usuário ou senha inválidos."
                )

        except Exception as erro:

            self.login_erro.configure(
                text=f"Erro: {erro}"
            )

        finally:

            cursor.close()
            conn.close()

    # ========================================================
    # SISTEMA
    # ========================================================

    def mostrar_sistema(self):

        self.limpar()

        self.grid_rowconfigure(
            0,
            weight=1
        )

        self.grid_columnconfigure(
            0,
            weight=0
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.criar_sidebar()
        self.criar_conteudo()

        self.mostrar_dashboard()

    # ========================================================
    # SIDEBAR
    # ========================================================

    def criar_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=235,
            fg_color=SIDEBAR,
            corner_radius=0
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        # ----------------------------------------------------
        # LOGO
        # ----------------------------------------------------

        logo = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        logo.pack(
            fill="x",
            padx=28,
            pady=(32, 35)
        )

        ctk.CTkLabel(
            logo,
            text="BELO",
            text_color=WHITE,
            font=("Arial", 25, "bold")
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            logo,
            text=" SABOR",
            text_color=RED,
            font=("Arial", 25, "bold")
        ).pack(
            side="left"
        )

        # ----------------------------------------------------
        # MENU
        # ----------------------------------------------------

        ctk.CTkLabel(
            self.sidebar,
            text="MENU",
            text_color=MUTED_2,
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w",
            padx=28,
            pady=(0, 10)
        )

        self.criar_nav(
            "Dashboard",
            self.mostrar_dashboard
        )

        self.criar_nav(
            "Clientes",
            self.mostrar_clientes
        )

        self.criar_nav(
            "Vendas",
            self.mostrar_vendas
        )

        if self.cargo == "admin":

            self.criar_nav(
                "Usuários",
                self.mostrar_usuarios
            )

        # ----------------------------------------------------
        # PARTE INFERIOR
        # ----------------------------------------------------

        bottom = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        bottom.pack(
            side="bottom",
            fill="x",
            padx=18,
            pady=22
        )

        linha = ctk.CTkFrame(
            bottom,
            height=1,
            fg_color=BORDER
        )

        linha.pack(
            fill="x",
            pady=(0, 15)
        )

        ctk.CTkLabel(
            bottom,
            text=self.usuario_logado,
            text_color=WHITE,
            font=("Arial", 13, "bold")
        ).pack(
            anchor="w",
            padx=10
        )

        ctk.CTkLabel(
            bottom,
            text=self.cargo.capitalize(),
            text_color=RED,
            font=("Arial", 10)
        ).pack(
            anchor="w",
            padx=10,
            pady=(2, 10)
        )

        ctk.CTkButton(
            bottom,
            text="Sair",
            height=38,
            corner_radius=8,
            fg_color="transparent",
            hover_color=SURFACE_HOVER,
            text_color=MUTED,
            anchor="w",
            command=self.sair
        ).pack(
            fill="x"
        )

    # ========================================================
    # NAVEGAÇÃO
    # ========================================================

    def criar_nav(
        self,
        texto,
        comando
    ):

        botao = ctk.CTkButton(
            self.sidebar,
            text=texto,
            height=43,
            corner_radius=8,
            fg_color="transparent",
            hover_color=SURFACE_HOVER,
            text_color=MUTED,
            font=("Arial", 13),
            anchor="w",
            command=comando
        )

        botao.pack(
            fill="x",
            padx=18,
            pady=3
        )

        self.nav_buttons[texto] = botao

    # ========================================================
    # ATIVAR MENU
    # ========================================================

    def ativar_menu(
        self,
        nome
    ):

        for texto, botao in self.nav_buttons.items():

            if texto == nome:

                botao.configure(
                    fg_color=RED,
                    text_color=WHITE
                )

            else:

                botao.configure(
                    fg_color="transparent",
                    text_color=MUTED
                )

    # ========================================================
    # ÁREA PRINCIPAL
    # ========================================================

    def criar_conteudo(self):

        self.main = ctk.CTkFrame(
            self,
            fg_color=BG,
            corner_radius=0
        )

        self.main.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.main.grid_rowconfigure(
            1,
            weight=1
        )

        self.main.grid_columnconfigure(
            0,
            weight=1
        )

        # ----------------------------------------------------
        # TOPBAR
        # ----------------------------------------------------

        self.topbar = ctk.CTkFrame(
            self.main,
            height=76,
            fg_color=BG
        )

        self.topbar.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=38
        )

        self.topbar.grid_propagate(False)

        self.titulo = ctk.CTkLabel(
            self.topbar,
            text="Dashboard",
            text_color=WHITE,
            font=("Arial", 25, "bold")
        )

        self.titulo.pack(
            side="left",
            pady=22
        )

        ctk.CTkLabel(
            self.topbar,
            text=datetime.now().strftime("%d/%m/%Y"),
            text_color=MUTED,
            font=("Arial", 12)
        ).pack(
            side="right",
            pady=22
        )

        # ----------------------------------------------------
        # CONTEÚDO
        # ----------------------------------------------------

        self.conteudo = ctk.CTkScrollableFrame(
            self.main,
            fg_color=BG,
            corner_radius=0
        )

        self.conteudo.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=28,
            pady=(0, 25)
        )

    # ========================================================
    # CABEÇALHO DA PÁGINA
    # ========================================================

    def pagina(
        self,
        titulo,
        descricao=None
    ):

        self.titulo.configure(
            text=titulo
        )

        self.limpar_conteudo()

        if descricao:

            ctk.CTkLabel(
                self.conteudo,
                text=descricao,
                text_color=MUTED,
                font=("Arial", 13)
            ).pack(
                anchor="w",
                pady=(0, 22)
            )

    # ========================================================
    # LIMPAR CONTEÚDO
    # ========================================================

    def limpar_conteudo(self):

        for widget in self.conteudo.winfo_children():
            widget.destroy()

    # ========================================================
    # DASHBOARD
    # ========================================================

    def mostrar_dashboard(self):

        self.ativar_menu(
            "Dashboard"
        )

        self.pagina(
            "Dashboard",
            f"Bem-vindo de volta, {self.usuario_logado}."
        )

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
                """
                SELECT COALESCE(SUM(valor), 0)
                FROM vendas
                """
            )

            faturamento = cursor.fetchone()[0]

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
                LIMIT 6
                """
            )

            ultimas = cursor.fetchall()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                str(erro)
            )

            return

        finally:

            cursor.close()
            conn.close()

        # ----------------------------------------------------
        # CARDS
        # ----------------------------------------------------

        cards = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent"
        )

        cards.pack(
            fill="x",
            pady=(0, 25)
        )

        for i in range(3):

            cards.grid_columnconfigure(
                i,
                weight=1
            )

        self.card(
            cards,
            "Clientes",
            str(clientes),
            "clientes cadastrados",
            RED,
            0
        )

        self.card(
            cards,
            "Vendas",
            str(vendas),
            "vendas registradas",
            BLUE,
            1
        )

        self.card(
            cards,
            "Faturamento",
            moeda(faturamento),
            "faturamento acumulado",
            GREEN,
            2
        )

        # ----------------------------------------------------
        # ÁREA INFERIOR
        # ----------------------------------------------------

        ctk.CTkLabel(
            self.conteudo,
            text="Atividade recente",
            text_color=WHITE,
            font=("Arial", 19, "bold")
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        tabela = ctk.CTkFrame(
            self.conteudo,
            fg_color=SURFACE,
            corner_radius=14,
            border_width=1,
            border_color=BORDER
        )

        tabela.pack(
            fill="x"
        )

        self.cabecalho_tabela(
            tabela,
            [
                ("ID", 0.08),
                ("CLIENTE", 0.42),
                ("PAGAMENTO", 0.22),
                ("VALOR", 0.28)
            ]
        )

        if not ultimas:

            ctk.CTkLabel(
                tabela,
                text="Nenhuma venda registrada ainda.",
                text_color=MUTED,
                font=("Arial", 13)
            ).pack(
                pady=35
            )

        else:

            for venda in ultimas:

                self.linha_venda(
                    tabela,
                    venda
                )

    # ========================================================
    # CARD
    # ========================================================

    def card(
        self,
        parent,
        titulo,
        valor,
        descricao,
        cor,
        coluna
    ):

        box = ctk.CTkFrame(
            parent,
            fg_color=SURFACE,
            corner_radius=14,
            height=140,
            border_width=1,
            border_color=BORDER
        )

        box.grid(
            row=0,
            column=coluna,
            sticky="ew",
            padx=5
        )

        box.grid_propagate(False)

        ctk.CTkFrame(
            box,
            width=4,
            fg_color=cor,
            corner_radius=4
        ).place(
            x=18,
            y=22,
            relheight=0.68
        )

        ctk.CTkLabel(
            box,
            text=titulo.upper(),
            text_color=MUTED,
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w",
            padx=38,
            pady=(25, 0)
        )

        ctk.CTkLabel(
            box,
            text=valor,
            text_color=WHITE,
            font=("Arial", 25, "bold")
        ).pack(
            anchor="w",
            padx=38
        )

        ctk.CTkLabel(
            box,
            text=descricao,
            text_color=MUTED_2,
            font=("Arial", 10)
        ).pack(
            anchor="w",
            padx=38
        )

    # ========================================================
    # CONFIGURAÇÃO DAS COLUNAS DAS TABELAS
    # ========================================================

    def configurar_colunas_tabela(self, frame, pesos):

        for i, peso in enumerate(pesos):
            frame.grid_columnconfigure(
                i,
                weight=peso,
                uniform="coluna_tabela"
            )

    # ========================================================
    # CABEÇALHO TABELA
    # ========================================================

    def cabecalho_tabela(
        self,
        parent,
        colunas
    ):

        header = ctk.CTkFrame(
            parent,
            height=48,
            fg_color=SURFACE_2,
            corner_radius=0
        )

        header.pack(
            fill="x"
        )

        pesos = [largura for texto, largura in colunas]
        self.configurar_colunas_tabela(header, pesos)

        for i, (texto, largura) in enumerate(colunas):

            ctk.CTkLabel(
                header,
                text=texto,
                text_color=MUTED,
                font=("Arial", 10, "bold"),
                anchor="center"
            ).grid(
                row=0,
                column=i,
                sticky="ew",
                padx=10,
                pady=12
            )

    # ========================================================
    # LINHA VENDA
    # ========================================================

    def linha_venda(
        self,
        parent,
        venda
    ):

        id_venda = venda[0]
        cliente = venda[1]
        valor = venda[2]
        pagamento = venda[3]

        linha = ctk.CTkFrame(
            parent,
            height=58,
            fg_color="transparent"
        )

        linha.pack(
            fill="x",
            padx=8,
            pady=1
        )

        pesos = [8, 42, 22, 28]
        self.configurar_colunas_tabela(linha, pesos)

        valores = [
            f"#{id_venda}",
            cliente,
            pagamento,
            moeda(valor)
        ]

        cores = [RED, WHITE, MUTED, GREEN]
        fontes = [
            ("Arial", 12, "bold"),
            ("Arial", 12),
            ("Arial", 12),
            ("Arial", 12, "bold")
        ]

        for i, texto in enumerate(valores):

            ctk.CTkLabel(
                linha,
                text=texto,
                text_color=cores[i],
                font=fontes[i],
                anchor="center"
            ).grid(
                row=0,
                column=i,
                sticky="ew",
                padx=10,
                pady=8
            )

    # ========================================================
    # CLIENTES
    # ========================================================

    def mostrar_clientes(self):

        self.ativar_menu(
            "Clientes"
        )

        self.pagina(
            "Clientes",
            "Gerencie sua base de clientes."
        )

        topo = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent"
        )

        topo.pack(
            fill="x",
            pady=(0, 15)
        )

        self.busca = ctk.CTkEntry(
            topo,
            width=360,
            height=44,
            corner_radius=9,
            fg_color=SURFACE,
            border_color=BORDER,
            placeholder_text="Buscar cliente..."
        )

        self.busca.pack(
            side="left"
        )

        self.busca.bind(
            "<KeyRelease>",
            lambda event: self.carregar_clientes()
        )

        ctk.CTkButton(
            topo,
            text="+  Novo cliente",
            width=145,
            height=44,
            corner_radius=9,
            fg_color=RED,
            hover_color=RED_HOVER,
            command=self.abrir_cadastro_cliente
        ).pack(
            side="right"
        )

        self.clientes_area = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent"
        )

        self.clientes_area.pack(
            fill="x"
        )

        self.carregar_clientes()

    # ========================================================
    # CARREGAR CLIENTES
    # ========================================================

    def carregar_clientes(self):

        if not hasattr(
            self,
            "clientes_area"
        ):
            return

        for widget in self.clientes_area.winfo_children():
            widget.destroy()

        pesquisa = self.busca.get().strip()

        conn = conectar()

        if conn is None:
            return

        cursor = conn.cursor()

        try:

            if pesquisa:

                cursor.execute(
                    """
                    SELECT id, nome, telefone, email
                    FROM clientes
                    WHERE nome LIKE %s
                    OR telefone LIKE %s
                    OR email LIKE %s
                    ORDER BY id DESC
                    """,
                    (
                        f"%{pesquisa}%",
                        f"%{pesquisa}%",
                        f"%{pesquisa}%"
                    )
                )

            else:

                cursor.execute(
                    """
                    SELECT id, nome, telefone, email
                    FROM clientes
                    ORDER BY id DESC
                    """
                )

            clientes = cursor.fetchall()

        finally:

            cursor.close()
            conn.close()

        tabela = ctk.CTkFrame(
            self.clientes_area,
            fg_color=SURFACE,
            corner_radius=14,
            border_width=1,
            border_color=BORDER
        )

        tabela.pack(
            fill="x"
        )

        header = ctk.CTkFrame(
            tabela,
            height=48,
            fg_color=SURFACE_2
        )

        header.pack(
            fill="x"
        )

        pesos = [1, 4, 3, 4, 3]
        self.configurar_colunas_tabela(header, pesos)

        for i, texto in enumerate([
            "ID",
            "CLIENTE",
            "TELEFONE",
            "E-MAIL",
            "AÇÕES"
        ]):

            ctk.CTkLabel(
                header,
                text=texto,
                text_color=MUTED,
                font=("Arial", 10, "bold"),
                anchor="center"
            ).grid(
                row=0,
                column=i,
                sticky="ew",
                padx=10,
                pady=12
            )

        for cliente in clientes:

            self.linha_cliente(
                tabela,
                cliente
            )

        if not clientes:

            ctk.CTkLabel(
                tabela,
                text="Nenhum cliente encontrado.",
                text_color=MUTED,
                font=("Arial", 13)
            ).pack(
                pady=35
            )

    # ========================================================
    # LINHA CLIENTE
    # ========================================================

    def linha_cliente(
        self,
        parent,
        cliente
    ):

        id_cliente = cliente[0]
        nome = cliente[1]
        telefone = cliente[2] or "-"
        email = cliente[3] or "-"

        linha = ctk.CTkFrame(
            parent,
            height=65,
            fg_color="transparent"
        )

        linha.pack(
            fill="x",
            padx=8,
            pady=2
        )

        pesos = [1, 4, 3, 4, 3]
        self.configurar_colunas_tabela(linha, pesos)

        dados = [
            f"#{id_cliente}",
            nome,
            telefone,
            email
        ]

        cores = [RED, WHITE, MUTED, MUTED]
        fontes = [
            ("Arial", 11, "bold"),
            ("Arial", 12),
            ("Arial", 11),
            ("Arial", 11)
        ]

        for i, texto in enumerate(dados):

            ctk.CTkLabel(
                linha,
                text=texto,
                text_color=cores[i],
                font=fontes[i],
                anchor="center"
            ).grid(
                row=0,
                column=i,
                sticky="ew",
                padx=10,
                pady=8
            )

        acoes = ctk.CTkFrame(
            linha,
            fg_color="transparent"
        )

        acoes.grid(
            row=0,
            column=4,
            sticky="nsew",
            padx=5,
            pady=8
        )

        acoes.grid_columnconfigure(
            0,
            weight=1
        )

        acoes.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkButton(
            acoes,
            text="Editar",
            width=65,
            height=30,
            corner_radius=7,
            fg_color=SURFACE_2,
            hover_color=SURFACE_HOVER,
            command=lambda: self.editar_cliente(id_cliente)
        ).grid(
            row=0,
            column=0,
            padx=2,
            pady=2
        )

        if self.cargo == "admin":

            ctk.CTkButton(
                acoes,
                text="Excluir",
                width=65,
                height=30,
                corner_radius=7,
                fg_color="#5A1D25",
                hover_color=RED,
                command=lambda: self.excluir_cliente(id_cliente)
            ).grid(
                row=0,
                column=1,
                padx=2,
                pady=2
            )

    # ========================================================
    # CADASTRAR CLIENTE
    # ========================================================

    def abrir_cadastro_cliente(self):

        janela = self.janela_formulario(
            "Novo cliente"
        )

        nome = self.campo(
            janela,
            "Nome completo"
        )

        telefone = self.campo(
            janela,
            "Telefone"
        )

        email = self.campo(
            janela,
            "E-mail"
        )

        def salvar():

            if not nome.get().strip():

                messagebox.showwarning(
                    "Atenção",
                    "Informe o nome do cliente."
                )

                return

            conn = conectar()

            if conn is None:
                return

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    INSERT INTO clientes
                    (nome, telefone, email)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        nome.get().strip(),
                        telefone.get().strip(),
                        email.get().strip()
                    )
                )

                conn.commit()

                janela.destroy()

                self.mostrar_clientes()

                messagebox.showinfo(
                    "Sucesso",
                    "Cliente cadastrado."
                )

            except Exception as erro:

                conn.rollback()

                messagebox.showerror(
                    "Erro",
                    str(erro)
                )

            finally:

                cursor.close()
                conn.close()

        self.botao_salvar(
            janela,
            "Cadastrar cliente",
            salvar
        )

    # ========================================================
    # EDITAR CLIENTE
    # ========================================================

    def editar_cliente(
        self,
        id_cliente
    ):

        if self.cargo != "admin":

            messagebox.showwarning(
                "Acesso negado",
                "Somente administradores podem editar clientes."
            )

            return

        conn = conectar()

        if conn is None:
            return

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT nome, telefone, email
                FROM clientes
                WHERE id = %s
                """,
                (id_cliente,)
            )

            cliente = cursor.fetchone()

        finally:

            cursor.close()
            conn.close()

        if not cliente:
            return

        janela = self.janela_formulario(
            "Editar cliente"
        )

        nome = self.campo(
            janela,
            "Nome completo",
            cliente[0]
        )

        telefone = self.campo(
            janela,
            "Telefone",
            cliente[1] or ""
        )

        email = self.campo(
            janela,
            "E-mail",
            cliente[2] or ""
        )

        def salvar():

            conn = conectar()

            if conn is None:
                return

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    UPDATE clientes
                    SET
                        nome = %s,
                        telefone = %s,
                        email = %s
                    WHERE id = %s
                    """,
                    (
                        nome.get().strip(),
                        telefone.get().strip(),
                        email.get().strip(),
                        id_cliente
                    )
                )

                conn.commit()

                janela.destroy()

                self.mostrar_clientes()

            except Exception as erro:

                conn.rollback()

                messagebox.showerror(
                    "Erro",
                    str(erro)
                )

            finally:

                cursor.close()
                conn.close()

        self.botao_salvar(
            janela,
            "Salvar alterações",
            salvar
        )

    # ========================================================
    # EXCLUIR CLIENTE
    # ========================================================

    def excluir_cliente(
        self,
        id_cliente
    ):

        if self.cargo != "admin":
            return

        if not messagebox.askyesno(
            "Excluir cliente",
            "Deseja realmente excluir este cliente?"
        ):
            return

        conn = conectar()

        if conn is None:
            return

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                DELETE FROM clientes
                WHERE id = %s
                """,
                (id_cliente,)
            )

            conn.commit()

            self.mostrar_clientes()

        except Exception as erro:

            conn.rollback()

            messagebox.showerror(
                "Erro",
                str(erro)
            )

        finally:

            cursor.close()
            conn.close()

    # ========================================================
    # VENDAS
    # ========================================================

    def mostrar_vendas(self):

        self.ativar_menu(
            "Vendas"
        )

        self.pagina(
            "Vendas",
            "Acompanhe e gerencie as vendas do negócio."
        )

        topo = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent"
        )

        topo.pack(
            fill="x",
            pady=(0, 15)
        )

        ctk.CTkButton(
            topo,
            text="+  Nova venda",
            width=140,
            height=44,
            corner_radius=9,
            fg_color=RED,
            hover_color=RED_HOVER,
            command=self.abrir_cadastro_venda
        ).pack(
            side="right"
        )

        self.vendas_area = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent"
        )

        self.vendas_area.pack(
            fill="x"
        )

        self.carregar_vendas()

    # ========================================================
    # CARREGAR VENDAS
    # ========================================================

    def carregar_vendas(self):

        for widget in self.vendas_area.winfo_children():
            widget.destroy()

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

        finally:

            cursor.close()
            conn.close()

        tabela = ctk.CTkFrame(
            self.vendas_area,
            fg_color=SURFACE,
            corner_radius=14,
            border_width=1,
            border_color=BORDER
        )

        tabela.pack(
            fill="x"
        )

        header = ctk.CTkFrame(
            tabela,
            height=48,
            fg_color=SURFACE_2
        )

        header.pack(
            fill="x"
        )

        pesos = [2, 8, 5, 5, 6]
        self.configurar_colunas_tabela(header, pesos)

        for i, texto in enumerate([
            "ID",
            "CLIENTE",
            "PAGAMENTO",
            "VALOR",
            "AÇÕES"
        ]):

            ctk.CTkLabel(
                header,
                text=texto,
                text_color=MUTED,
                font=("Arial", 10, "bold"),
                anchor="center"
            ).grid(
                row=0,
                column=i,
                sticky="ew",
                padx=10,
                pady=12
            )

        for venda in vendas:

            self.linha_venda_completa(
                tabela,
                venda
            )

        if not vendas:

            ctk.CTkLabel(
                tabela,
                text="Nenhuma venda registrada ainda.",
                text_color=MUTED,
                font=("Arial", 13)
            ).pack(
                pady=35
            )

    # ========================================================
    # LINHA VENDA
    # ========================================================

    def linha_venda_completa(
        self,
        parent,
        venda
    ):

        id_venda = venda[0]
        cliente = venda[1]
        valor = venda[2]
        pagamento = venda[3]

        linha = ctk.CTkFrame(
            parent,
            height=65,
            fg_color="transparent"
        )

        linha.pack(
            fill="x",
            padx=8,
            pady=2
        )

        pesos = [2, 8, 5, 5, 6]
        self.configurar_colunas_tabela(linha, pesos)

        dados = [
            f"#{id_venda}",
            cliente,
            pagamento,
            moeda(valor)
        ]

        cores = [RED, WHITE, MUTED, GREEN]
        fontes = [
            ("Arial", 11, "bold"),
            ("Arial", 12),
            ("Arial", 11),
            ("Arial", 12, "bold")
        ]

        for i, texto in enumerate(dados):

            ctk.CTkLabel(
                linha,
                text=texto,
                text_color=cores[i],
                font=fontes[i],
                anchor="center"
            ).grid(
                row=0,
                column=i,
                sticky="ew",
                padx=10,
                pady=8
            )

        acoes = ctk.CTkFrame(
            linha,
            fg_color="transparent"
        )

        acoes.grid(
            row=0,
            column=4,
            sticky="nsew",
            padx=5,
            pady=8
        )

        acoes.grid_columnconfigure(
            0,
            weight=1
        )

        acoes.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkButton(
            acoes,
            text="Editar",
            width=65,
            height=30,
            corner_radius=7,
            fg_color=SURFACE_2,
            hover_color=SURFACE_HOVER,
            command=lambda: self.editar_venda(id_venda)
        ).grid(
            row=0,
            column=0,
            padx=2,
            pady=2
        )

        if self.cargo == "admin":

            ctk.CTkButton(
                acoes,
                text="Excluir",
                width=65,
                height=30,
                corner_radius=7,
                fg_color="#5A1D25",
                hover_color=RED,
                command=lambda: self.excluir_venda(id_venda)
            ).grid(
                row=0,
                column=1,
                padx=2,
                pady=2
            )

    # ========================================================
    # NOVA VENDA
    # ========================================================

    def abrir_cadastro_venda(self):

        conn = conectar()

        if conn is None:
            return

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT id, nome
                FROM clientes
                ORDER BY nome
                """
            )

            clientes = cursor.fetchall()

        finally:

            cursor.close()
            conn.close()

        if not clientes:

            messagebox.showwarning(
                "Atenção",
                "Cadastre um cliente antes de registrar uma venda."
            )

            return

        janela = self.janela_formulario(
            "Nova venda",
            altura=500
        )

        nomes = [
            f"{cliente[0]} - {cliente[1]}"
            for cliente in clientes
        ]

        cliente = ctk.CTkOptionMenu(
            janela,
            values=nomes,
            width=350,
            height=44,
            corner_radius=9,
            fg_color=SURFACE_2,
            button_color=RED,
            button_hover_color=RED_HOVER
        )

        cliente.pack(
            pady=8
        )

        valor = self.campo(
            janela,
            "Valor da venda"
        )

        pagamento = ctk.CTkOptionMenu(
            janela,
            values=[
                "Pix",
                "Dinheiro",
                "Cartao"
            ],
            width=350,
            height=44,
            corner_radius=9,
            fg_color=SURFACE_2,
            button_color=RED,
            button_hover_color=RED_HOVER
        )

        pagamento.pack(
            pady=8
        )

        def salvar():

            try:

                valor_decimal = Decimal(
                    valor.get().replace(",", ".")
                )

                if valor_decimal <= 0:
                    raise InvalidOperation

            except InvalidOperation:

                messagebox.showwarning(
                    "Atenção",
                    "Digite um valor válido."
                )

                return

            cliente_id = int(
                cliente.get().split(" - ")[0]
            )

            conn = conectar()

            if conn is None:
                return

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    INSERT INTO vendas
                    (
                        cliente_id,
                        valor,
                        pagamento
                    )
                    VALUES (%s, %s, %s)
                    """,
                    (
                        cliente_id,
                        valor_decimal,
                        pagamento.get()
                    )
                )

                conn.commit()

                janela.destroy()

                self.mostrar_vendas()

                messagebox.showinfo(
                    "Sucesso",
                    "Venda registrada."
                )

            except Exception as erro:

                conn.rollback()

                messagebox.showerror(
                    "Erro",
                    str(erro)
                )

            finally:

                cursor.close()
                conn.close()

        self.botao_salvar(
            janela,
            "Registrar venda",
            salvar
        )

    # ========================================================
    # EDITAR VENDA
    # ========================================================

    def editar_venda(
        self,
        id_venda
    ):

        if self.cargo != "admin":

            messagebox.showwarning(
                "Acesso negado",
                "Somente administradores podem editar vendas."
            )

            return

        conn = conectar()

        if conn is None:
            return

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT valor, pagamento
                FROM vendas
                WHERE id = %s
                """,
                (id_venda,)
            )

            venda = cursor.fetchone()

        finally:

            cursor.close()
            conn.close()

        if not venda:
            return

        janela = self.janela_formulario(
            f"Editar venda #{id_venda}",
            altura=430
        )

        valor = self.campo(
            janela,
            "Valor",
            str(venda[0])
        )

        pagamento = ctk.CTkOptionMenu(
            janela,
            values=[
                "Pix",
                "Dinheiro",
                "Cartao"
            ],
            width=350,
            height=44,
            corner_radius=9,
            fg_color=SURFACE_2,
            button_color=RED,
            button_hover_color=RED_HOVER
        )

        pagamento.pack(
            pady=8
        )

        pagamento.set(
            venda[1]
        )

        def salvar():

            try:

                valor_decimal = Decimal(
                    valor.get().replace(",", ".")
                )

                if valor_decimal <= 0:
                    raise InvalidOperation

            except InvalidOperation:

                messagebox.showwarning(
                    "Atenção",
                    "Digite um valor válido."
                )

                return

            conn = conectar()

            if conn is None:
                return

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    UPDATE vendas
                    SET
                        valor = %s,
                        pagamento = %s
                    WHERE id = %s
                    """,
                    (
                        valor_decimal,
                        pagamento.get(),
                        id_venda
                    )
                )

                conn.commit()

                janela.destroy()

                self.mostrar_vendas()

            except Exception as erro:

                conn.rollback()

                messagebox.showerror(
                    "Erro",
                    str(erro)
                )

            finally:

                cursor.close()
                conn.close()

        self.botao_salvar(
            janela,
            "Salvar alterações",
            salvar
        )

    # ========================================================
    # EXCLUIR VENDA
    # ========================================================

    def excluir_venda(
        self,
        id_venda
    ):

        if self.cargo != "admin":
            return

        if not messagebox.askyesno(
            "Excluir venda",
            f"Deseja excluir a venda #{id_venda}?"
        ):
            return

        conn = conectar()

        if conn is None:
            return

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                DELETE FROM vendas
                WHERE id = %s
                """,
                (id_venda,)
            )

            conn.commit()

            self.mostrar_vendas()

        except Exception as erro:

            conn.rollback()

            messagebox.showerror(
                "Erro",
                str(erro)
            )

        finally:

            cursor.close()
            conn.close()

    # ========================================================
    # USUÁRIOS
    # ========================================================

    def mostrar_usuarios(self):

        if self.cargo != "admin":
            return

        self.ativar_menu(
            "Usuários"
        )

        self.pagina(
            "Usuários",
            "Controle quem possui acesso ao Belo Sabor."
        )

        topo = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent"
        )

        topo.pack(
            fill="x",
            pady=(0, 15)
        )

        ctk.CTkButton(
            topo,
            text="+  Novo usuário",
            width=145,
            height=44,
            corner_radius=9,
            fg_color=RED,
            hover_color=RED_HOVER,
            command=self.abrir_cadastro_usuario
        ).pack(
            side="right"
        )

        self.usuarios_area = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent"
        )

        self.usuarios_area.pack(
            fill="x"
        )

        self.carregar_usuarios()

    # ========================================================
    # CARREGAR USUÁRIOS
    # ========================================================

    def carregar_usuarios(self):

        for widget in self.usuarios_area.winfo_children():
            widget.destroy()

        conn = conectar()

        if conn is None:
            return

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT id, nome, usuario, cargo
                FROM usuarios
                ORDER BY id DESC
                """
            )

            usuarios = cursor.fetchall()

        finally:

            cursor.close()
            conn.close()

        tabela = ctk.CTkFrame(
            self.usuarios_area,
            fg_color=SURFACE,
            corner_radius=14,
            border_width=1,
            border_color=BORDER
        )

        tabela.pack(
            fill="x"
        )

        header = ctk.CTkFrame(
            tabela,
            height=48,
            fg_color=SURFACE_2
        )

        header.pack(
            fill="x"
        )

        pesos = [1, 4, 3, 2]
        self.configurar_colunas_tabela(header, pesos)

        for i, texto in enumerate([
            "ID",
            "NOME",
            "USUÁRIO",
            "CARGO"
        ]):

            ctk.CTkLabel(
                header,
                text=texto,
                text_color=MUTED,
                font=("Arial", 10, "bold"),
                anchor="center"
            ).grid(
                row=0,
                column=i,
                sticky="ew",
                padx=10,
                pady=12
            )

        for usuario in usuarios:

            linha = ctk.CTkFrame(
                tabela,
                height=60,
                fg_color="transparent"
            )

            linha.pack(
                fill="x",
                padx=8,
                pady=2
            )

            self.configurar_colunas_tabela(linha, pesos)

            valores = [
                f"#{usuario[0]}",
                usuario[1],
                usuario[2],
                usuario[3].upper()
            ]

            for i, valor in enumerate(valores):

                ctk.CTkLabel(
                    linha,
                    text=valor,
                    text_color=(
                        RED
                        if i == 3
                        else WHITE
                    ),
                    font=(
                        "Arial",
                        11,
                        "bold"
                        if i == 3
                        else "normal"
                    ),
                    anchor="center"
                ).grid(
                    row=0,
                    column=i,
                    sticky="ew",
                    padx=10,
                    pady=8
                )

        if not usuarios:

            ctk.CTkLabel(
                tabela,
                text="Nenhum usuário cadastrado.",
                text_color=MUTED,
                font=("Arial", 13)
            ).pack(
                pady=35
            )

    # ========================================================
    # NOVO USUÁRIO
    # ========================================================

    def abrir_cadastro_usuario(self):

        janela = self.janela_formulario(
            "Novo usuário",
            altura=560
        )

        nome = self.campo(
            janela,
            "Nome completo"
        )

        usuario = self.campo(
            janela,
            "Usuário"
        )

        senha = self.campo(
            janela,
            "Senha",
            mostrar="*"
        )

        cargo = ctk.CTkOptionMenu(
            janela,
            values=[
                "vendedor",
                "admin"
            ],
            width=350,
            height=44,
            corner_radius=9,
            fg_color=SURFACE_2,
            button_color=RED,
            button_hover_color=RED_HOVER
        )

        cargo.pack(
            pady=8
        )

        def salvar():

            if not nome.get().strip():

                messagebox.showwarning(
                    "Atenção",
                    "Informe o nome."
                )

                return

            if not usuario.get().strip():

                messagebox.showwarning(
                    "Atenção",
                    "Informe o usuário."
                )

                return

            if not senha.get().strip():

                messagebox.showwarning(
                    "Atenção",
                    "Informe a senha."
                )

                return

            conn = conectar()

            if conn is None:
                return

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    INSERT INTO usuarios
                    (
                        nome,
                        usuario,
                        senha,
                        cargo
                    )
                    VALUES
                    (%s, %s, %s, %s)
                    """,
                    (
                        nome.get().strip(),
                        usuario.get().strip(),
                        gerar_hash(
                            senha.get()
                        ),
                        cargo.get()
                    )
                )

                conn.commit()

                janela.destroy()

                self.mostrar_usuarios()

                messagebox.showinfo(
                    "Sucesso",
                    "Usuário criado."
                )

            except Exception as erro:

                conn.rollback()

                messagebox.showerror(
                    "Erro",
                    str(erro)
                )

            finally:

                cursor.close()
                conn.close()

        self.botao_salvar(
            janela,
            "Criar usuário",
            salvar
        )

    # ========================================================
    # JANELA PADRÃO
    # ========================================================

    def janela_formulario(
        self,
        titulo,
        altura=470
    ):

        janela = ctk.CTkToplevel(
            self
        )

        janela.title(
            f"Belo Sabor | {titulo}"
        )

        janela.geometry(
            f"500x{altura}"
        )

        janela.configure(
            fg_color=SIDEBAR
        )

        janela.resizable(
            False,
            False
        )

        janela.grab_set()

        ctk.CTkLabel(
            janela,
            text=titulo,
            text_color=WHITE,
            font=("Arial", 25, "bold")
        ).pack(
            pady=(35, 25)
        )

        return janela

    # ========================================================
    # CAMPO
    # ========================================================

    def campo(
        self,
        parent,
        placeholder,
        valor=None,
        mostrar=None
    ):

        entrada = ctk.CTkEntry(
            parent,
            width=350,
            height=44,
            corner_radius=9,
            fg_color=SURFACE,
            border_color=BORDER,
            placeholder_text=placeholder,
            show=mostrar if mostrar else None
        )

        entrada.pack(
            pady=8
        )

        if valor is not None:

            entrada.insert(
                0,
                str(valor)
            )

        return entrada

    # ========================================================
    # BOTÃO SALVAR
    # ========================================================

    def botao_salvar(
        self,
        janela,
        texto,
        comando
    ):

        ctk.CTkButton(
            janela,
            text=texto,
            width=350,
            height=46,
            corner_radius=9,
            fg_color=RED,
            hover_color=RED_HOVER,
            font=("Arial", 13, "bold"),
            command=comando
        ).pack(
            pady=25
        )

    # ========================================================
    # SAIR
    # ========================================================

    def sair(self):

        if messagebox.askyesno(
            "Sair",
            "Deseja realmente sair?"
        ):

            self.usuario_logado = None
            self.cargo = None
            self.nav_buttons = {}

            self.mostrar_login()


# ============================================================
# EXECUTAR
# ============================================================

if __name__ == "__main__":

    app = BeloSaborApp()

    app.mainloop()