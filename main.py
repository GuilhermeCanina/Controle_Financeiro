import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

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
        with open(arquivo_json, "w", encoding="utf-8") as arquivo:
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


def iniciar_programa():
    if nome_usuario:
        mostrar_interface()
    else:
        label_nome.config(text="Digite seu nome:")
        entry_nome.pack()
        botao_confirmar.pack(pady=5)


def mostrar_interface():
    label_nome.config(
        text=f"Bem-vindo(a), {nome_usuario}!",
        fg="black"
    )

    entry_nome.pack_forget()
    botao_confirmar.pack_forget()

    botao_adicionar_gasto.pack(pady=5)
    botao_adicionar_gasto_fixo.pack(pady=5)
    botao_editar_gasto.pack(pady=5)
    botao_excluir_gasto.pack(pady=5)

    lista_gastos.pack(pady=5)
    label_total.pack()

    botao_adicionar_receita.pack(pady=5)
    botao_adicionar_receita_fixa.pack(pady=5)
    botao_editar_receita.pack(pady=5)
    botao_excluir_receita.pack(pady=5)

    lista_receitas.pack(pady=5)
    label_total_receitas.pack()
    label_saldo.pack(pady=10)

    botao_relatorio.pack(pady=10)

    listar_gastos()
    listar_receitas()
    atualizar_totais()


def criar_nome_usuario():
    global nome_usuario

    nome = entry_nome.get().strip()

    if not nome:
        label_nome.config(
            text="Por favor, digite um nome válido.",
            fg="red"
        )
        return

    nome_usuario = nome
    salvar_dados()
    mostrar_interface()


def criar_gasto():
    abrir_janela_gasto(False)


def criar_gasto_fixo():
    abrir_janela_gasto(True)


def abrir_janela_gasto(gasto_fixo, gasto_editar=None, indice=None):
    new_window = tk.Toplevel(janelagastos)

    if gasto_editar is None:
        if gasto_fixo:
            new_window.title("Adicionar Gasto Fixo")
        else:
            new_window.title("Adicionar Gasto")
    else:
        new_window.title("Editar Gasto")

    new_window.geometry("600x400")

    tk.Label(new_window, text="Digite o valor do gasto:").pack(pady=5)

    entry_gasto = tk.Entry(new_window)
    entry_gasto.pack()

    tk.Label(new_window, text="Escolha a categoria do gasto:").pack(pady=5)

    categorias_var = tk.StringVar()

    entry_categoria = ttk.Combobox(
        new_window,
        textvariable=categorias_var,
        values=categorias_gastos,
        state="readonly"
    )
    entry_categoria.pack()

    if gasto_editar is not None:
        entry_gasto.insert(0, str(gasto_editar["valor"]))
        entry_categoria.set(gasto_editar["categoria"])

    def salvar():
        valor = entry_gasto.get().strip().replace(",", ".")
        categoria = entry_categoria.get().strip()

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

        if gasto_editar is not None:
            gastos[indice]["valor"] = valor_float
            gastos[indice]["categoria"] = categoria

            salvar_dados()
            listar_gastos()
            atualizar_totais()

            messagebox.showinfo(
                "Sucesso",
                "Gasto editado com sucesso!",
                parent=new_window
            )

        else:
            novo_gasto = {
                "valor": valor_float,
                "categoria": categoria,
                "fixo": gasto_fixo
            }

            if not gasto_fixo:
                novo_gasto["data"] = data_atual()

            gastos.append(novo_gasto)

            salvar_dados()
            listar_gastos()
            atualizar_totais()

            messagebox.showinfo(
                "Sucesso",
                "Gasto adicionado com sucesso!",
                parent=new_window
            )

        new_window.destroy()

    tk.Button(new_window, text="Salvar", command=salvar).pack(pady=15)


def gastos_visiveis():
    resultado = []

    for indice, gasto in enumerate(gastos):
        if gasto.get("fixo", False):
            resultado.append((indice, gasto))
        else:
            data_gasto = gasto.get("data", "")

            if data_gasto.endswith(mes_atual()):
                resultado.append((indice, gasto))

    return sorted(
        resultado,
        key=lambda item: not item[1].get("fixo", False)
    )


def listar_gastos():
    lista_gastos.delete(0, tk.END)
    total = 0

    for indice, gasto in gastos_visiveis():
        if gasto.get("fixo", False):
            texto = (
                f"FIXO — R$ {gasto['valor']:.2f} — "
                f"{gasto['categoria']}"
            )
        else:
            texto = (
                f"{gasto['data']} — R$ {gasto['valor']:.2f} — "
                f"{gasto['categoria']}"
            )

        lista_gastos.insert(tk.END, texto)
        total += gasto["valor"]

    label_total.config(text=f"Total de Gastos: R$ {total:.2f}")


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

    gastos.pop(indice_real)
    salvar_dados()
    listar_gastos()
    atualizar_totais()


