from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from ttkthemes.themed_tk import ThemedTk
from CidaTour.database import ConexaoBancoDados

class CadastroViagens:
    def __init__(self):
        self.janela_cadastro = ThemedTk(theme="clam")
        self.janela_cadastro.title("Cadastro de Viagens")

        self.frame = ttk.Frame(self.janela_cadastro, padding=10)
        self.frame.grid(row=0, column=0, padx=1, pady=1)

        # Campos de entrada
        self.label_titulo = ttk.Label(self.frame, text="Título:")
        self.label_titulo.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_titulo = ttk.Entry(self.frame)
        self.entry_titulo.grid(row=0, column=1, padx=5, pady=5)

        self.label_descricao = ttk.Label(self.frame, text="Descrição:")
        self.label_descricao.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.entry_descricao = tk.Text(self.frame, height=5, width=30)
        self.entry_descricao.grid(row=2, column=1, padx=5, pady=5)

        self.label_custo = ttk.Label(self.frame, text="Custo:")
        self.label_custo.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_custo = ttk.Entry(self.frame)
        self.entry_custo.grid(row=1, column=1, padx=5, pady=5)

        # Campos de data
        self.label_checkin = ttk.Label(self.frame, text="Data de Check-in:")
        self.label_checkin.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.cal_checkin = DateEntry(self.frame)
        self.cal_checkin.grid(row=3, column=1, padx=5, pady=5)

        self.label_checkout = ttk.Label(self.frame, text="Data de Check-out:")
        self.label_checkout.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.cal_checkout = DateEntry(self.frame)
        self.cal_checkout.grid(row=4, column=1, padx=5, pady=5)

        # Etiqueta para mostrar o número de caracteres restantes
        self.caracteres_restantes_label = ttk.Label(self.frame, text="Caracteres restantes: 255")
        self.caracteres_restantes_label.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Adicionar evento para atualizar a contagem de caracteres
        self.entry_descricao.bind("<KeyRelease>", self.atualizar_contagem_caracteres)

        # Botão de cadastro
        self.botao_cadastrar = ttk.Button(self.frame, text="Cadastrar", command=self.cadastrar_viagem)
        self.botao_cadastrar.grid(row=6, column=1, padx=5, pady=10)

    def atualizar_contagem_caracteres(self, event):
        texto = self.entry_descricao.get("1.0", tk.END)  # Obter o texto do campo de descrição
        caracteres_restantes = 255 - len(texto)  # Calcular os caracteres restantes
        self.caracteres_restantes_label.config(text=f"Caracteres restantes: {caracteres_restantes}")

    def cadastrar_viagem(self):
        # Obter os valores dos campos
        titulo = self.entry_titulo.get()
        descricao = self.entry_descricao.get("1.0", tk.END)
        custo = self.entry_custo.get()
        data_checkin = self.cal_checkin.get_date()
        data_checkout = self.cal_checkout.get_date()

        # Validar se os campos obrigatórios foram preenchidos
        if not titulo:
            messagebox.showerror("Erro no Preenchimento", "Preencha o campo Título")
            return
        if not data_checkin or not data_checkout:
            messagebox.showerror("Erro no Preenchimento", "Preencha as datas de Check-in e Check-out")
            return

        # Validar se a data de Check-in é anterior à data de Check-out
        if data_checkin > data_checkout:
            messagebox.showerror("Erro nas Datas", "A Data de Check-in deve ser anterior à Data de Check-out")
            return

        # Lógica para verificar se a viagem já existe com os mesmos valores
        conexao = ConexaoBancoDados()
        conexao.conectar()
        cursor = conexao.conn.cursor()

        # Consulta SQL para verificar se já existe uma viagem com o mesmo título
        select_sql = "SELECT id FROM viagens WHERE titulo = %s"
        valores = (titulo,)

        cursor.execute(select_sql, valores)
        viagem_existente = cursor.fetchone()

        if viagem_existente:
            messagebox.showerror("Erro no Cadastro", "Já existe uma viagem com o mesmo título.")
        else:
            try:
                # SQL para inserir uma nova viagem na tabela de viagens
                insert_sql = "INSERT INTO viagens (titulo, descricao, custo, data_check_in, data_check_out) VALUES (%s, %s, %s, %s, %s)"

                # Valores para a consulta SQL
                valores = (titulo, descricao, custo, data_checkin, data_checkout)

                # Executar a consulta SQL
                cursor.execute(insert_sql, valores)

                # Confirmar a operação e salvar as mudanças no banco de dados
                conexao.conn.commit()

                messagebox.showinfo("Cadastro Viagem", "Viagem cadastrada com sucesso!")

                # Limpar os campos após o cadastro
                self.entry_titulo.delete(0, tk.END)
                self.entry_descricao.delete("1.0", tk.END)
                self.entry_custo.delete(0, tk.END)
                self.cal_checkin.delete(0, tk.END)  # Limpar a data de Check-in
                self.cal_checkout.delete(0, tk.END)  # Limpar a data de Check-out

            except Exception as e:
                print(f"Erro ao cadastrar a viagem: {e}")
                messagebox.showerror("Erro no Cadastro", f"Ocorreu um erro ao cadastrar a viagem. Error: {e}")

            finally:
                # Fechar o cursor e a conexão
                cursor.close()
                conexao.desconectar()


