import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os
import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

COR_FUNDO = "#D9D3ED"

COR_CARD = "#F0F1F8"
COR_CARD_SECUNDARIO = "#F0EFFF"
COR_CARD_BRANCO = "#F9F9FD"

COR_ROXA = "#7161E5"
COR_ROXA_HOVER = "#5B4BC4"

COR_ROXA_CLARO = "#DAD6FA"
COR_ROXA_MUITO_CLARO = "#E9E6FF"

COR_VERDE = "#62B88A"
COR_VERDE_HOVER = "#4D9D73"

COR_VERMELHO = "#E56B72"
COR_VERMELHO_HOVER = "#CC5159"

COR_AMARELO = "#F2B84B"
COR_AMARELO_HOVER = "#D99E32"

COR_CINZA = "#E2E3EA"
COR_CINZA_HOVER = "#D2D3DC"

COR_TEXTO = "#434449"
COR_TEXTO_SECUNDARIO = "#737580"

COR_BRANCO = "#FFFFFF"

categorias_gastos = [
    "Alimentação",
    "Transporte",
    "Moradia",
    "Saúde",
    "Educação",
    "Lazer",
    "Outros"
]

categorias_receitas = [
    "Salário",
    "Freelance",
    "Investimentos",
    "Presentes",
    "Outros"
]

arquivo_json = "dados.json"

receitas = []
gastos = []
nome_usuario = ""

def data_atual():
    return datetime.now().strftime("%d/%m/%Y")


def mes_atual():
    return datetime.now().strftime("%m/%Y")

def obter_meses():

    meses = set()

    for gasto in gastos:

        if not gasto.get("fixo", False):

            data = gasto.get("data", "")

            if data:
                meses.add(data[-7:])

    for receita in receitas:

        if not receita.get("fixo", False):

            data = receita.get("data", "")

            if data:
                meses.add(data[-7:])

    meses.add(mes_atual())

    return sorted(
        meses,
        key=lambda x: datetime.strptime(x, "%m/%Y"),
        reverse=True
    )

def salvar_dados():

    dados = {
        "nome": nome_usuario,
        "gastos": gastos,
        "receitas": receitas
    }

    try:

        with open(
            arquivo_json,
            "w",
            encoding="utf-8"
        ) as arquivo:

            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    except Exception as erro:

        messagebox.showerror(
            "Erro",
            f"Não foi possível salvar os dados:\n{erro}",
            parent=janelagastos
        )

def carregar_dados():

    global gastos
    global receitas
    global nome_usuario

    if not os.path.exists(arquivo_json):
        return

    try:

        with open(
            arquivo_json,
            "r",
            encoding="utf-8"
        ) as arquivo:

            dados = json.load(arquivo)

        nome_usuario = dados.get(
            "nome",
            ""
        )

        gastos = dados.get(
            "gastos",
            []
        )

        receitas = dados.get(
            "receitas",
            []
        )

    except Exception as erro:

        messagebox.showerror(
            "Erro",
            f"Não foi possível carregar os dados:\n{erro}",
            parent=janelagastos
        )

        gastos = []
        receitas = []
        nome_usuario = ""

def iniciar_programa():

    if nome_usuario:

        mostrar_interface()

    else:

        label_nome.configure(
            text="Digite seu nome",
            font=("Century Gothic", 25, "bold"),
            text_color=COR_TEXTO
        )

        entry_nome.pack(
            pady=(30, 70)
        )

        botao_confirmar.pack(
            pady=15
        )


# ==========================================================
# MOSTRAR INTERFACE
# ==========================================================

def mostrar_interface():

    label_nome.configure(
        text=f"Olá, {nome_usuario}! 👋",
        text_color=COR_ROXA
    )

    entry_nome.pack_forget()
    botao_confirmar.pack_forget()

    frame_principal.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=10
    )

    listar_gastos()
    listar_receitas()
    atualizar_totais()


# ==========================================================
# CRIAR USUÁRIO
# ==========================================================

def criar_nome_usuario():

    global nome_usuario

    nome = entry_nome.get().strip()

    if not nome:

        label_nome.configure(
            text="Por favor, digite um nome válido.",
            text_color=COR_VERMELHO
        )

        return

    nome_usuario = nome

    salvar_dados()

    mostrar_interface()


# ==========================================================
# GASTOS
# ==========================================================

def criar_gasto():

    abrir_janela_gasto(False)


def criar_gasto_fixo():

    abrir_janela_gasto(True)


