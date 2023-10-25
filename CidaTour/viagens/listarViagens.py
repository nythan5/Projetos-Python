import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkcalendar import DateEntry
from CidaTour.database import ConexaoBancoDados
from tkinter import messagebox
from datetime import datetime
import pandas as pd
from tkinter import filedialog

class ListaViagens:
    def __init__(self):
        self.janela_lista = ThemedTk(theme="clam")
        self.janela_lista.title("Lista de Viagens")

        self.frame = ttk.Frame(self.janela_lista, padding=10)
        self.frame.grid(row=0, column=0, padx=1, pady=1)

        self.tree = ttk.Treeview(self.frame, columns=("Título", "Descrição", "Data Check-In", "Data Check-Out", "Custo", "Status Viagem"), show="headings")
        self.tree.heading("Título", text="Título", command=lambda: self.ordenar_coluna("Título", False))
        self.tree.heading("Descrição", text="Descrição", command=lambda: self.ordenar_coluna("Descrição", False))
        self.tree.heading("Data Check-In", text="Data Check-In", command=lambda: self.ordenar_coluna("Data Check-In", True))
        self.tree.heading("Data Check-Out", text="Data Check-Out", command=lambda: self.ordenar_coluna("Data Check-Out", True))
        self.tree.heading("Custo", text="Custo", command=lambda: self.ordenar_coluna("Custo", True))
        self.tree.heading("Status Viagem", text="Status Viagem", command=lambda: self.ordenar_coluna("Status Viagem", False))

        self.tree.column("Título", width=100)
        self.tree.grid(row=0, column=0, padx=10, pady=10)

        # Configurar as cores das linhas de grade
        self.tree.style = ttk.Style()
        self.tree.style.map("Treeview", background=[("selected", "Gray")])

        self.direcao_ordenacao = {}  # Rastrear a direção de ordenação de cada coluna

        self.carregar_viagens()

        # Lidar com eventos de clique duplo para edição
        self.tree.bind("<Double-1>", self.editar_viagem)

        # Botão "Exportar para Excel"
        export_button = ttk.Button(self.frame, text="Exportar para Excel", command=self.exportar_para_excel)
        export_button.grid(row=1, column=0, pady=10)

    def carregar_viagens(self):
        # Antes de carregar as viagens, limpe a árvore
        for item in self.tree.get_children():
            self.tree.delete(item)

        conexao = ConexaoBancoDados()
        conexao.conectar()

        try:
            cursor = conexao.conn.cursor()
            cursor.execute("SELECT titulo, descricao, data_check_in, data_check_out, custo, status_viagem FROM viagens")
            viagens = cursor.fetchall()

            for viagem in viagens:
                ativo = "Ativo" if viagem[5] else "Inativo"
                data_check_in = viagem[2] if viagem[2] else ""  # Lidar com datas nulas
                data_check_out = viagem[3] if viagem[3] else ""  # Lidar com datas nulas
                self.tree.insert("", "end", values=(viagem[0], viagem[1], data_check_in, data_check_out, viagem[4], ativo))

        except Exception as e:
            print(f"Erro ao carregar viagens: {e}")

        finally:
            cursor.close()
            conexao.desconectar()

    def ordenar_coluna(self, col, reverse):
        if col == "Status Viagem":
            colunas = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
            colunas.sort(reverse=reverse, key=lambda x: x[0])  # Ordenar com base nos valores de texto
        else:
            colunas = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
            colunas.sort(reverse=reverse, key=lambda x: (x[0], x[1]))  # Ordenar numericamente
        for index, (val, item) in enumerate(colunas):
            self.tree.move(item, '', index)

    def editar_viagem(self, event):
        item_selecionado = self.tree.selection()[0]  # Obter o item selecionado
        valores = self.tree.item(item_selecionado, 'values')  # Obter os valores das colunas
        self.abrir_formulario_edicao(valores)

    def abrir_formulario_edicao(self, valores):
        # Crie uma nova janela para edição
        janela_edicao = ThemedTk(theme="clam")
        janela_edicao.title("Editar Viagem")

        frame = ttk.Frame(janela_edicao, padding=10)
        frame.grid(row=0, column=0, padx=1, pady=1)

        # Adicione rótulos e campos de entrada para as informações da viagem
        ttk.Label(frame, text="Título:").grid(row=0, column=0, sticky="w")
        titulo_entry = ttk.Entry(frame)
        titulo_entry.insert(0, valores[0])
        titulo_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Descrição:").grid(row=1, column=0, sticky="w")
        descricao_entry = tk.Text(frame, height=5, width=30)
        descricao_entry.insert("1.0", valores[1])
        descricao_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Data Check-In:").grid(row=2, column=0, sticky="w")
        data_check_in_entry = DateEntry(frame)  # Usar o DateEntry para seleção de data
        if valores[2]:
            data_check_in = datetime.strptime(valores[2], '%Y-%m-%d')  # Converter a string em objeto de data
            data_check_in_entry.set_date(data_check_in)
        data_check_in_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Data Check-Out:").grid(row=3, column=0, sticky="w")
        data_check_out_entry = DateEntry(frame)  # Usar o DateEntry para seleção de data
        if valores[3]:
            data_check_out = datetime.strptime(valores[3], '%Y-%m-%d')  # Converter a string em objeto de data
            data_check_out_entry.set_date(data_check_out)
        data_check_out_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Custo:").grid(row=4, column=0, sticky="w")
        custo_entry = ttk.Entry(frame)
        custo_entry.insert(0, valores[4])
        custo_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        ativo_var = tk.StringVar()
        ativo_combobox = ttk.Combobox(frame, textvariable=ativo_var, values=["Ativo", "Inativo"])
        ativo_combobox.set(valores[5])
        ativo_combobox.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Função para atualizar as informações no banco de dados
        def atualizar_viagem():
            conexao = ConexaoBancoDados()
            conexao.conectar()

            try:
                cursor = conexao.conn.cursor()
                titulo = titulo_entry.get()
                descricao = descricao_entry.get("1.0", tk.END)
                data_check_in = data_check_in_entry.get_date()
                data_check_out = data_check_out_entry.get_date()
                custo = custo_entry.get()
                ativo = ativo_combobox.get()

                ativo = True if ativo == "Ativo" else False

                # Atualiza a viagem no banco de dados
                cursor.execute(
                    "UPDATE viagens SET titulo = %s, descricao = %s, data_check_in = %s, data_check_out = %s, custo = %s, status_viagem = %s WHERE titulo = %s",
                    (titulo, descricao, data_check_in, data_check_out, custo, ativo, valores[0]))  # Use o título como identificador

                conexao.conn.commit()
                messagebox.showinfo("Sucesso", "Viagem atualizada com sucesso")
                janela_edicao.destroy()
                self.carregar_viagens()  # Recarregue a lista de viagens para refletir as alterações

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar a viagem: {e}")

            finally:
                cursor.close()
                conexao.desconectar()

        ttk.Button(frame, text="Atualizar Viagem", command=atualizar_viagem).grid(row=6, column=0, columnspan=2)

        janela_edicao.mainloop()

    def exportar_para_excel(self):
        conexao = ConexaoBancoDados()
        conexao.conectar()

        try:
            cursor = conexao.conn.cursor()
            cursor.execute("SELECT * FROM viagens")
            viagens = cursor.fetchall()

            df = pd.DataFrame(viagens, columns=["ID", "Título", "Descrição",
                                                "Data Check-In", "Data Check-Out", "Custo", "Status Viagem", "Data_Cadastro"])

            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])

            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Sucesso", f"Lista de viagens exportada com sucesso para {file_path}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar lista de viagens: {e}")

        finally:
            cursor.close()
            conexao.desconectar()

if __name__ == "__main__":
    app = ListaViagens()
    app.janela_lista.mainloop()
