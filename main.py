import tkinter as tk
from tkinter import ttk
import tkinter as messagebox
import tkinter.messagebox as messagebox

categorias_gastos = ["Alimentação", "Transporte", "Moradia", "Saúde", "Educação", "Lazer", "Outros"]
categorias_receitas = ["Salário", "Freelance", "Investimentos", "Presentes", "Outros"]

receitas = []
gastos = []

def criar_nome_usuario():
    nome_usuario = entry_nome.get().strip()

    if not nome_usuario:
        label_nome.config(text="Por favor, digite um nome válido.", fg="red")
        return

    label_nome.config(text=f"Bem-vindo(a), {nome_usuario}!", fg="black")
    entry_nome.pack_forget()
    botao_confirmar.pack_forget()
    botao_adicionar_gasto.pack(pady=10)
    botao_adicionar_receita.pack(pady=10)
    lista_gastos.pack()
    label_total.pack()
    lista_receitas.pack()
    label_total_receitas.pack()
    label_saldo.pack()


def salvar_gasto(valor, categoria, janela):
    valor = valor.strip().replace(',', '.')
    categoria = categoria.strip()

    if not valor or not categoria:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    try:
        valor_float = float(valor)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, digite um valor numérico válido.", parent=janela)
        return

    if valor_float <= 0:
        messagebox.showerror("Erro", "Por favor, digite um valor positivo.", parent=janela)
        return

    messagebox.showinfo("Sucesso", f"Gasto de R${valor_float:.2f} na categoria '{categoria}' adicionado com sucesso!", parent=janela)

    gastos.append({"valor": valor_float, "categoria": categoria})
    listar_gastos()
    atualizar_totais()
    janela.destroy()

def criar_gasto():
    nome_usuario = entry_nome.get()
    if not nome_usuario:
        messagebox.showerror("Erro", "Por favor, digite um nome válido.", parent=janelagastos)
        return

    new_window = tk.Toplevel(janelagastos)
    new_window.title("Adicionar Gasto")
    new_window.geometry("600x400")

    label_gasto = tk.Label(new_window, text="Digite o valor do gasto:")
    label_gasto.pack()
    entry_gasto = tk.Entry(new_window)
    entry_gasto.pack()

    label_categoria = tk.Label(new_window, text="Escolha a categoria do gasto:")
    label_categoria.pack()

    categorias_var = tk.StringVar(value=categorias_gastos[0])

    entry_categoria = ttk.Combobox(new_window, textvariable=categorias_var, values=categorias_gastos, state="readonly")

    entry_categoria.pack()

    botao_salvar = tk.Button(new_window, text="Salvar Gasto", command=lambda: salvar_gasto(entry_gasto.get(), entry_categoria.get(), new_window))
    botao_salvar.pack(pady=10)

def listar_gastos():
    lista_gastos.delete(0, tk.END)
    total = 0

    for gasto in gastos:
        lista_gastos.insert(
            tk.END,
            f"R$ {gasto['valor']:.2f} — {gasto['categoria']}"
        )
        total += gasto["valor"]

    label_total.config(text=f"Total: R$ {total:.2f}")


def criar_receita():
    nome_usuario = entry_nome.get()
    if not nome_usuario:
        messagebox.showerror("Erro", "Por favor, digite um nome válido.", parent=janelagastos)
        return

    new_window = tk.Toplevel(janelagastos)
    new_window.title("Adicionar Receita")
    new_window.geometry("600x400")

    label_receita = tk.Label(new_window, text="Digite o valor da receita:")
    label_receita.pack()
    entry_receita = tk.Entry(new_window)
    entry_receita.pack()

    label_categoria = tk.Label(new_window, text="Escolha a categoria da receita:")
    label_categoria.pack()
    categorias_var = tk.StringVar(value=categorias_receitas[0])
    entry_categoria = ttk.Combobox(new_window, textvariable=categorias_var, values=categorias_receitas, state="readonly")
    entry_categoria.pack()

    botao_salvar = tk.Button(new_window, text="Salvar Receita", command=lambda: salvar_receita(entry_receita.get(), entry_categoria.get(), new_window))
    botao_salvar.pack(pady=10)

def salvar_receita(valor, categoria, janela):
    valor = valor.strip().replace(',', '.')
    categoria = categoria.strip()

    if not valor or not categoria:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    try:
        valor_float = float(valor)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, digite um valor numérico válido.", parent=janela)
        return

    if valor_float <= 0:
        messagebox.showerror("Erro", "Por favor, digite um valor positivo.", parent=janela)
        return

    messagebox.showinfo("Sucesso", f"Receita de R${valor_float:.2f} na categoria '{categoria}' adicionada com sucesso!", parent=janela)

    receitas.append({"valor": valor_float, "categoria": categoria})
    listar_receitas()
    atualizar_totais()
    janela.destroy()


def listar_receitas():
    lista_receitas.delete(0, tk.END)
    total = 0

    for receita in receitas:
        lista_receitas.insert(
            tk.END,
            f"R$ {receita['valor']:.2f} — {receita['categoria']}"
        )
        total += receita["valor"]

    label_total_receitas.config(text=f"Total: R$ {total:.2f}")

def atualizar_totais():
    total_gastos = sum(gasto["valor"] for gasto in gastos)
    total_receitas = sum(receita["valor"] for receita in receitas)
    saldo = total_receitas - total_gastos

    label_total.config(text=f"Total de Gastos: R$ {total_gastos:.2f}")
    label_total_receitas.config(text=f"Total de Receitas: R$ {total_receitas:.2f}")
    label_saldo.config(text=f"Saldo: R$ {saldo:.2f}")

janelagastos = tk.Tk()
janelagastos.geometry("1200x800")

janelagastos.title("Controle Financeiro")

label_nome = tk.Label(janelagastos, text="Digite seu nome:")
label_nome.pack()

entry_nome = tk.Entry(janelagastos)
entry_nome.pack()
botao_confirmar = tk.Button(janelagastos, text="Confirmar", command=criar_nome_usuario)
botao_confirmar.pack()

botao_adicionar_gasto = tk.Button(janelagastos, text="Adicionar Gasto", command=criar_gasto)

botao_adicionar_receita = tk.Button(janelagastos, text="Adicionar Receita", command=criar_receita)

lista_gastos = tk.Listbox(janelagastos, width=45, height=10)

label_total = tk.Label(janelagastos, text="Total: R$ 0,00")

lista_receitas = tk.Listbox(janelagastos, width=45, height=10)

label_total_receitas = tk.Label(janelagastos, text="Total de Receitas: R$ 0,00")

label_saldo = tk.Label(janelagastos, text="Saldo: R$ 0,00")

tk.Label(janelagastos, text="Controle Financeiro", font=("Arial", 16)).pack(pady=10)

janelagastos.mainloop()