# ==========================================================
# JANELA DE GASTO
# ==========================================================

def abrir_janela_gasto(
    gasto_fixo,
    gasto_editar=None,
    indice=None
):

    new_window = ctk.CTkToplevel(
        janelagastos
    )

    new_window.geometry(
        "500x450"
    )

    new_window.resizable(
        False,
        False
    )

    new_window.configure(
        fg_color=COR_FUNDO
    )

    if gasto_editar is None:

        if gasto_fixo:
            titulo_texto = "Adicionar Gasto Fixo"
        else:
            titulo_texto = "Adicionar Gasto"

    else:

        titulo_texto = "Editar Gasto"

    new_window.title(
        titulo_texto
    )

    new_window.grab_set()

    # TÍTULO

    ctk.CTkLabel(
        new_window,
        text=titulo_texto,
        font=("Arial", 22, "bold"),
        text_color=COR_ROXA
    ).pack(
        pady=(30, 25)
    )

    # VALOR

    ctk.CTkLabel(
        new_window,
        text="Valor do gasto",
        font=("Arial", 14),
        text_color=COR_TEXTO
    ).pack(
        anchor="w",
        padx=50
    )

    entry_gasto = ctk.CTkEntry(
        new_window,
        placeholder_text="Ex: 150,00",
        width=400,
        height=40,
        corner_radius=10,
        fg_color=COR_BRANCO,
        border_color=COR_ROXA_CLARO,
        text_color=COR_TEXTO
    )

    entry_gasto.pack(
        pady=(5, 20)
    )

    # CATEGORIA

    ctk.CTkLabel(
        new_window,
        text="Categoria",
        font=("Arial", 14),
        text_color=COR_TEXTO
    ).pack(
        anchor="w",
        padx=50
    )

    categorias_var = tk.StringVar()

    entry_categoria = ctk.CTkComboBox(
        new_window,
        variable=categorias_var,
        values=categorias_gastos,
        width=400,
        height=40,
        corner_radius=10,
        state="readonly",
        fg_color=COR_BRANCO,
        border_color=COR_ROXA,
        button_color=COR_ROXA,
        button_hover_color=COR_ROXA_HOVER,
        text_color=COR_TEXTO
    )

    entry_categoria.pack(
        pady=(5, 20)
    )

    # PREENCHER AO EDITAR

    if gasto_editar is not None:

        entry_gasto.insert(
            0,
            str(gasto_editar["valor"])
        )

        entry_categoria.set(
            gasto_editar["categoria"]
        )

    # SALVAR

    def salvar():

        valor = (
            entry_gasto
            .get()
            .strip()
            .replace(",", ".")
        )

        categoria = (
            entry_categoria
            .get()
            .strip()
        )

        if not valor or not categoria:

            messagebox.showerror(
                "Erro",
                "Por favor, preencha todos os campos.",
                parent=new_window
            )

            return

        try:

            valor_float = float(valor)

        except ValueError:

            messagebox.showerror(
                "Erro",
                "Digite um valor numérico válido.",
                parent=new_window
            )

            return

        if valor_float <= 0:

            messagebox.showerror(
                "Erro",
                "Digite um valor positivo.",
                parent=new_window
            )

            return

        # EDITAR

        if gasto_editar is not None:

            gastos[indice]["valor"] = valor_float
            gastos[indice]["categoria"] = categoria

            mensagem = "Gasto editado com sucesso!"

        # NOVO

        else:

            novo_gasto = {
                "valor": valor_float,
                "categoria": categoria,
                "fixo": gasto_fixo
            }

            if not gasto_fixo:

                novo_gasto["data"] = data_atual()

            gastos.append(
                novo_gasto
            )

            mensagem = "Gasto adicionado com sucesso!"

        salvar_dados()

        listar_gastos()
        atualizar_totais()

        messagebox.showinfo(
            "Sucesso",
            mensagem,
            parent=new_window
        )

        new_window.destroy()

    ctk.CTkButton(
        new_window,
        text="Salvar",
        command=salvar,
        width=400,
        height=45,
        corner_radius=12,
        font=("Arial", 14, "bold"),
        fg_color=COR_ROXA,
        hover_color=COR_ROXA_HOVER
    ).pack(
        pady=15
    )


# ==========================================================
# GASTOS VISÍVEIS
# ==========================================================

