import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from CidaTour.database import ConexaoBancoDados
from tkinter import messagebox
import pandas as pd
from tkinter import filedialog

class ListarClientesViagem:
    def __init__(self):
        self.janela = ThemedTk(theme="clam")
        self.janela.title("Listar Clientes por Viagem")

        self.frame = ttk.Frame(self.janela, padding=10)
        self.frame.grid(row=0, column=0, padx=1, pady=1)

        # Crie um ComboBox para selecionar uma viagem ativa
        self.label_viagem = ttk.Label(self.frame, text="Viagens Ativas:")
        self.label_viagem.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.combobox_viagem = ttk.Combobox(self.frame)
        self.combobox_viagem.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.combobox_viagem.bind("<<ComboboxSelected>>", self.listar_clientes_por_viagem)

        # Crie uma label para exibir o número de pessoas associadas
        self.label_num_pessoas = ttk.Label(self.frame, text="")
        self.label_num_pessoas.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Crie um Listbox para listar os clientes vinculados
        self.clientes_listbox = tk.Listbox(self.frame, width=40, height=10)
        self.clientes_listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.clientes_listbox.bind("<Button-1>", self.selecionar_cliente)

        # Adicione um botão para deletar um cliente
        self.botao_deletar = ttk.Button(self.frame, text="Deletar Cliente", command=self.deletar_cliente)
        self.botao_deletar.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Botão "Exportar para Excel"
        export_button = ttk.Button(self.frame, text="Exportar para Excel", command=self.exportar_para_excel)
        export_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Carregue as viagens ativas no Combobox
        self.carregar_viagens_ativas()

        # Variáveis para armazenar o cliente selecionado
        self.cliente_selecionado = None
        self.viagem_selecionada = None
        self.cliente_id_selecionado = None

    def carregar_viagens_ativas(self):
        # Conecte-se ao banco de dados
        conexao = ConexaoBancoDados()
        conexao.conectar()

        try:
            cursor = conexao.conn.cursor()

            # Execute uma consulta para obter as viagens ativas
            cursor.execute("SELECT titulo FROM viagens WHERE status_viagem = 1")
            viagens_ativas = cursor.fetchall()

            # Obtenha a lista de títulos das viagens ativas
            titulos_viagens_ativas = [viagens[0] for viagens in viagens_ativas]

            # Atualize o Combobox com os títulos das viagens ativas
            self.combobox_viagem['values'] = titulos_viagens_ativas

        except Exception as e:
            print(f"Erro ao carregar viagens ativas: {e}")

        finally:
            cursor.close()
            conexao.desconectar()

    def listar_clientes_por_viagem(self, event):
        # Obter a viagem selecionada do ComboBox
        self.viagem_selecionada = self.combobox_viagem.get()

        # Conecte-se ao banco de dados
        conexao = ConexaoBancoDados()
        conexao.conectar()

        try:
            cursor = conexao.conn.cursor()

            # Execute uma consulta para obter os clientes vinculados a essa viagem
            cursor.execute("""
                SELECT c.nome, c.sobrenome
                FROM clientes c
                JOIN viagens_clientes vc ON c.id = vc.id_cliente
                JOIN viagens v ON vc.id_viagem = v.id
                WHERE v.titulo = %s
            """, (self.viagem_selecionada,))
            clientes_vinculados = cursor.fetchall()

            # Limpar o Listbox
            self.clientes_listbox.delete(0, tk.END)

            # Listar os clientes vinculados no Listbox
            for cliente in clientes_vinculados:
                nome_completo = f"{cliente[0]} {cliente[1]}"
                self.clientes_listbox.insert(tk.END, nome_completo)

            # Atualizar a label com o número de pessoas associadas
            num_pessoas = len(clientes_vinculados)
            self.label_num_pessoas.config(text=f"Número de Pessoas Associadas: {num_pessoas}")

        except Exception as e:
            print(f"Erro ao listar clientes por viagem: {e}")

        finally:
            cursor.close()
            conexao.desconectar()

    def selecionar_cliente(self, event):
        try:
            # Obtém o índice do item selecionado no Listbox
            index = self.clientes_listbox.curselection()[0]

            # Obtém o cliente selecionado
            self.cliente_selecionado = self.clientes_listbox.get(index)

            # Separe o nome do sobrenome
            nome, sobrenome = self.cliente_selecionado.split(" ")

            # Conecte-se ao banco de dados
            conexao = ConexaoBancoDados()
            conexao.conectar()

            cursor = conexao.conn.cursor()

            # Execute uma consulta para obter o ID do cliente com base no nome e sobrenome
            cursor.execute("SELECT id FROM clientes WHERE nome = %s AND sobrenome = %s", (nome, sobrenome))
            cliente_id = cursor.fetchone()
            print("CLiente Selecionado", self.cliente_id_selecionado)

            if cliente_id:
                # Armazene o ID do cliente selecionado
                self.cliente_id_selecionado = cliente_id[0]

        except IndexError:
            # Trate a exceção se nenhum cliente estiver selecionado
            self.cliente_selecionado = None

    def deletar_cliente(self):
        if not self.cliente_selecionado or not self.viagem_selecionada:
            messagebox.showerror("Erro", "Selecione um cliente para deletar.")
            return

        # Conecte-se ao banco de dados
        conexao = ConexaoBancoDados()
        conexao.conectar()

        try:
            cursor = conexao.conn.cursor()

            # Separe o nome do sobrenome
            nome, sobrenome = self.cliente_selecionado.split(" ")

            # Execute uma consulta para obter o ID do cliente com base no nome e sobrenome
            cursor.execute("SELECT id FROM clientes WHERE nome = %s AND sobrenome = %s", (nome, sobrenome))
            cliente_id = cursor.fetchone()

            if cliente_id:
                # Execute uma consulta para desassociar o cliente da viagem
                cursor.execute(
                    "DELETE FROM viagens_clientes WHERE id_viagem = (SELECT id FROM viagens WHERE titulo = %s) AND id_cliente = %s",
                    (self.viagem_selecionada, cliente_id[0]))
                conexao.conn.commit()
                messagebox.showinfo("Status", f"Cliente removido da viagem: {self.viagem_selecionada}")

                # Atualize a lista de clientes na interface
                self.listar_clientes_por_viagem(None)

        except Exception as e:
            print(f"Erro ao deletar cliente da viagem: {e}")
            messagebox.showerror("Erro", f"Não foi possível deletar o cliente da viagem. {e}")

        finally:
            cursor.close()
            conexao.desconectar()

    def exportar_para_excel(self):
        if not self.viagem_selecionada:
            messagebox.showerror("Erro", "Selecione uma viagem para exportar.")
            return

        # Conecte-se ao banco de dados
        conexao = ConexaoBancoDados()
        conexao.conectar()

        try:
            cursor = conexao.conn.cursor()

            # Execute uma consulta para obter os clientes vinculados a essa viagem
            cursor.execute("""
                SELECT c.nome, c.sobrenome, c.rg, c.cpf, c.telefone
                FROM clientes c
                JOIN viagens_clientes vc ON c.id = vc.id_cliente
                JOIN viagens v ON vc.id_viagem = v.id
                WHERE v.titulo = %s
            """, (self.viagem_selecionada,))
            clientes_vinculados = cursor.fetchall()

            # Criar um DataFrame com os clientes
            df = pd.DataFrame(clientes_vinculados, columns=["Nome", "Sobrenome", "RG", "CPF", "Telefone"])

            # Solicitar o local de salvamento do arquivo Excel
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])

            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Sucesso", f"Lista de clientes exportada com sucesso para {file_path}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar lista de clientes: {e}")

        finally:
            cursor.close()
            conexao.desconectar()

if __name__ == "__main__":
    app = ListarClientesViagem()
    app.janela.mainloop()
