import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os
import customtkinter as ctk

# configuracoes de tema
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# paleta de cores
COR_FUNDO = "#F6F5FA"
COR_BRANCO = "#FFFFFF"
COR_CARD = "#FFFFFF"
COR_CARD_SECUNDARIO = "#F0ECF8"
COR_BORDA = "#DCD5EC"

COR_ROXO = "#5B3CC4"
COR_ROXO_HOVER = "#492EAA"
COR_LILAS = "#8E70E5"
COR_LILAS_HOVER = "#795BD4"
COR_LILAS_CLARO = "#EBE5FA"
COR_LILAS_TEXTO = "#4A2DA8"

COR_TEXTO = "#1F1B2C"
COR_TEXTO_SECUNDARIO = "#6E6882"
COR_TEXTO_MUTED = "#9690A8"

COR_VERDE = "#1F844F"
COR_VERDE_HOVER = "#186B3F"
COR_VERDE_BG = "#E8F6EE"
COR_VERDE_TEXTO = "#145934"

COR_VERMELHO = "#C5303E"
COR_VERMELHO_HOVER = "#A72532"
COR_VERMELHO_BG = "#FCEBEB"
COR_VERMELHO_TEXTO = "#8F1E29"

# categorias
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

# formatacao de datas e valores
def data_atual():
    return datetime.now().strftime("%d/%m/%Y")

def mes_atual():
    return datetime.now().strftime("%m/%Y")

def formatar_moeda(valor):
    texto = f"R$ {valor:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")

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

def formatar_mes(mes):
    data = datetime.strptime(mes, "%m/%Y")
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    return f"{meses[data.month - 1]} de {data.year}"

def calcular_variacao(atual, anterior):
    if anterior == 0:
        if atual == 0:
            return "Sem alteração"
        return "Não é possível calcular porcentagem"

    variacao = ((atual - anterior) / anterior) * 100

    if variacao > 0:
        return f"+{variacao:.1f}%"
    if variacao < 0:
        return f"{variacao:.1f}%"
    return "0.0%"

