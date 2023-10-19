import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from CidaTour.database import ConexaoBancoDados
from tkinter import messagebox

class AssociarClientesViagem:
    def __init__(self):
        self.janela = ThemedTk(theme="clam")
        self.janela.title("Associar Clientes a Viagem")

        self.frame = ttk.Frame(self.janela, padding=10)
        self.frame.grid(row=0, column=0, padx=1, pady=1)

        # Crie uma lista de seleção para viagens ativas
        self.label_viagem = ttk.Label(self.frame, text="Viagens Disponíveis:")
        self.label_viagem.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Adicione um Combobox para selecionar uma viagem ativa
        self.combobox_viagem = ttk.Combobox(self.frame)
        self.combobox_viagem.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Crie uma lista de seleção para clientes ativos
        self.label_cliente = ttk.Label(self.frame, text="Clientes Ativos:")
        self.label_cliente.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Adicione um Combobox para selecionar um cliente ativo
        self.combobox_cliente = ttk.Combobox(self.frame)
        self.combobox_cliente.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Botão para associar cliente à viagem
        self.botao_associar = ttk.Button(self.frame, text="Associar", command=self.associar_cliente_viagem)
        self.botao_associar.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        # Carregar clientes ativos no Combobox
        self.carregar_clientes_ativos()

        # Carregar viagens disponíveis no Combobox
        self.carregar_viagens_disponiveis()

    def carregar_clientes_ativos(self):
        # Limpe os valores existentes no Combobox de clientes
        self.combobox_cliente.set('')

        # Conecte-se ao banco de dados
        conexao = ConexaoBancoDados()
        conexao.conectar()

        try:
            cursor = conexao.conn.cursor()

            # Execute uma consulta para obter os clientes ativos
            cursor.execute("SELECT nome FROM clientes WHERE status_cliente = 1")
            clientes_ativos = cursor.fetchall()

            # Obtenha a lista de nomes dos clientes ativos
            nomes_clientes_ativos = [cliente[0] for cliente in clientes_ativos]

            # Preencha o Combobox de clientes com os nomes dos clientes ativos
            self.combobox_cliente['values'] = nomes_clientes_ativos

        except Exception as e:
            print(f"Erro ao carregar clientes ativos: {e}")

        finally:
            cursor.close()
            conexao.desconectar()

    def carregar_viagens_disponiveis(self):
        # Limpe os valores existentes no Combobox de viagens
        self.combobox_viagem.set('')

        # Conecte-se ao banco de dados
        conexao = ConexaoBancoDados()
        conexao.conectar()

        try:
            cursor = conexao.conn.cursor()

            # Execute uma consulta para obter as viagens ativas com vagas disponíveis
            cursor.execute("SELECT titulo FROM viagens WHERE status_viagem = 1")
            viagens_disponíveis = cursor.fetchall()

            # Crie uma lista de exibição que inclui o nome da viagem e o mês
            viagens_exibicao = [viagem[0] for viagem in viagens_disponíveis]

            # Preencha o Combobox de viagens com os destinos das viagens disponíveis
            self.combobox_viagem['values'] = viagens_exibicao

        except Exception as e:
            print(f"Erro ao carregar viagens disponíveis: {e}")

        finally:
            cursor.close()
            conexao.desconectar()

    def associar_cliente_viagem(self):
        # Obter o cliente e a viagem selecionados dos Combobox
        cliente_selecionado = self.combobox_cliente.get()
        viagem_selecionada = self.combobox_viagem.get()

        # Obter o ID do cliente a partir do banco de dados usando o método da classe
        id_cliente = self.obter_id_cliente_por_nome(cliente_selecionado)

        # Obter o ID da viagem a partir do banco de dados usando o método da classe
        id_viagem = self.obter_id_viagem_por_titulo(viagem_selecionada)

        if id_cliente is not None and id_viagem is not None:
            # Conecte-se ao banco de dados
            conexao = ConexaoBancoDados()
            conexao.conectar()

            try:
                cursor = conexao.conn.cursor()

                # Certifique-se de que id_cliente e id_viagem sejam valores inteiros ou adequados ao tipo de dados da tabela
                query = f"INSERT INTO viagens_clientes (id_cliente, id_viagem) VALUES ({id_cliente}, {id_viagem})"
                cursor.execute(query)

                # Commit para salvar as alterações no banco de dados
                conexao.conn.commit()

                messagebox.showinfo("Status", f"CLiente Associado a viagem {viagem_selecionada} ")

            except Exception as e:
                print(f"Erro ao associar cliente à viagem: {e}")
                messagebox.showerror("Erro ao associar cliente à viagem",f"Erro: {e} ")

            finally:
                cursor.close()
                conexao.desconectar()

    def obter_id_cliente_por_nome(self, nome_cliente):
        try:
            conexao = ConexaoBancoDados()
            conexao.conectar()
            cursor = conexao.conn.cursor()

            # Consulta SQL parametrizada para obter o ID do cliente com base no nome
            query = "SELECT id FROM clientes WHERE nome = %s"
            print("Query:", query)  # Adicione esta linha para imprimir a consulta
            cursor.execute(query, (nome_cliente,))
            resultado = cursor.fetchone()
            print("Resultado:", resultado)  # Adicione esta linha para imprimir o resultado

            if resultado:
                id_cliente = resultado[0]
                return id_cliente

        except Exception as e:
            print(f"Erro ao obter ID do cliente: {e}")
        finally:
            cursor.close()
            conexao.desconectar()

        return None  # Retorna None se não encontrar o cliente com o nome especificado

    def obter_id_viagem_por_titulo(self, titulo):
        try:
            conexao = ConexaoBancoDados()
            conexao.conectar()
            cursor = conexao.conn.cursor()

            # Consulta SQL para obter o ID da viagem com base no título
            query = "SELECT id FROM viagens WHERE titulo = %s"
            print("Query:", query)  # Adicione esta linha para imprimir a consulta
            print("Titulo", titulo)
            cursor.execute(query, (titulo,))
            resultado = cursor.fetchone()
            print("Resultado:", resultado)  # Adicione esta linha para imprimir o resultado

            if resultado:
                id_viagem = resultado[0]
                return id_viagem


        except Exception as e:
            print(f"Erro ao obter ID da viagem: {e}")
        finally:
            cursor.close()
            conexao.desconectar()

        return None  # Retorna None se não encontrar a viagem com o título especificado



