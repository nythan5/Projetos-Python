import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from CidaTour.database import ConexaoBancoDados
from tkinter import messagebox

class ListaClientes:
    def __init__(self):
        self.janela_lista = ThemedTk(theme="clam")
        self.janela_lista.title("Lista de Clientes")

        self.frame = ttk.Frame(self.janela_lista, padding=10)
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

        # Lidar com eventos de clique duplo para edição
        self.tree.bind("<Double-1>", self.editar_cliente)

    def carregar_clientes(self):
        # Limpar a árvore antes de carregar os clientes
        for item in self.tree.get_children():
            self.tree.delete(item)

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

    def editar_cliente(self, event):
        item_selecionado = self.tree.selection()[0]  # Obter o item selecionado
        valores = self.tree.item(item_selecionado, 'values')  # Obter os valores das colunas
        self.abrir_formulario_edicao(valores)

    def abrir_formulario_edicao(self, valores):
        janela_edicao = ThemedTk(theme="clam")
        janela_edicao.title("Editar Cliente")

        frame = ttk.Frame(janela_edicao, padding=10)
        frame.grid(row=0, column=0, padx=1, pady=1)

        ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w")
        nome_entry = ttk.Entry(frame)
        nome_entry.insert(0, valores[0])
        nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Sobrenome:").grid(row=1, column=0, sticky="w")
        sobrenome_entry = ttk.Entry(frame)
        sobrenome_entry.insert(0, valores[1])
        sobrenome_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="CPF:").grid(row=2, column=0, sticky="w")
        cpf_entry = ttk.Entry(frame)
        cpf_entry.insert(0, valores[2])
        cpf_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Data de Nascimento:").grid(row=3, column=0, sticky="w")
        data_nascimento_entry = ttk.Entry(frame)
        data_nascimento_entry.insert(0, valores[3])
        data_nascimento_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Telefone:").grid(row=4, column=0, sticky="w")
        telefone_entry = ttk.Entry(frame)
        telefone_entry.insert(0, valores[4])
        telefone_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        ativo_var = tk.StringVar()
        ativo_combobox = ttk.Combobox(frame, textvariable=ativo_var, values=["Ativo", "Inativo"])
        ativo_combobox.set(valores[5])
        ativo_combobox.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        def atualizar_cliente():
            conexao = ConexaoBancoDados()
            conexao.conectar()

            try:
                cursor = conexao.conn.cursor()
                nome = nome_entry.get()
                sobrenome = sobrenome_entry.get()
                cpf = cpf_entry.get()
                data_nascimento = data_nascimento_entry.get()
                telefone = telefone_entry.get()
                ativo = ativo_combobox.get()

                ativo = True if ativo == "Ativo" else False

                cursor.execute(
                    "UPDATE clientes SET nome = %s, sobrenome = %s, cpf = %s, data_nascimento = %s, telefone = %s, status_cliente = %s WHERE cpf = %s",
                    (nome, sobrenome, cpf, data_nascimento, telefone, ativo, valores[2]))  # Use o CPF como identificador

                conexao.conn.commit()
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso")
                janela_edicao.destroy()
                self.carregar_clientes()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar o cliente: {e}")

            finally:
                cursor.close()
                conexao.desconectar()

        ttk.Button(frame, text="Atualizar Cliente", command=atualizar_cliente).grid(row=6, column=0, columnspan=2)

        janela_edicao.mainloop()

