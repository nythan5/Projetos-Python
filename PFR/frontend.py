import threading
import tkinter as tk
from tkinter import ttk
from backend import AutomacaoPfr
import sys


class InterfaceGrafica:
    def __init__(self, janela,lista_pfr_preenchidas):
        self.janela = janela
        self.janela.title("Confirmação de PFR's")
        self.janela.geometry("450x130")

        # Status da aplicação
        self.event = threading.Event()
        self.lista_pfr_preenchidas = lista_pfr_preenchidas



        # Botão "Iniciar"
        self.botao_iniciar = tk.Button(self.janela, text="Iniciar", command=self.iniciar,width=15, height=3)
        self.botao_iniciar.pack(side=tk.LEFT,padx=5, pady=4)

        # Botão "Finalizar"
        self.botao_finalizar = tk.Button(self.janela, text="Finalizar", command=self.finalizar,width=15, height=3)
        self.botao_finalizar.pack(side=tk.RIGHT,padx=5, pady=4)

        # Rótulo acima da Listbox
        self.label_lista = tk.Label(self.janela, text="Lista de PFR's confirmadas!")
        self.label_lista.pack(side=tk.TOP, padx=5, pady=2)

        # Lista de PFRs preenchidas (widget)
        self.lista_pfr_widget = tk.Listbox(self.janela)
        self.lista_pfr_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


    def atualizar_lista(self):
        for item in self.lista_pfr_preenchidas:
            self.lista_pfr_widget.insert(tk.END, item)

    def codigo_a_executar(self):
        self.atualizar_lista()
        #app.iniciar_navegador()
        app.iniciar_automacao()
        self.atualizar_lista()





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
        self.janela.destroy()
        sys.exit()


if __name__ == "__main__":
    janela_principal = tk.Tk()
    app = AutomacaoPfr()
    lista_pfr_preenchidas = app.lista_pfr_naorealizadas
    print(lista_pfr_preenchidas)
    tela = InterfaceGrafica(janela_principal, lista_pfr_preenchidas)
    janela_principal.mainloop()