def gastos_visiveis():

    resultado = []

    for indice, gasto in enumerate(gastos):

        if gasto.get("fixo", False):

            resultado.append(
                (indice, gasto)
            )

        else:

            data_gasto = gasto.get(
                "data",
                ""
            )

            if data_gasto.endswith(
                mes_atual()
            ):

                resultado.append(
                    (indice, gasto)
                )

    return sorted(
        resultado,
        key=lambda item:
        not item[1].get("fixo", False)
    )


# ==========================================================
# LISTAR GASTOS
# ==========================================================

def listar_gastos():

    lista_gastos.delete(
        0,
        tk.END
    )

    for indice, gasto in gastos_visiveis():

        if gasto.get("fixo", False):

            texto = (
                f"🔄 FIXO  |  "
                f"R$ {gasto['valor']:.2f}  |  "
                f"{gasto['categoria']}"
            )

        else:

            texto = (
                f"{gasto['data']}  |  "
                f"R$ {gasto['valor']:.2f}  |  "
                f"{gasto['categoria']}"
            )

        lista_gastos.insert(
            tk.END,
            texto
        )


# ==========================================================
# EDITAR GASTO
# ==========================================================

def editar_gasto():

    selecao = lista_gastos.curselection()

    if not selecao:

        messagebox.showwarning(
            "Aviso",
            "Selecione um gasto para editar.",
            parent=janelagastos
        )

        return

    posicao = selecao[0]

    lista = gastos_visiveis()

    indice_real, gasto = lista[posicao]

    abrir_janela_gasto(
        gasto.get("fixo", False),
        gasto,
        indice_real
    )


# ==========================================================
# EXCLUIR GASTO
# ==========================================================

def excluir_gasto():

    selecao = lista_gastos.curselection()

    if not selecao:

        messagebox.showwarning(
            "Aviso",
            "Selecione um gasto para excluir.",
            parent=janelagastos
        )

        return

    posicao = selecao[0]

    lista = gastos_visiveis()

    indice_real, gasto = lista[posicao]

    confirmacao = messagebox.askyesno(
        "Confirmar exclusão",
        f"Deseja excluir o gasto de R$ {gasto['valor']:.2f}?",
        parent=janelagastos
    )

    if not confirmacao:
        return

    gastos.pop(
        indice_real
    )

    salvar_dados()

    listar_gastos()
    atualizar_totais()


# ==========================================================
# RECEITAS
# ==========================================================

def criar_receita():

    abrir_janela_receita(False)


def criar_receita_fixa():

    abrir_janela_receita(True)


# ==========================================================
# JANELA DE RECEITA
# ==========================================================

