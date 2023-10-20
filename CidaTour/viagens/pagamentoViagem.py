import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkcalendar import DateEntry
from CidaTour.database import ConexaoBancoDados
from tkinter import messagebox
from datetime import datetime

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

        self.treeview = ttk.Treeview(self.frame, columns=("Nome", "Valor Pago", "Valor Restante"))
        self.treeview.heading("Nome", text="Nome", command=lambda: self.sort_column(self.treeview, "Nome", False))
        self.treeview.heading("Valor Pago", text="Valor Pago", command=lambda: self.sort_column(self.treeview, "Valor Pago", True))
        self.treeview.heading("Valor Restante", text="Valor Restante", command=lambda: self.sort_column(self.treeview, "Valor Restante", True))
        self.treeview.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        # Configurar a largura da primeira coluna para 0
        self.treeview.column("#0", width=0, stretch=tk.NO)

        self.carregar_viagens()

    def sort_column(self, treeview, col, reverse):
        items = [(treeview.set(item, col), item) for item in treeview.get_children('')]
        items.sort(reverse=reverse)
        for index, (val, item) in enumerate(items):
            treeview.move(item, '', index)

    def carregar_viagens(self):
        conexao = ConexaoBancoDados()
        conexao.conectar()

        try:
            cursor = conexao.conn.cursor()
            cursor.execute("SELECT titulo FROM viagens WHERE status_viagem = 1")
            viagens_disponiveis = cursor.fetchall()
            titulos_viagens_disponiveis = [viagem[0] for viagem in viagens_disponiveis]  # Corrigido o nome da variável
            self.combobox_viagem['values'] = titulos_viagens_disponiveis

        except Exception as e:
            print(f"Erro ao carregar viagens disponíveis: {e}")

        finally:
            cursor.close()
            conexao.desconectar()

    def carregar_clientes(self, event):
        viagem_selecionada = self.combobox_viagem.get()
        conexao = ConexaoBancoDados()
        conexao.conectar()

        try:
            cursor = conexao.conn.cursor()
            cursor.execute("""
                SELECT c.nome, p.valor_pago
                FROM clientes c
                JOIN viagens_clientes vc ON c.id = vc.id_cliente
                JOIN viagens v ON vc.id_viagem = v.id
                LEFT JOIN pagamentos p ON vc.id = p.id_viagens_clientes
                WHERE v.titulo = %s
            """, (viagem_selecionada,))
            clientes_vinculados = cursor.fetchall()

            for item in self.treeview.get_children():
                self.treeview.delete(item)

            for cliente in clientes_vinculados:
                nome = cliente[0]
                valor_pago = cliente[1] if cliente[1] is not None else 0
                valor_custo = self.obter_valor_custo(viagem_selecionada)
                valor_restante = valor_custo - valor_pago
                self.treeview.insert("", "end", values=(nome, valor_pago, valor_restante))

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

if __name__ == "__main__":
    app = RegistroPagamentoViagem()
    app.janela.mainloop()
