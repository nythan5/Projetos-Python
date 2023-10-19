import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from CidaTour.database import ConexaoBancoDados
from tkinter import messagebox


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

        # Crie uma área de texto para listar os clientes vinculados
        self.clientes_text = tk.Text(self.frame, wrap=tk.WORD, width=40, height=10)
        self.clientes_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Carregue as viagens ativas no Combobox
        self.carregar_viagens_ativas()

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
            titulos_viagens_ativas = [viagem[0] for viagem in viagens_ativas]

            # Atualize o Combobox com os títulos das viagens ativas
            self.combobox_viagem['values'] = titulos_viagens_ativas

            return titulos_viagens_ativas

        except Exception as e:
            print(f"Erro ao carregar viagens ativas: {e}")

        finally:
            cursor.close()
            conexao.desconectar()
            return []

    def listar_clientes_por_viagem(self, event):
        # Obter a viagem selecionada do ComboBox
        viagem_selecionada = self.combobox_viagem.get()

        # Conecte-se ao banco de dados
        conexao = ConexaoBancoDados()
        conexao.conectar()

        try:
            cursor = conexao.conn.cursor()

            # Execute uma consulta para obter os clientes vinculados a essa viagem
            cursor.execute("""
                SELECT c.nome
                FROM clientes c
                JOIN viagens_clientes vc ON c.id = vc.id_cliente
                JOIN viagens v ON vc.id_viagem = v.id
                WHERE v.titulo = %s
            """, (viagem_selecionada,))
            clientes_vinculados = cursor.fetchall()

            # Limpar a área de texto
            self.clientes_text.delete(1.0, tk.END)

            # Listar os clientes vinculados na área de texto
            for cliente in clientes_vinculados:
                self.clientes_text.insert(tk.END, cliente[0] + "\n")

            # Atualizar a label com o número de pessoas associadas
            num_pessoas = len(clientes_vinculados)
            self.label_num_pessoas.config(text=f"Número de Pessoas Associadas: {num_pessoas}")

        except Exception as e:
            print(f"Erro ao listar clientes por viagem: {e}")

        finally:
            cursor.close()
            conexao.desconectar()


if __name__ == "__main__":
    app = ListarClientesViagem()
    app.janela.mainloop()