def abrir_janela_receita(
    receita_fixa,
    receita_editar=None,
    indice=None
):

    new_window = ctk.CTkToplevel(
        janelagastos
    )

    new_window.geometry(
        "500x450"
    )

    new_window.resizable(
        False,
        False
    )

    new_window.configure(
        fg_color=COR_FUNDO
    )

    if receita_editar is None:

        if receita_fixa:
            titulo_texto = "Adicionar Receita Fixa"
        else:
            titulo_texto = "Adicionar Receita"

    else:

        titulo_texto = "Editar Receita"

    new_window.title(
        titulo_texto
    )

    new_window.grab_set()

    # TÍTULO

    ctk.CTkLabel(
        new_window,
        text=titulo_texto,
        font=("Arial", 22, "bold"),
        text_color=COR_ROXA
    ).pack(
        pady=(30, 25)
    )

    # VALOR

    ctk.CTkLabel(
        new_window,
        text="Valor da receita",
        font=("Arial", 14),
        text_color=COR_TEXTO
    ).pack(
        anchor="w",
        padx=50
    )

    entry_receita = ctk.CTkEntry(
        new_window,
        placeholder_text="Ex: 2500,00",
        width=400,
        height=40,
        corner_radius=10,
        fg_color=COR_BRANCO,
        border_color=COR_ROXA_CLARO,
        text_color=COR_TEXTO
    )

    entry_receita.pack(
        pady=(5, 20)
    )

    # CATEGORIA

    ctk.CTkLabel(
        new_window,
        text="Categoria",
        font=("Arial", 14),
        text_color=COR_TEXTO
    ).pack(
        anchor="w",
        padx=50
    )

    categorias_var = tk.StringVar()

    entry_categoria = ctk.CTkComboBox(
        new_window,
        variable=categorias_var,
        values=categorias_receitas,
        width=400,
        height=40,
        corner_radius=10,
        state="readonly",
        fg_color=COR_BRANCO,
        border_color=COR_ROXA,
        button_color=COR_ROXA,
        button_hover_color=COR_ROXA_HOVER,
        text_color=COR_TEXTO
    )

    entry_categoria.pack(
        pady=(5, 20)
    )

    # PREENCHER AO EDITAR

    if receita_editar is not None:

        entry_receita.insert(
            0,
            str(receita_editar["valor"])
        )

        entry_categoria.set(
            receita_editar["categoria"]
        )

    # SALVAR

    def salvar():

        valor = (
            entry_receita
            .get()
            .strip()
            .replace(",", ".")
        )

        categoria = (
            entry_categoria
            .get()
            .strip()
        )

        if not valor or not categoria:

            messagebox.showerror(
                "Erro",
                "Por favor, preencha todos os campos.",
                parent=new_window
            )

            return

        try:

            valor_float = float(valor)

        except ValueError:

            messagebox.showerror(
                "Erro",
                "Digite um valor numérico válido.",
                parent=new_window
            )

            return

        if valor_float <= 0:

            messagebox.showerror(
                "Erro",
                "Digite um valor positivo.",
                parent=new_window
            )

            return

        # EDITAR

        if receita_editar is not None:

            receitas[indice]["valor"] = valor_float
            receitas[indice]["categoria"] = categoria

            mensagem = "Receita editada com sucesso!"

        # NOVA

        else:

            nova_receita = {
                "valor": valor_float,
                "categoria": categoria,
                "fixo": receita_fixa
            }

            if not receita_fixa:

                nova_receita["data"] = data_atual()

            receitas.append(
                nova_receita
            )

            mensagem = "Receita adicionada com sucesso!"

        salvar_dados()

        listar_receitas()
        atualizar_totais()

        messagebox.showinfo(
            "Sucesso",
            mensagem,
            parent=new_window
        )

        new_window.destroy()

    ctk.CTkButton(
        new_window,
        text="Salvar",
        command=salvar,
        width=400,
        height=45,
        corner_radius=12,
        font=("Arial", 14, "bold"),
        fg_color=COR_ROXA,
        hover_color=COR_ROXA_HOVER
    ).pack(
        pady=15
    )


# ==========================================================
# RECEITAS VISÍVEIS
# ==========================================================

def receitas_visiveis():

    resultado = []

    for indice, receita in enumerate(receitas):

        if receita.get("fixo", False):

            resultado.append(
                (indice, receita)
            )

        else:

            data_receita = receita.get(
                "data",
                ""
            )

            if data_receita.endswith(
                mes_atual()
            ):

                resultado.append(
                    (indice, receita)
                )

    return sorted(
        resultado,
        key=lambda item:
        not item[1].get("fixo", False)
    )


# ==========================================================
# LISTAR RECEITAS
# ==========================================================

def listar_receitas():

    lista_receitas.delete(
        0,
        tk.END
    )

    for indice, receita in receitas_visiveis():

        if receita.get("fixo", False):

            texto = (
                f"🔄 FIXO  |  "
                f"R$ {receita['valor']:.2f}  |  "
                f"{receita['categoria']}"
            )

        else:

            texto = (
                f"{receita['data']}  |  "
                f"R$ {receita['valor']:.2f}  |  "
                f"{receita['categoria']}"
            )

        lista_receitas.insert(
            tk.END,
            texto
        )


# ==========================================================
# EDITAR RECEITA
# ==========================================================

def editar_receita():

    selecao = lista_receitas.curselection()

    if not selecao:

        messagebox.showwarning(
            "Aviso",
            "Selecione uma receita para editar.",
            parent=janelagastos
        )

        return

    posicao = selecao[0]

    lista = receitas_visiveis()

    indice_real, receita = lista[posicao]

    abrir_janela_receita(
        receita.get("fixo", False),
        receita,
        indice_real
    )


# ==========================================================
# EXCLUIR RECEITA
# ==========================================================

def excluir_receita():

    selecao = lista_receitas.curselection()

    if not selecao:

        messagebox.showwarning(
            "Aviso",
            "Selecione uma receita para excluir.",
            parent=janelagastos
        )

        return

    posicao = selecao[0]

    lista = receitas_visiveis()

    indice_real, receita = lista[posicao]

    confirmacao = messagebox.askyesno(
        "Confirmar exclusão",
        f"Deseja excluir a receita de R$ {receita['valor']:.2f}?",
        parent=janelagastos
    )

    if not confirmacao:
        return

    receitas.pop(
        indice_real
    )

    salvar_dados()

    listar_receitas()
    atualizar_totais()