def criar_receita():
    abrir_janela_receita(False)


def criar_receita_fixa():
    abrir_janela_receita(True)


def abrir_janela_receita(receita_fixa, receita_editar=None, indice=None):
    new_window = tk.Toplevel(janelagastos)

    if receita_editar is None:
        if receita_fixa:
            new_window.title("Adicionar Receita Fixa")
        else:
            new_window.title("Adicionar Receita")
    else:
        new_window.title("Editar Receita")

    new_window.geometry("600x400")

    tk.Label(new_window, text="Digite o valor da receita:").pack(pady=5)

    entry_receita = tk.Entry(new_window)
    entry_receita.pack()

    tk.Label(new_window, text="Escolha a categoria da receita:").pack(pady=5)

    categorias_var = tk.StringVar()

    entry_categoria = ttk.Combobox(
        new_window,
        textvariable=categorias_var,
        values=categorias_receitas,
        state="readonly"
    )
    entry_categoria.pack()

    if receita_editar is not None:
        entry_receita.insert(0, str(receita_editar["valor"]))
        entry_categoria.set(receita_editar["categoria"])

    def salvar():
        valor = entry_receita.get().strip().replace(",", ".")
        categoria = entry_categoria.get().strip()

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

        if receita_editar is not None:
            receitas[indice]["valor"] = valor_float
            receitas[indice]["categoria"] = categoria

            salvar_dados()
            listar_receitas()
            atualizar_totais()

            messagebox.showinfo(
                "Sucesso",
                "Receita editada com sucesso!",
                parent=new_window
            )

        else:
            nova_receita = {
                "valor": valor_float,
                "categoria": categoria,
                "fixo": receita_fixa
            }

            if not receita_fixa:
                nova_receita["data"] = data_atual()

            receitas.append(nova_receita)

            salvar_dados()
            listar_receitas()
            atualizar_totais()

            messagebox.showinfo(
                "Sucesso",
                "Receita adicionada com sucesso!",
                parent=new_window
            )

        new_window.destroy()

    tk.Button(new_window, text="Salvar", command=salvar).pack(pady=15)


def receitas_visiveis():
    resultado = []

    for indice, receita in enumerate(receitas):
        if receita.get("fixo", False):
            resultado.append((indice, receita))
        else:
            data_receita = receita.get("data", "")

            if data_receita.endswith(mes_atual()):
                resultado.append((indice, receita))

    return sorted(
        resultado,
        key=lambda item: not item[1].get("fixo", False)
    )


def listar_receitas():
    lista_receitas.delete(0, tk.END)
    total = 0

    for indice, receita in receitas_visiveis():
        if receita.get("fixo", False):
            texto = (
                f"FIXO — R$ {receita['valor']:.2f} — "
                f"{receita['categoria']}"
            )
        else:
            texto = (
                f"{receita['data']} — R$ {receita['valor']:.2f} — "
                f"{receita['categoria']}"
            )

        lista_receitas.insert(tk.END, texto)
        total += receita["valor"]

    label_total_receitas.config(
        text=f"Total de Receitas: R$ {total:.2f}"
    )


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

    receitas.pop(indice_real)
    salvar_dados()
    listar_receitas()
    atualizar_totais()


def calcular_gastos_mes(mes):
    total = 0

    for gasto in gastos:
        if gasto.get("fixo", False):
            total += gasto["valor"]
        else:
            data = gasto.get("data", "")

            if data.endswith(mes):
                total += gasto["valor"]

    return total


def calcular_receitas_mes(mes):
    total = 0

    for receita in receitas:
        if receita.get("fixo", False):
            total += receita["valor"]
        else:
            data = receita.get("data", "")

            if data.endswith(mes):
                total += receita["valor"]

    return total


def formatar_mes(mes):
    data = datetime.strptime(mes, "%m/%Y")

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

    return f"{meses[data.month - 1]} de {data.year}"


def calcular_variacao(atual, anterior):
    if anterior == 0:
        if atual == 0:
            return "Sem alteração"

        return "Não é possível calcular a porcentagem"

    variacao = ((atual - anterior) / anterior) * 100

    if variacao > 0:
        return f"Aumento de {variacao:.2f}%"

    if variacao < 0:
        return f"Diminuição de {abs(variacao):.2f}%"

    return "Sem alteração"


