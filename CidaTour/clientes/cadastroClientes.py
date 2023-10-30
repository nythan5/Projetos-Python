from datetime import datetime
import tkinter as tk
from tkinter import ttk
import mysql.connector
from ttkthemes import ThemedTk
from tkcalendar import DateEntry
from tkinter import messagebox
from CidaTour.database import ConexaoBancoDados


class CadastroClientes:
    def __init__(self):
        self.janela_cadastro = ThemedTk(theme="clam")
        self.janela_cadastro.title("Cadastro de Clientes")

        self.frame = ttk.Frame(self.janela_cadastro)
        self.frame.grid(row=0, column=0, padx=1, pady=1)

        # Campos de entrada
        self.label_nome = ttk.Label(self.frame, text="Nome:")
        self.label_nome.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome = ttk.Entry(self.frame)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        self.label_sobrenome = ttk.Label(self.frame, text="Sobrenome:")
        self.label_sobrenome.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_sobrenome = ttk.Entry(self.frame)
        self.entry_sobrenome.grid(row=1, column=1, padx=5, pady=5)

        self.label_rg = ttk.Label(self.frame, text="Registro Geral (RG):")
        self.label_rg.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_rg = ttk.Entry(self.frame)
        self.entry_rg.grid(row=2, column=1, padx=5, pady=5)

        self.label_cpf = ttk.Label(self.frame, text="Cadastro de Pessoa Fisica (CPF):")
        self.label_cpf.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_cpf = ttk.Entry(self.frame)
        self.entry_cpf.grid(row=3, column=1, padx=5, pady=5)

        self.label_telefone = ttk.Label(self.frame, text="Telefone de Contato:")
        self.label_telefone.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_telefone = ttk.Entry(self.frame)
        self.entry_telefone.grid(row=4, column=1, padx=5, pady=5)

        self.label_data_nascimento = ttk.Label(self.frame, text="Data de Nascimento:")
        self.label_data_nascimento.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entry_data_nascimento = DateEntry(self.frame)
        self.entry_data_nascimento.grid(row=5, column=1, padx=5, pady=5)

        # Limitar o RG, CPF e telefone
        self.entry_rg.bind("<KeyRelease>", self.limitar_rg)
        self.entry_cpf.bind("<KeyRelease>", self.limitar_cpf)
        self.entry_telefone.bind("<KeyRelease>", self.limitar_telefone)

        # Botão de cadastro
        self.botao_cadastrar = ttk.Button(self.frame, text="Cadastrar", command=self.cadastrar_cliente)
        self.botao_cadastrar.grid(row=6, column=1, padx=5, pady=10)

    def limitar_rg(self, event):
        if len(event.widget.get()) > 15:
            event.widget.delete(15, tk.END)

    def limitar_cpf(self, event):
        if len(event.widget.get()) > 15:
            event.widget.delete(15, tk.END)

    def limitar_telefone(self, event):
        valor = event.widget.get()
        if not valor.isdigit():  # Verificar se o valor contém apenas dígitos
            event.widget.delete(0, tk.END)  # Limpar o campo se não for um número
        elif len(valor) > 15:
            event.widget.delete(15, tk.END)  # Limitar a 15 dígitos

    def cadastrar_cliente(self):
        # Obter os valores dos campos
        nome = self.entry_nome.get()
        sobrenome = self.entry_sobrenome.get()
        rg = self.entry_rg.get()
        cpf = self.entry_cpf.get()
        data_nascimento = self.entry_data_nascimento.get()
        data_nascimento_formatada = datetime.strptime(data_nascimento, '%m/%d/%y').strftime('%Y-%m-%d')
        telefone = self.entry_telefone.get()

        # Validar se os campos obrigatórios foram preenchidos
        if nome and sobrenome and cpf and data_nascimento:
            conexao = ConexaoBancoDados()
            conexao.conectar()

            try:
                cursor = conexao.conn.cursor()

                # Verificar se já existe um cliente com o mesmo CPF ou RG
                cursor.execute("SELECT cpf, rg FROM clientes WHERE cpf = %s OR rg = %s", (cpf, rg))
                existing_client = cursor.fetchone()

                if existing_client:
                    messagebox.showerror("Erro", "Já existe um cliente com o mesmo CPF ou RG.")
                else:
                    # Inserir o novo cliente na tabela de clientes
                    insert_sql = "INSERT INTO clientes (nome, sobrenome, rg, cpf, data_nascimento, telefone) VALUES (%s, %s, %s, %s, %s, %s)"
                    valores = (nome, sobrenome, rg, cpf, data_nascimento_formatada, telefone)
                    cursor.execute(insert_sql, valores)
                    conexao.conn.commit()

                    messagebox.showinfo("Cadastro Cliente", "Cliente cadastrado com sucesso!")

                    # Limpar os campos após o cadastro
                    self.entry_nome.delete(0, tk.END)
                    self.entry_sobrenome.delete(0, tk.END)
                    self.entry_rg.delete(0, tk.END)
                    self.entry_cpf.delete(0, tk.END)
                    self.entry_data_nascimento.delete(0, tk.END)  # Limpar a data
                    self.entry_telefone.delete(0, tk.END)

            except mysql.connector.Error as e:
                print(f"Erro ao cadastrar o cliente: {e}")
                messagebox.showerror("Erro no Cadastro", f"Ocorreu um erro ao cadastrar o cliente. Type_error: {e} ")

            finally:
                cursor.close()
                conexao.desconectar()

        else:
            tk.messagebox.showerror("Erro no Preenchimento",
                                    "Preencha os campos obrigatórios: Nome, Sobrenome, CPF e Data de Nascimento")


if __name__ == "__main__":
    app = CadastroClientes()
    app.janela_cadastro.mainloop()