# ==========================================================
# CÁLCULO DE GASTOS
# ==========================================================

def calcular_gastos_mes(mes):

    total = 0

    for gasto in gastos:

        if gasto.get("fixo", False):

            total += gasto["valor"]

        else:

            data = gasto.get(
                "data",
                ""
            )

            if data.endswith(mes):

                total += gasto["valor"]

    return total


# ==========================================================
# CÁLCULO DE RECEITAS
# ==========================================================

def calcular_receitas_mes(mes):

    total = 0

    for receita in receitas:

        if receita.get("fixo", False):

            total += receita["valor"]

        else:

            data = receita.get(
                "data",
                ""
            )

            if data.endswith(mes):

                total += receita["valor"]

    return total


# ==========================================================
# FORMATAR MÊS
# ==========================================================

def formatar_mes(mes):

    data = datetime.strptime(
        mes,
        "%m/%Y"
    )

    meses = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro"
    ]

    return (
        f"{meses[data.month - 1]} "
        f"de {data.year}"
    )


# ==========================================================
# VARIAÇÃO
# ==========================================================

def calcular_variacao(
    atual,
    anterior
):

    if anterior == 0:

        if atual == 0:

            return "Sem alteração"

        return "Não é possível calcular a porcentagem"

    variacao = (
        (atual - anterior)
        / anterior
    ) * 100

    if variacao > 0:

        return f"Aumento de {variacao:.2f}%"

    if variacao < 0:

        return f"Diminuição de {abs(variacao):.2f}%"

    return "Sem alteração"


# ==========================================================
# RELATÓRIO
# ==========================================================

def abrir_relatorio():

    janela_relatorio = ctk.CTkToplevel(
        janelagastos
    )

    janela_relatorio.title(
        "Relatório Financeiro"
    )

    janela_relatorio.geometry(
        "900x700"
    )

    janela_relatorio.configure(
        fg_color=COR_FUNDO
    )

    janela_relatorio.grab_set()

    # TÍTULO

    ctk.CTkLabel(
        janela_relatorio,
        text="RELATÓRIO FINANCEIRO",
        font=("Arial", 24, "bold"),
        text_color=COR_ROXA
    ).pack(
        pady=20
    )

    # FRAME DA TABELA

    frame_tabela = ctk.CTkFrame(
        janela_relatorio,
        fg_color=COR_CARD,
        corner_radius=20
    )

    frame_tabela.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    # ESTILO TREEVIEW

    estilo = ttk.Style()

    estilo.theme_use(
        "clam"
    )

    estilo.configure(
        "Treeview",
        background=COR_CARD_BRANCO,
        foreground=COR_TEXTO,
        fieldbackground=COR_CARD_BRANCO,
        rowheight=35,
        font=("Arial", 10)
    )

    estilo.configure(
        "Treeview.Heading",
        background=COR_ROXA,
        foreground="white",
        font=("Arial", 10, "bold")
    )

    estilo.map(
        "Treeview",
        background=[
            ("selected", COR_ROXA_CLARO)
        ],
        foreground=[
            ("selected", COR_TEXTO)
        ]
    )

    tabela = ttk.Treeview(
        frame_tabela,
        columns=(
            "mes",
            "gastos",
            "receitas",
            "saldo"
        ),
        show="headings"
    )

    tabela.heading(
        "mes",
        text="Mês"
    )

    tabela.heading(
        "gastos",
        text="Gastos"
    )

    tabela.heading(
        "receitas",
        text="Receitas"
    )

    tabela.heading(
        "saldo",
        text="Saldo"
    )

    tabela.column(
        "mes",
        width=220
    )

    tabela.column(
        "gastos",
        width=150
    )

    tabela.column(
        "receitas",
        width=150
    )

    tabela.column(
        "saldo",
        width=150
    )

    tabela.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # MESES

    meses = obter_meses()

    gastos_meses = []

    for mes in meses:

        total_gastos = calcular_gastos_mes(
            mes
        )

        total_receitas = calcular_receitas_mes(
            mes
        )

        saldo = (
            total_receitas
            - total_gastos
        )

        gastos_meses.append(
            (
                mes,
                total_gastos
            )
        )

        tabela.insert(
            "",
            tk.END,
            values=(
                formatar_mes(mes),
                f"R$ {total_gastos:.2f}",
                f"R$ {total_receitas:.2f}",
                f"R$ {saldo:.2f}"
            )
        )

    # COMPARAÇÃO

    ctk.CTkLabel(
        janela_relatorio,
        text="Comparação dos gastos",
        font=("Arial", 17, "bold"),
        text_color=COR_ROXA
    ).pack(
        pady=10
    )

    frame_comparacao = ctk.CTkFrame(
        janela_relatorio,
        fg_color=COR_CARD,
        corner_radius=20
    )

    frame_comparacao.pack(
        fill="x",
        padx=30,
        pady=5
    )

    if len(gastos_meses) < 2:

        ctk.CTkLabel(
            frame_comparacao,
            text=(
                "Ainda não existem meses suficientes "
                "para comparar os gastos."
            ),
            text_color=COR_TEXTO_SECUNDARIO
        ).pack(
            pady=15
        )

    else:

        for i in range(
            len(gastos_meses) - 1
        ):

            mes_atual_relatorio = (
                gastos_meses[i]
            )

            mes_anterior_relatorio = (
                gastos_meses[i + 1]
            )

            gasto_atual = (
                mes_atual_relatorio[1]
            )

            gasto_anterior = (
                mes_anterior_relatorio[1]
            )

            variacao = calcular_variacao(
                gasto_atual,
                gasto_anterior
            )

            texto = (
                f"{formatar_mes(mes_atual_relatorio[0])} "
                f"→ "
                f"{formatar_mes(mes_anterior_relatorio[0])}: "
                f"{variacao}"
            )

            ctk.CTkLabel(
                frame_comparacao,
                text=texto,
                font=("Arial", 12),
                text_color=COR_TEXTO
            ).pack(
                anchor="w",
                padx=15,
                pady=5
            )

    # FECHAR

    ctk.CTkButton(
        janela_relatorio,
        text="Fechar",
        command=janela_relatorio.destroy,
        width=200,
        height=40,
        corner_radius=12,
        fg_color=COR_ROXA,
        hover_color=COR_ROXA_HOVER
    ).pack(
        pady=15
    )


