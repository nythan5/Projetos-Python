import threading
import tkinter as tk
from tkinter import ttk
from backend import AutomacaoPfr
import sys
from PIL import Image
from PIL import ImageTk


class InterfaceGrafica:
    def __init__(self, janela, lista_pfr_preenchidas):
        self.janela = janela
        self.janela.title("Confirmação de PFR's")
        self.janela.geometry("490x130")

        # Configurar ícone da aplicação
        self.icon = ImageTk.PhotoImage(file="../PFR/icon/list_notes_930.ico")
        self.janela.iconphoto(True, self.icon)

        # Status da aplicação
        self.event = threading.Event()
        self.lista_pfr_preenchidas = lista_pfr_preenchidas
        self.total_linhas = app.carregar_planilha()[1]


        # Botão "Iniciar"
        self.botao_iniciar = tk.Button(self.janela, text="Iniciar Processo", command=self.iniciar, width=15, height=3)
        self.botao_iniciar.pack(side=tk.LEFT, padx=5, pady=4)

        # Botão "Finalizar"
        self.botao_finalizar = tk.Button(self.janela, text="Parar Processo", command=self.finalizar, width=15, height=3)
        self.botao_finalizar.pack(side=tk.RIGHT, padx=5, pady=4)

        # Rótulo acima da Listbox
        self.label_lista = tk.Label(self.janela,
                                    text=f"Lista de PFR's confirmada: {len(self.lista_pfr_preenchidas)} "
                                         f"de {self.total_linhas}")
        self.label_lista.pack(side=tk.TOP, padx=5, pady=2)

        # Lista de PFRs preenchidas (widget)
        self.lista_pfr_widget = tk.Listbox(self.janela)
        self.lista_pfr_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Callback que atualiza a listagem na Interface Grafica
        app.set_callback(self.atualizar_lista)

    def atualizar_lista(self, pfr):
        try:
            self.lista_pfr_widget.insert(tk.END, pfr)
            self.atualizar_label()
        except TypeError:
            print("Não foi possivel atualizar a lista")

    def atualizar_label(self):
        total_elementos = len(self.lista_pfr_widget.get(0, tk.END))
        self.label_lista.config(text=f"Lista de PFR's confirmada: {len(self.lista_pfr_preenchidas)} "
                                     f"de {self.total_linhas}")

    def codigo_a_executar(self):
        app.iniciar_navegador()
        app.iniciar_automacao()

    def iniciar(self):
        # Ação a ser realizada ao clicar no botão "Iniciar"
        print("Iniciando...")

        try:
            t = threading.Thread(target=self.codigo_a_executar)
            t.start()

        except ConnectionRefusedError:
            self.status_aplicacao = False
            print("Aplicação Encerrada")

    def finalizar(self):
        # Ação a ser realizada ao clicar no botão "Finalizar"
        print("Finalizando...")
        app.fechar_navegador()
        self.event.set()
        # self.janela.destroy()
        # sys.exit()


if __name__ == "__main__":
    janela_principal = tk.Tk()
    app = AutomacaoPfr()
    lista_pfr_preenchidas = app.lista_pfr_preenchidas
    tela = InterfaceGrafica(janela_principal, lista_pfr_preenchidas)
    janela_principal.mainloop()