# salvar dados no json
def salvar_dados():
    dados = {
        "nome": nome_usuario,
        "gastos": gastos,
        "receitas": receitas
    }
    try:
        with open(arquivo_json, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
    except Exception as erro:
        messagebox.showerror(
            "Erro",
            f"Não foi possível salvar os dados:\n{erro}",
            parent=janelagastos
        )

# carregar dados do json
def carregar_dados():
    global gastos, receitas, nome_usuario
    if not os.path.exists(arquivo_json):
        return

    try:
        with open(arquivo_json, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        nome_usuario = dados.get("nome", "")
        gastos = dados.get("gastos", [])
        receitas = dados.get("receitas", [])
    except Exception as erro:
        messagebox.showerror(
            "Erro",
            f"Não foi possível carregar os dados:\n{erro}",
            parent=janelagastos
        )
        gastos = []
        receitas = []
        nome_usuario = ""

# filtrar registros do mes atual
def gastos_visiveis():
    resultado = []
    for indice, gasto in enumerate(gastos):
        if gasto.get("fixo", False):
            resultado.append((indice, gasto))
        else:
            data_gasto = gasto.get("data", "")
            if data_gasto.endswith(mes_atual()):
                resultado.append((indice, gasto))

    return sorted(resultado, key=lambda item: not item[1].get("fixo", False))

def receitas_visiveis():
    resultado = []
    for indice, receita in enumerate(receitas):
        if receita.get("fixo", False):
            resultado.append((indice, receita))
        else:
            data_receita = receita.get("data", "")
            if data_receita.endswith(mes_atual()):
                resultado.append((indice, receita))

    return sorted(resultado, key=lambda item: not item[1].get("fixo", False))

# calcular totais do mes
def calcular_gastos_mes(mes):
    total = 0.0
    for gasto in gastos:
        if gasto.get("fixo", False):
            total += gasto.get("valor", 0.0)
        else:
            data = gasto.get("data", "")
            if data.endswith(mes):
                total += gasto.get("valor", 0.0)
    return total

def calcular_receitas_mes(mes):
    total = 0.0
    for receita in receitas:
        if receita.get("fixo", False):
            total += receita.get("valor", 0.0)
        else:
            data = receita.get("data", "")
            if data.endswith(mes):
                total += receita.get("valor", 0.0)
    return total

# atualizar totais nos cards
def atualizar_totais():
    total_gastos = sum(gasto["valor"] for _, gasto in gastos_visiveis())
    total_receitas = sum(receita["valor"] for _, receita in receitas_visiveis())
    saldo = total_receitas - total_gastos

    label_total_gastos.configure(text=formatar_moeda(total_gastos))
    label_total_receitas.configure(text=formatar_moeda(total_receitas))
    label_saldo.configure(text=formatar_moeda(saldo))

    if saldo >= 0:
        label_saldo.configure(text_color=COR_VERDE)
        tag_saldo.configure(
            text="POSITIVO",
            fg_color=COR_VERDE_BG,
            text_color=COR_VERDE_TEXTO
        )
    else:
        label_saldo.configure(text_color=COR_VERMELHO)
        tag_saldo.configure(
            text="NEGATIVO",
            fg_color=COR_VERMELHO_BG,
            text_color=COR_VERMELHO_TEXTO
        )

# listar gastos
def listar_gastos():
    for widget in scroll_gastos.winfo_children():
        widget.destroy()

    itens = gastos_visiveis()
    label_qtd_gastos.configure(text=f"{len(itens)} REGISTROS")

    if not itens:
        empty = ctk.CTkFrame(scroll_gastos, fg_color="transparent")
        empty.pack(fill="both", expand=True, pady=40)

        ctk.CTkLabel(
            empty,
            text="Nenhum gasto registrado este mês.",
            font=("Segoe UI", 12),
            text_color=COR_TEXTO_MUTED
        ).pack()
        return

    for indice_real, gasto in itens:
        criar_linha_item(
            parent=scroll_gastos,
            indice_real=indice_real,
            item=gasto,
            tipo="gasto"
        )

# listar receitas
def listar_receitas():
    for widget in scroll_receitas.winfo_children():
        widget.destroy()

    itens = receitas_visiveis()
    label_qtd_receitas.configure(text=f"{len(itens)} REGISTROS")

    if not itens:
        empty = ctk.CTkFrame(scroll_receitas, fg_color="transparent")
        empty.pack(fill="both", expand=True, pady=40)

        ctk.CTkLabel(
            empty,
            text="Nenhuma receita registrada este mês.",
            font=("Segoe UI", 12),
            text_color=COR_TEXTO_MUTED
        ).pack()
        return

    for indice_real, receita in itens:
        criar_linha_item(
            parent=scroll_receitas,
            indice_real=indice_real,
            item=receita,
            tipo="receita"
        )

# criar linha da lista
def criar_linha_item(parent, indice_real, item, tipo):
    is_gasto = (tipo == "gasto")
    categoria = item.get("categoria", "Outros")
    is_fixo = item.get("fixo", False)
    valor = item.get("valor", 0.0)

    card = ctk.CTkFrame(
        parent,
        fg_color=COR_BRANCO,
        corner_radius=0,
        border_width=1,
        border_color=COR_BORDA
    )
    card.pack(fill="x", pady=3, padx=2)

    inner = ctk.CTkFrame(card, fg_color="transparent")
    inner.pack(fill="x", padx=12, pady=8)

    left_side = ctk.CTkFrame(inner, fg_color="transparent")
    left_side.pack(side="left", fill="y")

    if is_fixo:
        tag_tipo = ctk.CTkLabel(
            left_side,
            text="FIXO",
            font=("Segoe UI", 9, "bold"),
            fg_color=COR_LILAS_CLARO,
            text_color=COR_LILAS_TEXTO,
            corner_radius=0,
            padx=7,
            pady=2
        )
        tag_tipo.pack(side="left", padx=(0, 10))
    else:
        tag_data = ctk.CTkLabel(
            left_side,
            text=item.get("data", ""),
            font=("Segoe UI", 10),
            fg_color=COR_CARD_SECUNDARIO,
            text_color=COR_TEXTO_SECUNDARIO,
            corner_radius=0,
            padx=7,
            pady=2
        )
        tag_data.pack(side="left", padx=(0, 10))

    ctk.CTkLabel(
        left_side,
        text=categoria,
        font=("Segoe UI", 12, "bold"),
        text_color=COR_TEXTO
    ).pack(side="left")

    right_side = ctk.CTkFrame(inner, fg_color="transparent")
    right_side.pack(side="right")

    cor_valor = COR_VERMELHO if is_gasto else COR_VERDE
    ctk.CTkLabel(
        right_side,
        text=formatar_moeda(valor),
        font=("Segoe UI", 12, "bold"),
        text_color=cor_valor
    ).pack(side="left", padx=(0, 12))

    btn_editar = ctk.CTkButton(
        right_side,
        text="Editar",
        width=50,
        height=26,
        corner_radius=0,
        fg_color=COR_CARD_SECUNDARIO,
        hover_color=COR_LILAS_CLARO,
        text_color=COR_ROXO,
        font=("Segoe UI", 11, "bold"),
        command=lambda: acao_editar_item(is_gasto, is_fixo, item, indice_real)
    )
    btn_editar.pack(side="left", padx=(0, 4))

    btn_excluir = ctk.CTkButton(
        right_side,
        text="Excluir",
        width=50,
        height=26,
        corner_radius=0,
        fg_color=COR_VERMELHO_BG,
        hover_color=COR_VERMELHO_HOVER,
        text_color=COR_VERMELHO_TEXTO,
        font=("Segoe UI", 11, "bold"),
        command=lambda: acao_excluir_item(is_gasto, item, indice_real)
    )
    btn_excluir.pack(side="left")

# acoes para editar e excluir
def acao_editar_item(is_gasto, is_fixo, item, indice_real):
    if is_gasto:
        abrir_janela_gasto(is_fixo, item, indice_real)
    else:
        abrir_janela_receita(is_fixo, item, indice_real)

def acao_excluir_item(is_gasto, item, indice_real):
    tipo_nome = "o gasto" if is_gasto else "a receita"
    confirmacao = messagebox.askyesno(
        "Confirmar exclusão",
        f"Deseja excluir {tipo_nome} de {formatar_moeda(item['valor'])} ({item['categoria']})?",
        parent=janelagastos
    )
    if not confirmacao:
        return

    if is_gasto:
        gastos.pop(indice_real)
        salvar_dados()
        listar_gastos()
    else:
        receitas.pop(indice_real)
        salvar_dados()
        listar_receitas()

    atualizar_totais()

# janela de gasto
def abrir_janela_gasto(gasto_fixo, gasto_editar=None, indice=None):
    new_window = ctk.CTkToplevel(janelagastos)
    new_window.geometry("420x360")
    new_window.resizable(False, False)
    new_window.configure(fg_color=COR_FUNDO)

    titulo_texto = "Editar Gasto" if gasto_editar else ("Adicionar Gasto Fixo" if gasto_fixo else "Adicionar Gasto")
    new_window.title(titulo_texto)
    new_window.grab_set()

    modal_frame = ctk.CTkFrame(
        new_window,
        fg_color=COR_BRANCO,
        corner_radius=0,
        border_width=1,
        border_color=COR_BORDA
    )
    modal_frame.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(
        modal_frame,
        text=titulo_texto.upper(),
        font=("Segoe UI", 14, "bold"),
        text_color=COR_ROXO
    ).pack(pady=(22, 16), padx=25, anchor="center")

    ctk.CTkLabel(
        modal_frame,
        text="VALOR (R$)",
        font=("Segoe UI", 10, "bold"),
        text_color=COR_TEXTO_SECUNDARIO
    ).pack(anchor="w", padx=30)

    entry_gasto = ctk.CTkEntry(
        modal_frame,
        placeholder_text="0,00",
        height=36,
        corner_radius=0,
        fg_color=COR_BRANCO,
        border_color=COR_BORDA,
        text_color=COR_TEXTO,
        font=("Segoe UI", 12)
    )
    entry_gasto.pack(fill="x", padx=30, pady=(4, 14))

    ctk.CTkLabel(
        modal_frame,
        text="CATEGORIA",
        font=("Segoe UI", 10, "bold"),
        text_color=COR_TEXTO_SECUNDARIO
    ).pack(anchor="w", padx=30)

    categorias_var = tk.StringVar()
    entry_categoria = ctk.CTkComboBox(
        modal_frame,
        variable=categorias_var,
        values=categorias_gastos,
        height=36,
        corner_radius=0,
        state="readonly",
        fg_color=COR_BRANCO,
        border_color=COR_BORDA,
        button_color=COR_ROXO,
        button_hover_color=COR_ROXO_HOVER,
        text_color=COR_TEXTO,
        font=("Segoe UI", 12)
    )
    entry_categoria.pack(fill="x", padx=30, pady=(4, 22))

    if gasto_editar is not None:
        entry_gasto.insert(0, str(gasto_editar["valor"]).replace(".", ","))
        entry_categoria.set(gasto_editar["categoria"])
    else:
        entry_categoria.set(categorias_gastos[0])

    def salvar():
        valor = entry_gasto.get().strip().replace(",", ".")
        categoria = entry_categoria.get().strip()

        if not valor or not categoria:
            messagebox.showerror("Erro", "Preencha todos os campos.", parent=new_window)
            return

        try:
            valor_float = float(valor)
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido.", parent=new_window)
            return

        if valor_float <= 0:
            messagebox.showerror("Erro", "Digite um valor positivo.", parent=new_window)
            return

        if gasto_editar is not None:
            gastos[indice]["valor"] = valor_float
            gastos[indice]["categoria"] = categoria
            mensagem = "Gasto atualizado com sucesso."
        else:
            novo_gasto = {
                "valor": valor_float,
                "categoria": categoria,
                "fixo": gasto_fixo
            }
            if not gasto_fixo:
                novo_gasto["data"] = data_atual()
            gastos.append(novo_gasto)
            mensagem = "Gasto adicionado com sucesso."

        salvar_dados()
        listar_gastos()
        atualizar_totais()
        messagebox.showinfo("Sucesso", mensagem, parent=new_window)
        new_window.destroy()

    btn_row = ctk.CTkFrame(modal_frame, fg_color="transparent")
    btn_row.pack(fill="x", padx=30, pady=(0, 15))

    ctk.CTkButton(
        btn_row,
        text="Cancelar",
        command=new_window.destroy,
        width=90,
        height=34,
        corner_radius=0,
        fg_color=COR_CARD_SECUNDARIO,
        hover_color=COR_LILAS_CLARO,
        text_color=COR_TEXTO,
        font=("Segoe UI", 11, "bold")
    ).pack(side="left")

    ctk.CTkButton(
        btn_row,
        text="Salvar",
        command=salvar,
        height=34,
        corner_radius=0,
        fg_color=COR_ROXO,
        hover_color=COR_ROXO_HOVER,
        text_color=COR_BRANCO,
        font=("Segoe UI", 11, "bold")
    ).pack(side="right", fill="x", expand=True, padx=(10, 0))

# funcao para criar gasto
def criar_gasto():
    abrir_janela_gasto(False)

# funcao para criar gasto fixo
def criar_gasto_fixo():
    abrir_janela_gasto(True)

# janela de receita
def abrir_janela_receita(receita_fixa, receita_editar=None, indice=None):
    new_window = ctk.CTkToplevel(janelagastos)
    new_window.geometry("420x360")
    new_window.resizable(False, False)
    new_window.configure(fg_color=COR_FUNDO)

    titulo_texto = "Editar Receita" if receita_editar else ("Adicionar Receita Fixa" if receita_fixa else "Adicionar Receita")
    new_window.title(titulo_texto)
    new_window.grab_set()

    modal_frame = ctk.CTkFrame(
        new_window,
        fg_color=COR_BRANCO,
        corner_radius=0,
        border_width=1,
        border_color=COR_BORDA
    )
    modal_frame.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(
        modal_frame,
        text=titulo_texto.upper(),
        font=("Segoe UI", 14, "bold"),
        text_color=COR_ROXO
    ).pack(pady=(22, 16), padx=25, anchor="center")

    ctk.CTkLabel(
        modal_frame,
        text="VALOR (R$)",
        font=("Segoe UI", 10, "bold"),
        text_color=COR_TEXTO_SECUNDARIO
    ).pack(anchor="w", padx=30)

    entry_receita = ctk.CTkEntry(
        modal_frame,
        placeholder_text="0,00",
        height=36,
        corner_radius=0,
        fg_color=COR_BRANCO,
        border_color=COR_BORDA,
        text_color=COR_TEXTO,
        font=("Segoe UI", 12)
    )
    entry_receita.pack(fill="x", padx=30, pady=(4, 14))

    ctk.CTkLabel(
        modal_frame,
        text="CATEGORIA",
        font=("Segoe UI", 10, "bold"),
        text_color=COR_TEXTO_SECUNDARIO
    ).pack(anchor="w", padx=30)

    categorias_var = tk.StringVar()
    entry_categoria = ctk.CTkComboBox(
        modal_frame,
        variable=categorias_var,
        values=categorias_receitas,
        height=36,
        corner_radius=0,
        state="readonly",
        fg_color=COR_BRANCO,
        border_color=COR_BORDA,
        button_color=COR_ROXO,
        button_hover_color=COR_ROXO_HOVER,
        text_color=COR_TEXTO,
        font=("Segoe UI", 12)
    )
    entry_categoria.pack(fill="x", padx=30, pady=(4, 22))

    if receita_editar is not None:
        entry_receita.insert(0, str(receita_editar["valor"]).replace(".", ","))
        entry_categoria.set(receita_editar["categoria"])
    else:
        entry_categoria.set(categorias_receitas[0])

    def salvar():
        valor = entry_receita.get().strip().replace(",", ".")
        categoria = entry_categoria.get().strip()

        if not valor or not categoria:
            messagebox.showerror("Erro", "Preencha todos os campos.", parent=new_window)
            return

        try:
            valor_float = float(valor)
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido.", parent=new_window)
            return

        if valor_float <= 0:
            messagebox.showerror("Erro", "Digite um valor positivo.", parent=new_window)
            return

        if receita_editar is not None:
            receitas[indice]["valor"] = valor_float
            receitas[indice]["categoria"] = categoria
            mensagem = "Receita atualizada com sucesso."
        else:
            nova_receita = {
                "valor": valor_float,
                "categoria": categoria,
                "fixo": receita_fixa
            }
            if not receita_fixa:
                nova_receita["data"] = data_atual()
            receitas.append(nova_receita)
            mensagem = "Receita adicionada com sucesso."

        salvar_dados()
        listar_receitas()
        atualizar_totais()
        messagebox.showinfo("Sucesso", mensagem, parent=new_window)
        new_window.destroy()

    btn_row = ctk.CTkFrame(modal_frame, fg_color="transparent")
    btn_row.pack(fill="x", padx=30, pady=(0, 15))

    ctk.CTkButton(
        btn_row,
        text="Cancelar",
        command=new_window.destroy,
        width=90,
        height=34,
        corner_radius=0,
        fg_color=COR_CARD_SECUNDARIO,
        hover_color=COR_LILAS_CLARO,
        text_color=COR_TEXTO,
        font=("Segoe UI", 11, "bold")
    ).pack(side="left")

    ctk.CTkButton(
        btn_row,
        text="Salvar",
        command=salvar,
        height=34,
        corner_radius=0,
        fg_color=COR_ROXO,
        hover_color=COR_ROXO_HOVER,
        text_color=COR_BRANCO,
        font=("Segoe UI", 11, "bold")
    ).pack(side="right", fill="x", expand=True, padx=(10, 0))

# funcao para criar receita
def criar_receita():
    abrir_janela_receita(False)

# funcao para criar receita fixa
def criar_receita_fixa():
    abrir_janela_receita(True)

# janela de relatorio
def abrir_relatorio():
    janela_relatorio = ctk.CTkToplevel(janelagastos)
    janela_relatorio.title("Relatório Financeiro")
    janela_relatorio.geometry("840x640")
    janela_relatorio.configure(fg_color=COR_FUNDO)
    janela_relatorio.grab_set()

    # faixa superior do relatorio
    faixa_relatorio = ctk.CTkFrame(
        janela_relatorio,
        fg_color=COR_ROXO,
        corner_radius=0,
        height=65
    )
    faixa_relatorio.pack(fill="x")

    ctk.CTkLabel(
        faixa_relatorio,
        text="RELATÓRIO FINANCEIRO CONSOLIDADO",
        font=("Segoe UI", 14, "bold"),
        text_color=COR_BRANCO
    ).pack(pady=(14, 2))

    ctk.CTkLabel(
        faixa_relatorio,
        text="Histórico consolidado por mês de referência",
        font=("Segoe UI", 10),
        text_color=COR_LILAS_CLARO
    ).pack(pady=(0, 14))

    frame_tabela = ctk.CTkFrame(
        janela_relatorio,
        fg_color=COR_BRANCO,
        corner_radius=0,
        border_width=1,
        border_color=COR_BORDA
    )
    frame_tabela.pack(fill="both", expand=True, padx=25, pady=(15, 10))

    estilo = ttk.Style()
    estilo.theme_use("clam")

    estilo.configure(
        "Treeview",
        background=COR_BRANCO,
        foreground=COR_TEXTO,
        fieldbackground=COR_BRANCO,
        rowheight=30,
        font=("Segoe UI", 10)
    )

    estilo.configure(
        "Treeview.Heading",
        background=COR_CARD_SECUNDARIO,
        foreground=COR_ROXO,
        font=("Segoe UI", 10, "bold"),
        relief="flat"
    )

    estilo.map(
        "Treeview",
        background=[("selected", COR_LILAS_CLARO)],
        foreground=[("selected", COR_ROXO)]
    )

    tabela = ttk.Treeview(
        frame_tabela,
        columns=("mes", "gastos", "receitas", "saldo"),
        show="headings"
    )

    tabela.heading("mes", text="Mês")
    tabela.heading("gastos", text="Gastos")
    tabela.heading("receitas", text="Receitas")
    tabela.heading("saldo", text="Saldo")

    tabela.column("mes", width=200, anchor="center")
    tabela.column("gastos", width=150, anchor="center")
    tabela.column("receitas", width=150, anchor="center")
    tabela.column("saldo", width=150, anchor="center")

    tabela.pack(fill="both", expand=True, padx=10, pady=10)

    meses = obter_meses()
    gastos_meses = []

    for mes in meses:
        total_gastos = calcular_gastos_mes(mes)
        total_receitas = calcular_receitas_mes(mes)
        saldo = total_receitas - total_gastos

        gastos_meses.append((mes, total_gastos))

        tabela.insert(
            "",
            tk.END,
            values=(
                formatar_mes(mes),
                formatar_moeda(total_gastos),
                formatar_moeda(total_receitas),
                formatar_moeda(saldo)
            )
        )

    frame_comparacao = ctk.CTkFrame(
        janela_relatorio,
        fg_color=COR_BRANCO,
        corner_radius=0,
        border_width=1,
        border_color=COR_BORDA
    )
    frame_comparacao.pack(fill="x", padx=25, pady=(0, 15))

    ctk.CTkLabel(
        frame_comparacao,
        text="VARIAÇÃO DE GASTOS ENTRE MESES",
        font=("Segoe UI", 10, "bold"),
        text_color=COR_TEXTO_SECUNDARIO
    ).pack(pady=(12, 6))

    if len(gastos_meses) < 2:
        ctk.CTkLabel(
            frame_comparacao,
            text="Dados insuficientes para calcular variação (mínimo de 2 meses).",
            font=("Segoe UI", 11),
            text_color=COR_TEXTO_MUTED
        ).pack(pady=(0, 12))
    else:
        for i in range(len(gastos_meses) - 1):
            m_atual = gastos_meses[i]
            m_anterior = gastos_meses[i + 1]
            variacao = calcular_variacao(m_atual[1], m_anterior[1])

            linha_comp = ctk.CTkFrame(frame_comparacao, fg_color="transparent")
            linha_comp.pack(pady=(0, 6))

            ctk.CTkLabel(
                linha_comp,
                text=f"{formatar_mes(m_atual[0])}  vs  {formatar_mes(m_anterior[0])}:",
                font=("Segoe UI", 11),
                text_color=COR_TEXTO
            ).pack(side="left")

            is_aumento = "+" in variacao
            bg_tag = COR_VERMELHO_BG if is_aumento else COR_VERDE_BG
            txt_tag = COR_VERMELHO_TEXTO if is_aumento else COR_VERDE_TEXTO
            if "Sem alteração" in variacao or "Não é" in variacao or "0.0%" in variacao:
                bg_tag = COR_CARD_SECUNDARIO
                txt_tag = COR_TEXTO_SECUNDARIO

            ctk.CTkLabel(
                linha_comp,
                text=variacao,
                font=("Segoe UI", 10, "bold"),
                fg_color=bg_tag,
                text_color=txt_tag,
                corner_radius=0,
                padx=6,
                pady=1
            ).pack(side="left", padx=8)

    ctk.CTkButton(
        janela_relatorio,
        text="Fechar",
        command=janela_relatorio.destroy,
        width=120,
        height=32,
        corner_radius=0,
        fg_color=COR_ROXO,
        hover_color=COR_ROXO_HOVER,
        font=("Segoe UI", 11, "bold")
    ).pack(pady=(0, 15))

# login e identificacao
def criar_nome_usuario():
    global nome_usuario
    nome = entry_nome.get().strip()
    if not nome:
        label_nome_msg.configure(
            text="Digite um nome válido para continuar.",
            text_color=COR_VERMELHO
        )
        return

    nome_usuario = nome
    salvar_dados()
    mostrar_interface()

def mostrar_interface():
    label_subtitulo.configure(text=f"USUÁRIO: {nome_usuario.upper()}  |  HOJE: {data_atual()}")
    frame_login.pack_forget()

    frame_principal.pack(fill="both", expand=True, padx=40, pady=(15, 20))
    listar_gastos()
    listar_receitas()
    atualizar_totais()

def iniciar_programa():
    if nome_usuario:
        mostrar_interface()
    else:
        frame_login.pack(pady=60)

# janela principal
janelagastos = ctk.CTk()
janelagastos.geometry("1100x780")
janelagastos.minsize(960, 680)
janelagastos.title("Controle Financeiro")
janelagastos.configure(fg_color=COR_FUNDO)

# faixa atras do titulo
faixa_titulo = ctk.CTkFrame(
    janelagastos,
    fg_color=COR_ROXO,
    corner_radius=0,
    height=80
)
faixa_titulo.pack(fill="x")

label_titulo = ctk.CTkLabel(
    faixa_titulo,
    text="CONTROLE FINANCEIRO",
    font=("Segoe UI", 20, "bold"),
    text_color=COR_BRANCO
)
label_titulo.pack(pady=(16, 2))

label_subtitulo = ctk.CTkLabel(
    faixa_titulo,
    text=f"PAINEL DE GESTÃO  |  {data_atual()}",
    font=("Segoe UI", 10, "bold"),
    text_color=COR_LILAS_CLARO
)
label_subtitulo.pack(pady=(0, 16))

# identificacao do usuario
frame_login = ctk.CTkFrame(
    janelagastos,
    fg_color=COR_BRANCO,
    corner_radius=0,
    border_width=1,
    border_color=COR_BORDA
)

ctk.CTkLabel(
    frame_login,
    text="IDENTIFICAÇÃO",
    font=("Segoe UI", 14, "bold"),
    text_color=COR_ROXO
).pack(pady=(30, 4), padx=60)

label_nome_msg = ctk.CTkLabel(
    frame_login,
    text="Informe seu nome para acessar o painel:",
    font=("Segoe UI", 11),
    text_color=COR_TEXTO_SECUNDARIO
)
label_nome_msg.pack(pady=(0, 15))

entry_nome = ctk.CTkEntry(
    frame_login,
    placeholder_text="Nome",
    width=260,
    height=36,
    corner_radius=0,
    fg_color=COR_BRANCO,
    border_color=COR_BORDA,
    text_color=COR_TEXTO,
    font=("Segoe UI", 12)
)
entry_nome.pack(pady=10)

ctk.CTkButton(
    frame_login,
    text="Entrar",
    command=criar_nome_usuario,
    width=140,
    height=34,
    corner_radius=0,
    fg_color=COR_ROXO,
    hover_color=COR_ROXO_HOVER,
    font=("Segoe UI", 11, "bold")
).pack(pady=(10, 30))

# painel principal
frame_principal = ctk.CTkFrame(janelagastos, fg_color="transparent")

# cards de resumo centralizados
frame_resumo = ctk.CTkFrame(frame_principal, fg_color="transparent")
frame_resumo.pack(fill="x", pady=(0, 15))

# card gastos
card_gastos = ctk.CTkFrame(
    frame_resumo,
    fg_color=COR_BRANCO,
    corner_radius=0,
    border_width=1,
    border_color=COR_BORDA
)
card_gastos.pack(side="left", fill="both", expand=True, padx=(0, 6))

ctk.CTkLabel(
    card_gastos,
    text="GASTOS DO MÊS",
    font=("Segoe UI", 10, "bold"),
    text_color=COR_TEXTO_SECUNDARIO
).pack(pady=(16, 2))

label_total_gastos = ctk.CTkLabel(
    card_gastos,
    text="R$ 0,00",
    font=("Segoe UI", 22, "bold"),
    text_color=COR_VERMELHO
)
label_total_gastos.pack(pady=(0, 16))

# card receitas
card_receitas = ctk.CTkFrame(
    frame_resumo,
    fg_color=COR_BRANCO,
    corner_radius=0,
    border_width=1,
    border_color=COR_BORDA
)
card_receitas.pack(side="left", fill="both", expand=True, padx=6)

ctk.CTkLabel(
    card_receitas,
    text="RECEITAS DO MÊS",
    font=("Segoe UI", 10, "bold"),
    text_color=COR_TEXTO_SECUNDARIO
).pack(pady=(16, 2))

label_total_receitas = ctk.CTkLabel(
    card_receitas,
    text="R$ 0,00",
    font=("Segoe UI", 22, "bold"),
    text_color=COR_VERDE
)
label_total_receitas.pack(pady=(0, 16))

# card saldo
card_saldo = ctk.CTkFrame(
    frame_resumo,
    fg_color=COR_BRANCO,
    corner_radius=0,
    border_width=1,
    border_color=COR_BORDA
)
card_saldo.pack(side="left", fill="both", expand=True, padx=(6, 0))

top_saldo = ctk.CTkFrame(card_saldo, fg_color="transparent")
top_saldo.pack(pady=(14, 2))

ctk.CTkLabel(
    top_saldo,
    text="SALDO ATUAL",
    font=("Segoe UI", 10, "bold"),
    text_color=COR_TEXTO_SECUNDARIO
).pack(side="left", padx=(0, 6))

tag_saldo = ctk.CTkLabel(
    top_saldo,
    text="NEUTRO",
    font=("Segoe UI", 9, "bold"),
    fg_color=COR_CARD_SECUNDARIO,
    text_color=COR_TEXTO_SECUNDARIO,
    corner_radius=0,
    padx=5,
    pady=1
)
tag_saldo.pack(side="left")

label_saldo = ctk.CTkLabel(
    card_saldo,
    text="R$ 0,00",
    font=("Segoe UI", 22, "bold"),
    text_color=COR_VERDE
)
label_saldo.pack(pady=(0, 14))

# duas colunas principais
frame_colunas = ctk.CTkFrame(frame_principal, fg_color="transparent")
frame_colunas.pack(fill="both", expand=True)

# coluna de gastos
coluna_gastos = ctk.CTkFrame(
    frame_colunas,
    fg_color=COR_BRANCO,
    corner_radius=0,
    border_width=1,
    border_color=COR_BORDA
)
coluna_gastos.pack(side="left", fill="both", expand=True, padx=(0, 6))

header_col_gastos = ctk.CTkFrame(coluna_gastos, fg_color="transparent")
header_col_gastos.pack(fill="x", padx=16, pady=(12, 6))

ctk.CTkLabel(
    header_col_gastos,
    text="GASTOS",
    font=("Segoe UI", 13, "bold"),
    text_color=COR_ROXO
).pack(side="left")

label_qtd_gastos = ctk.CTkLabel(
    header_col_gastos,
    text="0 REGISTROS",
    font=("Segoe UI", 9, "bold"),
    fg_color=COR_CARD_SECUNDARIO,
    text_color=COR_TEXTO_SECUNDARIO,
    corner_radius=0,
    padx=6,
    pady=2
)
label_qtd_gastos.pack(side="right")

scroll_gastos = ctk.CTkScrollableFrame(
    coluna_gastos,
    fg_color="transparent",
    corner_radius=0,
    scrollbar_button_color=COR_BORDA,
    scrollbar_button_hover_color=COR_LILAS
)
scroll_gastos.pack(fill="both", expand=True, padx=10, pady=4)

botoes_gastos_frame = ctk.CTkFrame(coluna_gastos, fg_color="transparent")
botoes_gastos_frame.pack(fill="x", padx=12, pady=12)

ctk.CTkButton(
    botoes_gastos_frame,
    text="+ Novo Gasto",
    command=criar_gasto,
    height=34,
    corner_radius=0,
    fg_color=COR_ROXO,
    hover_color=COR_ROXO_HOVER,
    font=("Segoe UI", 11, "bold")
).pack(side="left", fill="x", expand=True, padx=(0, 4))

ctk.CTkButton(
    botoes_gastos_frame,
    text="+ Gasto Fixo",
    command=criar_gasto_fixo,
    height=34,
    corner_radius=0,
    fg_color=COR_CARD_SECUNDARIO,
    hover_color=COR_LILAS_CLARO,
    text_color=COR_ROXO,
    font=("Segoe UI", 11, "bold")
).pack(side="left", fill="x", expand=True, padx=(4, 0))

# coluna de receitas
coluna_receitas = ctk.CTkFrame(
    frame_colunas,
    fg_color=COR_BRANCO,
    corner_radius=0,
    border_width=1,
    border_color=COR_BORDA
)
coluna_receitas.pack(side="left", fill="both", expand=True, padx=(6, 0))

header_col_receitas = ctk.CTkFrame(coluna_receitas, fg_color="transparent")
header_col_receitas.pack(fill="x", padx=16, pady=(12, 6))

ctk.CTkLabel(
    header_col_receitas,
    text="RECEITAS",
    font=("Segoe UI", 13, "bold"),
    text_color=COR_ROXO
).pack(side="left")

label_qtd_receitas = ctk.CTkLabel(
    header_col_receitas,
    text="0 REGISTROS",
    font=("Segoe UI", 9, "bold"),
    fg_color=COR_CARD_SECUNDARIO,
    text_color=COR_TEXTO_SECUNDARIO,
    corner_radius=0,
    padx=6,
    pady=2
)
label_qtd_receitas.pack(side="right")

scroll_receitas = ctk.CTkScrollableFrame(
    coluna_receitas,
    fg_color="transparent",
    corner_radius=0,
    scrollbar_button_color=COR_BORDA,
    scrollbar_button_hover_color=COR_LILAS
)
scroll_receitas.pack(fill="both", expand=True, padx=10, pady=4)

botoes_receitas_frame = ctk.CTkFrame(coluna_receitas, fg_color="transparent")
botoes_receitas_frame.pack(fill="x", padx=12, pady=12)

ctk.CTkButton(
    botoes_receitas_frame,
    text="+ Nova Receita",
    command=criar_receita,
    height=34,
    corner_radius=0,
    fg_color=COR_VERDE,
    hover_color=COR_VERDE_HOVER,
    font=("Segoe UI", 11, "bold")
).pack(side="left", fill="x", expand=True, padx=(0, 4))

ctk.CTkButton(
    botoes_receitas_frame,
    text="+ Receita Fixa",
    command=criar_receita_fixa,
    height=34,
    corner_radius=0,
    fg_color=COR_VERDE_BG,
    hover_color=COR_CARD_SECUNDARIO,
    text_color=COR_VERDE_TEXTO,
    font=("Segoe UI", 11, "bold")
).pack(side="left", fill="x", expand=True, padx=(4, 0))

# botao de relatorio
botao_relatorio = ctk.CTkButton(
    frame_principal,
    text="Relatório Financeiro Consolidado",
    command=abrir_relatorio,
    height=36,
    corner_radius=0,
    font=("Segoe UI", 11, "bold"),
    fg_color=COR_ROXO,
    hover_color=COR_ROXO_HOVER
)
botao_relatorio.pack(fill="x", pady=(12, 0))

# iniciar programa
carregar_dados()
iniciar_programa()
janelagastos.mainloop()