# ==========================================================
# ATUALIZAR TOTAIS
# ==========================================================

def atualizar_totais():

    total_gastos = sum(
        gasto["valor"]
        for indice, gasto
        in gastos_visiveis()
    )

    total_receitas = sum(
        receita["valor"]
        for indice, receita
        in receitas_visiveis()
    )

    saldo = (
        total_receitas
        - total_gastos
    )

    # GASTOS

    label_total.configure(
        text=(
            f"R$ {total_gastos:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
    )

    # RECEITAS

    label_total_receitas.configure(
        text=(
            f"R$ {total_receitas:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
    )

    # SALDO

    label_saldo.configure(
        text=(
            f"R$ {saldo:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
    )

    if saldo >= 0:

        label_saldo.configure(
            text_color=COR_VERDE
        )

    else:

        label_saldo.configure(
            text_color=COR_VERMELHO
        )


# ==========================================================
# JANELA PRINCIPAL
# ==========================================================

janelagastos = ctk.CTk()

janelagastos.geometry(
    "1200x800"
)

janelagastos.minsize(
    1000,
    700
)

janelagastos.title(
    "Controle Financeiro"
)

janelagastos.configure(
    fg_color=COR_FUNDO
)


# ==========================================================
# CABEÇALHO
# ==========================================================

frame_cabecalho = ctk.CTkFrame(
    janelagastos,
    fg_color=COR_CARD,
    corner_radius=25
)

frame_cabecalho.pack(
    fill="x",
    padx=55,
    pady=(50, 20)
)


label_titulo = ctk.CTkLabel(
    frame_cabecalho,
    text="CONTROLE FINANCEIRO",
    font=("Gill Sans", 30, "bold"),
    text_color=COR_ROXA
)

label_titulo.pack(
    pady=(20, 5)
)


label_data = ctk.CTkLabel(
    frame_cabecalho,
    text=f"Data: {data_atual()}",
    text_color=COR_TEXTO_SECUNDARIO,
    font=("Arial", 15)
)

label_data.pack(
    pady=(0, 10)
)


label_nome = ctk.CTkLabel(
    frame_cabecalho,
    text="Digite seu nome",
    font=("Arial", 15, "bold"),
    text_color=COR_TEXTO
)

label_nome.pack(
    pady=5
)


entry_nome = ctk.CTkEntry(
    frame_cabecalho,
    placeholder_text="Seu nome",
    width=300,
    height=40,
    corner_radius=10,
    fg_color=COR_BRANCO,
    border_color=COR_ROXA_CLARO,
    text_color=COR_TEXTO
)


botao_confirmar = ctk.CTkButton(
    frame_cabecalho,
    text="Entrar",
    font=("Arial", 17),
    command=criar_nome_usuario,
    width=150,
    height=35,
    corner_radius=10,
    fg_color=COR_ROXA,
    hover_color=COR_ROXA_HOVER
)


# ==========================================================
# INTERFACE PRINCIPAL
# ==========================================================

frame_principal = ctk.CTkFrame(
    janelagastos,
    fg_color="transparent"
)


# ==========================================================
# CARDS DE RESUMO
# ==========================================================

frame_resumo = ctk.CTkFrame(
    frame_principal,
    fg_color="transparent"
)

frame_resumo.pack(
    fill="x",
    pady=(0, 15)
)


# ==========================================================
# CARD GASTOS
# ==========================================================

card_gastos = ctk.CTkFrame(
    frame_resumo,
    fg_color=COR_CARD,
    corner_radius=20
)

card_gastos.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 8)
)


ctk.CTkLabel(
    card_gastos,
    text="💸 Gastos",
    font=("Arial", 15, "bold"),
    text_color=COR_TEXTO
).pack(
    pady=(15, 5)
)


label_total = ctk.CTkLabel(
    card_gastos,
    text="R$ 0,00",
    font=("Arial", 22, "bold"),
    text_color=COR_VERMELHO
)

label_total.pack(
    pady=(0, 15)
)


# ==========================================================
# CARD RECEITAS
# ==========================================================

card_receitas = ctk.CTkFrame(
    frame_resumo,
    fg_color=COR_CARD,
    corner_radius=20
)

card_receitas.pack(
    side="left",
    fill="both",
    expand=True,
    padx=8
)


ctk.CTkLabel(
    card_receitas,
    text="💰 Receitas",
    font=("Arial", 15, "bold"),
    text_color=COR_TEXTO
).pack(
    pady=(15, 5)
)


label_total_receitas = ctk.CTkLabel(
    card_receitas,
    text="R$ 0,00",
    font=("Arial", 22, "bold"),
    text_color=COR_VERDE
)

label_total_receitas.pack(
    pady=(0, 15)
)


# ==========================================================
# CARD SALDO
# ==========================================================

card_saldo = ctk.CTkFrame(
    frame_resumo,
    fg_color=COR_CARD,
    corner_radius=20
)

card_saldo.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(8, 0)
)