def abrir_relatorio():
    janela_relatorio = tk.Toplevel(janelagastos)
    janela_relatorio.title("Relatório Financeiro")
    janela_relatorio.geometry("900x700")

    tk.Label(
        janela_relatorio,
        text="Relatório Financeiro",
        font=("Arial", 18)
    ).pack(pady=10)

    meses = obter_meses()

    frame = tk.Frame(janela_relatorio)
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    tabela = ttk.Treeview(
        frame,
        columns=("mes", "gastos", "receitas", "saldo"),
        show="headings"
    )

    tabela.heading("mes", text="Mês")
    tabela.heading("gastos", text="Gastos")
    tabela.heading("receitas", text="Receitas")
    tabela.heading("saldo", text="Saldo")

    tabela.column("mes", width=200)
    tabela.column("gastos", width=150)
    tabela.column("receitas", width=150)
    tabela.column("saldo", width=150)

    tabela.pack(fill="both", expand=True)

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
                f"R$ {total_gastos:.2f}",
                f"R$ {total_receitas:.2f}",
                f"R$ {saldo:.2f}"
            )
        )

    tk.Label(
        janela_relatorio,
        text="Comparação dos gastos",
        font=("Arial", 14)
    ).pack(pady=10)

    frame_comparacao = tk.Frame(janela_relatorio)
    frame_comparacao.pack(fill="x", padx=30, pady=5)

    if len(gastos_meses) < 2:
        tk.Label(
            frame_comparacao,
            text="Ainda não existem meses suficientes para comparar os gastos."
        ).pack()
    else:
        for i in range(len(gastos_meses) - 1):
            mes_atual_relatorio = gastos_meses[i]
            mes_anterior_relatorio = gastos_meses[i + 1]

            gasto_atual = mes_atual_relatorio[1]
            gasto_anterior = mes_anterior_relatorio[1]

            variacao = calcular_variacao(
                gasto_atual,
                gasto_anterior
            )

            texto = (
                f"{formatar_mes(mes_atual_relatorio[0])} "
                f"comparado com "
                f"{formatar_mes(mes_anterior_relatorio[0])}: "
                f"{variacao}"
            )

            tk.Label(
                frame_comparacao,
                text=texto,
                font=("Arial", 11)
            ).pack(anchor="w", pady=3)

    tk.Button(janela_relatorio, text="Fechar", command=janela_relatorio.destroy).pack(pady=15)


def atualizar_totais():
    total_gastos = sum(
        gasto["valor"]
        for indice, gasto in gastos_visiveis()
    )

    total_receitas = sum(
        receita["valor"]
        for indice, receita in receitas_visiveis()
    )

    saldo = total_receitas - total_gastos

    label_total.config(
        text=f"Total de Gastos: R$ {total_gastos:.2f}"
    )

    label_total_receitas.config(
        text=f"Total de Receitas: R$ {total_receitas:.2f}"
    )

    label_saldo.config(
        text=f"Saldo: R$ {saldo:.2f}"
    )


janelagastos = tk.Tk()
janelagastos.geometry("1200x800")
janelagastos.title("Controle Financeiro")

label_data = tk.Label(
    janelagastos,
    text=f"Data: {data_atual()}",
    font=("Arial", 12)
)
label_data.pack(pady=5)

label_titulo = tk.Label(
    janelagastos,
    text="Controle Financeiro",
    font=("Arial", 16)
)
label_titulo.pack(pady=10)

label_nome = tk.Label(janelagastos, text="Digite seu nome:")
label_nome.pack()

entry_nome = tk.Entry(janelagastos)
botao_confirmar = tk.Button(janelagastos, text="Confirmar", command=criar_nome_usuario)

botao_adicionar_gasto = tk.Button(janelagastos, text="Adicionar Gasto", command=criar_gasto)
botao_adicionar_gasto_fixo = tk.Button(janelagastos, text="Adicionar Gasto Fixo", command=criar_gasto_fixo)
botao_editar_gasto = tk.Button(janelagastos, text="Editar Gasto Selecionado", command=editar_gasto)
botao_excluir_gasto = tk.Button(janelagastos, text="Excluir Gasto Selecionado", command=excluir_gasto)

lista_gastos = tk.Listbox(janelagastos, width=60, height=10)
label_total = tk.Label(janelagastos, text="Total de Gastos: R$ 0,00")

botao_adicionar_receita = tk.Button(janelagastos, text="Adicionar Receita", command=criar_receita)
botao_adicionar_receita_fixa = tk.Button(janelagastos, text="Adicionar Receita Fixa", command=criar_receita_fixa)
botao_editar_receita = tk.Button(janelagastos, text="Editar Receita Selecionada", command=editar_receita)
botao_excluir_receita = tk.Button(janelagastos, text="Excluir Receita Selecionada", command=excluir_receita)

lista_receitas = tk.Listbox(janelagastos, width=60, height=10)
label_total_receitas = tk.Label(janelagastos, text="Total de Receitas: R$ 0,00")
label_saldo = tk.Label(janelagastos, text="Saldo: R$ 0,00")

botao_relatorio = tk.Button(janelagastos, text="Relatório", command=abrir_relatorio)

carregar_dados()
iniciar_programa()

janelagastos.mainloop()