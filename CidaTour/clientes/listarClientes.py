import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from database import ConexaoBancoDados

class ListaClientes:
    def __init__(self):
        self.janela_lista = ThemedTk(theme="clam")
        self.janela_lista.title("Lista de Clientes")

        self.frame = ttk.Frame(self.janela_lista)
        self.frame.grid(row=0, column=0, padx=1, pady=1)

        self.tree = ttk.Treeview(self.frame, columns=("Nome", "Sobrenome", "CPF", "Data de Nascimento", "Telefone", "Ativo"), show="headings")
        self.tree.heading("Nome", text="Nome", command=lambda: self.ordenar_coluna("Nome", False))
        self.tree.heading("Sobrenome", text="Sobrenome", command=lambda: self.ordenar_coluna("Sobrenome", False))
        self.tree.heading("CPF", text="CPF", command=lambda: self.ordenar_coluna("CPF", False))
        self.tree.heading("Data de Nascimento", text="Data de Nascimento", command=lambda: self.ordenar_coluna("Data de Nascimento", True))
        self.tree.heading("Telefone", text="Telefone", command=lambda: self.ordenar_coluna("Telefone", False))
        self.tree.heading("Ativo", text="Ativo", command=lambda: self.ordenar_coluna("Ativo", False))

        self.tree.column("Ativo", width=80)  # Largura da coluna "Ativo"
        self.tree.grid(row=0, column=0)

        # Configurar as cores das linhas de grade
        self.tree.style = ttk.Style()
        self.tree.style.map("Treeview", background=[("selected", "Gray")])

        self.direcao_ordenacao = {}  # Rastrear a direção de ordenação de cada coluna

        self.carregar_clientes()

    def carregar_clientes(self):
        conexao = ConexaoBancoDados()
        conexao.conectar()

        try:
            cursor = conexao.conn.cursor()
            cursor.execute("SELECT nome, sobrenome, cpf, data_nascimento, telefone, status_cliente FROM clientes")
            clientes = cursor.fetchall()

            for cliente in clientes:
                ativo = "Ativo" if cliente[5] else "Inativo"
                self.tree.insert("", "end", values=(cliente[0], cliente[1], cliente[2], cliente[3], cliente[4], ativo))

        except Exception as e:
            print(f"Erro ao carregar clientes: {e}")

        finally:
            cursor.close()
            conexao.desconectar()

    def ordenar_coluna(self, col, reverse):
        if col == "Ativo":
            colunas = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
            colunas.sort(reverse=reverse, key=lambda x: x[0])  # Ordenar com base nos valores de texto
        else:
            colunas = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
            colunas.sort(reverse=reverse, key=lambda x: (x[0], x[1]))  # Ordenar numericamente
        for index, (val, item) in enumerate(colunas):
            self.tree.move(item, '', index)


