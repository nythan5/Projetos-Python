import tkinter as tk
from tkinter import ttk
from openpyxl import Workbook
from ttkthemes import ThemedTk
from CidaTour.database import ConexaoBancoDados
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
from tkinter import filedialog

class RegistroPagamentoViagem:
    def __init__(self):
        self.janela = ThemedTk(theme="clam")
        self.janela.title("Registro de Pagamento")

        self.frame = ttk.Frame(self.janela, padding=10)
        self.frame.pack()

        self.label_viagem = ttk.Label(self.frame, text="Viagem:")
        self.label_viagem.grid(row=0, column=0, padx=5, pady=10)
        self.combobox_viagem = ttk.Combobox(self.frame)
        self.combobox_viagem.grid(row=0, column=1, padx=5, pady=10)

        self.combobox_viagem.bind("<<ComboboxSelected>>", self.carregar_clientes)

        self.treeview = ttk.Treeview(self.frame, columns=("Nome", "Valor Pago", "Saldo Restante"))
        self.treeview.heading("#1", text="Nome")
        self.treeview.heading("#2", text="Valor Pago")
        self.treeview.heading("#3", text="Saldo Restante")
        self.treeview.column("#0", width=0, stretch=tk.NO)
        self.treeview.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        self.carregar_viagens()
        self.valor_total_pago = {}

        # Botão para cadastrar pagamento
        ttk.Button(self.frame, text="Cadastrar Pagamento", command=self.abrir_cadastro_pagamento).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        ttk.Button(self.frame, text="Exportar para Excel", command=self.exportar_pagamentos_para_excel).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def carregar_viagens(self):
        conexao = ConexaoBancoDados()
        conexao.conectar()

        try:
            cursor = conexao.conn.cursor()
            cursor.execute("SELECT titulo FROM viagens WHERE status_viagem = 1")
            viagens_disponíveis = cursor.fetchall()
            títulos_viagens_disponíveis = [viagem[0] for viagem in viagens_disponíveis]
            self.combobox_viagem['values'] = títulos_viagens_disponíveis

        except Exception as e:
            print(f"Erro ao carregar viagens disponíveis: {e}")

        finally:
            cursor.close()
            conexao.desconectar()

    def carregar_clientes(self, event):
        viagem_selecionada = self.combobox_viagem.get()
        if not viagem_selecionada:
            return

        conexao = ConexaoBancoDados()
        conexao.conectar()

        try:
            cursor = conexao.conn.cursor()
            cursor.execute("""
                SELECT c.id, c.nome, c.sobrenome, SUM(p.valor_pago)
                FROM clientes c
                JOIN viagens_clientes vc ON c.id = vc.id_cliente
                JOIN viagens v ON vc.id_viagem = v.id
                LEFT JOIN pagamentos p ON vc.id = p.id_viagens_clientes
                WHERE v.titulo = %s
                GROUP BY c.id
            """, (viagem_selecionada,))
            clientes_vinculados = cursor.fetchall()

            for item in self.treeview.get_children():
                self.treeview.delete(item)

            for cliente in clientes_vinculados:
                id_cliente = cliente[0]
                nome = f"{cliente[1]} {cliente[2]}"
                valor_total_pago = float(cliente[3] if cliente[3] is not None else 0)
                valor_custo = self.obter_valor_custo(viagem_selecionada)
                valor_restante = valor_custo - valor_total_pago
                self.treeview.insert("", "end", values=(nome, valor_total_pago, valor_restante, id_cliente))

            self.treeview.bind("<Double-1>", self.abrir_pagamentos_cliente)

        except Exception as e:
            print(f"Erro ao listar clientes vinculados: {e}")

        finally:
            cursor.close()
            conexao.desconectar()

    def obter_valor_custo(self, viagem_selecionada):
        conexao = ConexaoBancoDados()
        conexao.conectar()

        try:
            cursor = conexao.conn.cursor()
            cursor.execute("SELECT custo FROM viagens WHERE titulo = %s", (viagem_selecionada,))
            resultado = cursor.fetchone()

            if resultado:
                return resultado[0]
            else:
                return 0

        except Exception as e:
            print(f"Erro ao obter o valor do custo da viagem: {e}")
            return 0

        finally:
            cursor.close()
            conexao.desconectar()

    def abrir_pagamentos_cliente(self, event):
        item_selecionado = self.treeview.selection()[0]
        id_cliente = self.treeview.item(item_selecionado, 'values')[3]
        nome_cliente_completo = self.treeview.item(item_selecionado, 'values')[0]
        nome_cliente = nome_cliente_completo.split()[0]
        viagem_selecionada = self.combobox_viagem.get()

        id_viagem_cliente = self.obter_id_viagens_clientes(nome_cliente, viagem_selecionada)

        # Abra uma nova janela para exibir os pagamentos do cliente
        janela_pagamentos_cliente = ThemedTk(theme="clam")
        janela_pagamentos_cliente.title(f"Pagamentos de {nome_cliente}")

        frame = ttk.Frame(janela_pagamentos_cliente, padding=10)
        frame.pack()

        treeview_pagamentos = ttk.Treeview(frame, columns=("Valor Pago", "Data Pagamento"))
        treeview_pagamentos.heading("#1", text="Valor Pago")
        treeview_pagamentos.heading("#2", text="Data Pagamento")
        treeview_pagamentos.column("#0", width=0, stretch=tk.NO)
        treeview_pagamentos.grid(row=0, column=0, padx=5, pady=10)

        conexao = ConexaoBancoDados()
        conexao.conectar()

        try:
            cursor = conexao.conn.cursor()
            cursor.execute("SELECT valor_pago, data_pagamento FROM pagamentos WHERE id_viagens_clientes = %s", (id_viagem_cliente, ))
            pagamentos = cursor.fetchall()

            for pagamento in pagamentos:
                valor_pago = pagamento[0]
                data_pagamento = pagamento[1]
                treeview_pagamentos.insert("", "end", values=(valor_pago, data_pagamento))

        except Exception as e:
            print(f"Erro ao listar pagamentos do cliente: {e}")

        finally:
            cursor.close()
            conexao.desconectar()

        def fechar_janela():
            janela_pagamentos_cliente.destroy()

        # Botão para fechar a janela
        ttk.Button(frame, text="Fechar", command=fechar_janela).grid(row=1, column=0, padx=5, pady=10)

    def abrir_cadastro_pagamento(self):
        # Abra uma nova janela para o cadastro de pagamento
        janela_cadastro_pagamento = ThemedTk(theme="clam")
        janela_cadastro_pagamento.title("Cadastro de Pagamento")

        frame = ttk.Frame(janela_cadastro_pagamento, padding=10)
        frame.pack()

        # Adicione um combobox para selecionar a viagem
        ttk.Label(frame, text="Viagem:").grid(row=0, column=0, padx=5, pady=10)
        self.combobox_viagem_cadastro = ttk.Combobox(frame)
        self.combobox_viagem_cadastro.grid(row=0, column=1, padx=5, pady=10)
        self.combobox_viagem_cadastro['values'] = self.combobox_viagem['values']  # Copia os valores do combobox da tela principal

        # Evento para carregar clientes associados à viagem selecionada
        self.combobox_viagem_cadastro.bind("<<ComboboxSelected>>", self.carregar_clientes_cadastro)

        ttk.Label(frame, text="Cliente:").grid(row=1, column=0, padx=5, pady=10)
        self.combobox_cliente = ttk.Combobox(frame)
        self.combobox_cliente.grid(row=1, column=1, padx=5, pady=10)

        ttk.Label(frame, text="Valor Pago:").grid(row=2, column=0, padx=5, pady=10)
        self.entry_valor = ttk.Entry(frame)
        self.entry_valor.grid(row=2, column=1, padx=5, pady=10)

        ttk.Label(frame, text="Data Pagamento:").grid(row=3, column=0, padx=5, pady=10)
        self.calendario = Calendar(frame)
        self.calendario.grid(row=3, column=1, padx=5, pady=10)

        # Botão para confirmar o cadastro do pagamento
        ttk.Button(frame, text="Confirmar", command=self.cadastrar_pagamento).grid(row=4, column=0, columnspan=2,
                                                                                   padx=5, pady=10)

        # Atualize a lista de clientes associados à viagem selecionada
        self.combobox_viagem_cadastro.bind("<<ComboboxSelected>>", self.carregar_clientes_cadastro)

    def carregar_clientes_cadastro(self, event):
        viagem_selecionada = self.combobox_viagem_cadastro.get()
        conexao = ConexaoBancoDados()
        conexao.conectar()

        try:
            cursor = conexao.conn.cursor()
            cursor.execute("""
                SELECT c.nome
                FROM clientes c
                JOIN viagens_clientes vc ON c.id = vc.id_cliente
                JOIN viagens v ON vc.id_viagem = v.id
                WHERE v.titulo = %s
            """, (viagem_selecionada,))
            clientes_associados = cursor.fetchall()
            nomes_clientes = [cliente[0] for cliente in clientes_associados]
            self.combobox_cliente['values'] = nomes_clientes

        except Exception as e:
            print(f"Erro ao carregar clientes associados à viagem: {e}")

        finally:
            cursor.close()
            conexao.desconectar()

    def cadastrar_pagamento(self):
        cliente_selecionado = self.combobox_cliente.get()
        viagem_selecionada = self.combobox_viagem_cadastro.get()
        valor_pago = self.entry_valor.get()
        data_pagamento = self.calendario.get_date()

        # Realize a validação dos dados aqui
        if not cliente_selecionado or not viagem_selecionada or not valor_pago or not data_pagamento:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        # Formate a data no formato 'YYYY-MM-DD'
        try:
            data_pagamento = datetime.strptime(data_pagamento, "%m/%d/%y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Data de pagamento inválida. Use o formato MM/DD/YY.")
            return

        # Obtenha o ID de viagens_clientes
        id_viagens_clientes = self.obter_id_viagens_clientes(cliente_selecionado, viagem_selecionada)

        if id_viagens_clientes is not None:
            # Insira os dados do pagamento no banco de dados
            conexao = ConexaoBancoDados()
            conexao.conectar()

            try:
                cursor = conexao.conn.cursor()
                cursor.execute("""
                    INSERT INTO pagamentos (id_viagens_clientes, valor_pago, data_pagamento)
                    VALUES (%s, %s, %s)
                """, (id_viagens_clientes, valor_pago, data_pagamento))

                conexao.conn.commit()

                # Atualize a exibição dos valores na Treeview
                self.carregar_clientes(None)

            except Exception as e:
                print(f"Erro ao cadastrar pagamento: {e}")
                conexao.conn.rollback()

            finally:
                cursor.close()
                conexao.desconectar()
        else:
            messagebox.showerror("Erro",
                                 "Não foi possível encontrar o ID de viagens_clientes para o cliente e viagem selecionados.")

    def obter_id_viagens_clientes(self, cliente, viagem):
        conexao = ConexaoBancoDados()
        conexao.conectar()

        try:
            cursor = conexao.conn.cursor()
            cursor.execute("""
                SELECT vc.id
                FROM viagens_clientes vc
                JOIN clientes c ON vc.id_cliente = c.id
                JOIN viagens v ON vc.id_viagem = v.id
                WHERE c.nome = %s AND v.titulo = %s
            """, (cliente, viagem))
            resultado = cursor.fetchone()

            if resultado:
                return resultado[0]
            else:
                return None

        except Exception as e:
            print(f"Erro ao obter o ID de viagens_clientes: {e}")
            return None

        finally:
            cursor.close()
            conexao.desconectar()

    def run(self):
        self.janela.mainloop()

    def exportar_pagamentos_para_excel(self):
        arquivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx")])

        if arquivo:
            wb = Workbook()
            ws = wb.active

            # Adicione cabeçalhos às colunas
            ws.append(["Nome", "Valor Pago", "Saldo Restante"])

            # Obtenha os dados da Treeview
            for item in self.treeview.get_children():
                nome = self.treeview.item(item, 'values')[0]
                valor_pago = self.treeview.item(item, 'values')[1]
                saldo_restante = self.treeview.item(item, 'values')[2]
                ws.append([nome, valor_pago, saldo_restante])

            wb.save(arquivo)

            messagebox.showinfo("Exportação Concluída", "Os dados foram exportados para Excel com sucesso.")

if __name__ == "__main__":
    app = RegistroPagamentoViagem()
    app.run()
