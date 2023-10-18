import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkcalendar import DateEntry

def limitar_rg(event):
    if len(event.widget.get()) > 15:
        event.widget.delete(12, tk.END)

def limitar_cpf(event):
    if len(event.widget.get()) > 15:
        event.widget.delete(12, tk.END)

def cadastrar_cliente():
    # Obter os valores dos campos
    nome = entry_nome.get()
    sobrenome = entry_sobrenome.get()
    rg = entry_rg.get()
    cpf = entry_cpf.get()
    data_nascimento = entry_data_nascimento.get()
    telefone = entry_telefone.get()

    # Validar se os campos obrigatórios foram preenchidos
    if nome and sobrenome and cpf and data_nascimento:
        # Lógica para inserir os dados em sua tabela (conexão com o banco de dados será adicionada posteriormente)
        # Por enquanto, apenas imprima os valores
        print("Nome:", nome)
        print("Sobrenome:", sobrenome)
        print("RG:", rg)
        print("CPF:", cpf)
        print("Data de Nascimento:", data_nascimento)
        print("Telefone:", telefone)

        # Limpar os campos após o cadastro
        entry_nome.delete(0, tk.END)
        entry_sobrenome.delete(0, tk.END)
        entry_rg.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
        entry_data_nascimento.set("")  # Limpar a data
        entry_telefone.delete(0, tk.END)
    else:
        # Exibir uma mensagem de erro se os campos obrigatórios não estiverem preenchidos
        tk.messagebox.showerror("Erro", "Preencha os campos obrigatórios: Nome, Sobrenome, CPF e Data de Nascimento")

janela_cadastro = ThemedTk(theme="clam")
janela_cadastro.title("Cadastro de Clientes")

frame = ttk.Frame(janela_cadastro)
frame.grid(row=0, column=0, padx=1, pady=1)

# Campos de entrada
label_nome = ttk.Label(frame, text="Nome:")
label_nome.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_nome = ttk.Entry(frame)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

label_sobrenome = ttk.Label(frame, text="Sobrenome:")
label_sobrenome.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_sobrenome = ttk.Entry(frame)
entry_sobrenome.grid(row=1, column=1, padx=5, pady=5)

label_data_nascimento = ttk.Label(frame, text="Data de Nascimento:")
label_data_nascimento.grid(row=4, column=0, padx=5, pady=5, sticky="w")
entry_data_nascimento = DateEntry(frame)
entry_data_nascimento.grid(row=4, column=1, padx=5, pady=5)

label_rg = ttk.Label(frame, text="Registro Geral (RG):")
label_rg.grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_rg = ttk.Entry(frame)
entry_rg.grid(row=2, column=1, padx=5, pady=5)

label_cpf = ttk.Label(frame, text="Cadastro de Pessoa Fisica (CPF):")
label_cpf.grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_cpf = ttk.Entry(frame)
entry_cpf.grid(row=3, column=1, padx=5, pady=5)

# Limitar o RG e o CPF a 12 dígitos
entry_rg.bind("<KeyRelease>", limitar_rg)
entry_cpf.bind("<KeyRelease>", limitar_cpf)

# Repita esse processo para os outros campos (Telefone)

# Botão de cadastro
botao_cadastrar = ttk.Button(frame, text="Cadastrar", command=cadastrar_cliente)
botao_cadastrar.grid(row=6, column=1, padx=5, pady=10)

janela_cadastro.mainloop()