ctk.CTkLabel(
    card_saldo,
    text="📊 Saldo",
    font=("Arial", 15, "bold"),
    text_color=COR_TEXTO
).pack(
    pady=(15, 5)
)


label_saldo = ctk.CTkLabel(
    card_saldo,
    text="R$ 0,00",
    font=("Arial", 22, "bold"),
    text_color=COR_VERDE
)

label_saldo.pack(
    pady=(0, 15)
)


# ==========================================================
# DUAS COLUNAS
# ==========================================================

frame_colunas = ctk.CTkFrame(
    frame_principal,
    fg_color="transparent"
)

frame_colunas.pack(
    fill="both",
    expand=True
)


# ==========================================================
# COLUNA DE GASTOS
# ==========================================================

frame_gastos = ctk.CTkFrame(
    frame_colunas,
    fg_color=COR_CARD,
    corner_radius=25
)

frame_gastos.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 8)
)


ctk.CTkLabel(
    frame_gastos,
    text="💸 Gastos do mês",
    font=("Arial", 20, "bold"),
    text_color=COR_ROXA
).pack(
    pady=15
)


lista_gastos = tk.Listbox(
    frame_gastos,
    width=60,
    height=10,
    bg=COR_CARD_BRANCO,
    fg=COR_TEXTO,
    selectbackground=COR_ROXA,
    selectforeground=COR_BRANCO,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    font=("Arial", 11)
)

lista_gastos.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=5
)


# BOTÃO ADICIONAR GASTO

botao_adicionar_gasto = ctk.CTkButton(
    frame_gastos,
    text="➕ Adicionar Gasto",
    command=criar_gasto,
    height=38,
    corner_radius=12,
    fg_color=COR_ROXA,
    hover_color=COR_ROXA_HOVER
)

botao_adicionar_gasto.pack(
    fill="x",
    padx=15,
    pady=4
)


# BOTÃO GASTO FIXO

botao_adicionar_gasto_fixo = ctk.CTkButton(
    frame_gastos,
    text="🔄 Adicionar Gasto Fixo",
    command=criar_gasto_fixo,
    height=38,
    corner_radius=12,
    fg_color=COR_ROXA_CLARO,
    hover_color=COR_ROXA_MUITO_CLARO,
    text_color=COR_ROXA
)

botao_adicionar_gasto_fixo.pack(
    fill="x",
    padx=15,
    pady=4
)


# BOTÃO EDITAR

botao_editar_gasto = ctk.CTkButton(
    frame_gastos,
    text="✏️ Editar Selecionado",
    command=editar_gasto,
    height=38,
    corner_radius=12,
    fg_color=COR_CINZA,
    hover_color=COR_CINZA_HOVER,
    text_color=COR_TEXTO
)

botao_editar_gasto.pack(
    fill="x",
    padx=15,
    pady=4
)


# BOTÃO EXCLUIR

botao_excluir_gasto = ctk.CTkButton(
    frame_gastos,
    text="🗑️ Excluir Selecionado",
    command=excluir_gasto,
    height=38,
    corner_radius=12,
    fg_color=COR_VERMELHO,
    hover_color=COR_VERMELHO_HOVER
)

botao_excluir_gasto.pack(
    fill="x",
    padx=15,
    pady=(4, 15)
)


# ==========================================================
# COLUNA DE RECEITAS
# ==========================================================

frame_receitas = ctk.CTkFrame(
    frame_colunas,
    fg_color=COR_CARD,
    corner_radius=25
)

frame_receitas.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(8, 0)
)


ctk.CTkLabel(
    frame_receitas,
    text="💰 Receitas do mês",
    font=("Arial", 20, "bold"),
    text_color=COR_ROXA
).pack(
    pady=15
)


lista_receitas = tk.Listbox(
    frame_receitas,
    width=60,
    height=10,
    bg=COR_CARD_BRANCO,
    fg=COR_TEXTO,
    selectbackground=COR_ROXA,
    selectforeground=COR_BRANCO,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    font=("Arial", 11)
)

lista_receitas.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=5
)


# BOTÃO ADICIONAR RECEITA

botao_adicionar_receita = ctk.CTkButton(
    frame_receitas,
    text="➕ Adicionar Receita",
    command=criar_receita,
    height=38,
    corner_radius=12,
    fg_color=COR_VERDE,
    hover_color=COR_VERDE_HOVER
)

botao_adicionar_receita.pack(
    fill="x",
    padx=15,
    pady=4
)


# BOTÃO RECEITA FIXA

botao_adicionar_receita_fixa = ctk.CTkButton(
    frame_receitas,
    text="🔄 Adicionar Receita Fixa",
    command=criar_receita_fixa,
    height=38,
    corner_radius=12,
    fg_color=COR_ROXA_CLARO,
    hover_color=COR_ROXA_MUITO_CLARO,
    text_color=COR_ROXA
)

botao_adicionar_receita_fixa.pack(
    fill="x",
    padx=15,
    pady=4
)


# BOTÃO EDITAR

botao_editar_receita = ctk.CTkButton(
    frame_receitas,
    text="✏️ Editar Selecionada",
    command=editar_receita,
    height=38,
    corner_radius=12,
    fg_color=COR_CINZA,
    hover_color=COR_CINZA_HOVER,
    text_color=COR_TEXTO
)

botao_editar_receita.pack(
    fill="x",
    padx=15,
    pady=4
)


# BOTÃO EXCLUIR

botao_excluir_receita = ctk.CTkButton(
    frame_receitas,
    text="🗑️ Excluir Selecionada",
    command=excluir_receita,
    height=38,
    corner_radius=12,
    fg_color=COR_VERMELHO,
    hover_color=COR_VERMELHO_HOVER
)

botao_excluir_receita.pack(
    fill="x",
    padx=15,
    pady=(4, 15)
)


# ==========================================================
# BOTÃO RELATÓRIO
# ==========================================================

botao_relatorio = ctk.CTkButton(
    frame_principal,
    text="Abrir Relatório Financeiro",
    command=abrir_relatorio,
    height=45,
    corner_radius=14,
    font=("Arial", 14, "bold"),
    fg_color=COR_ROXA,
    hover_color=COR_ROXA_HOVER
)

botao_relatorio.pack(
    fill="x",
    pady=(15, 0)
)


# ==========================================================
# INICIAR PROGRAMA
# ==========================================================

carregar_dados()

iniciar_programa()

janelagastos.mainloop()