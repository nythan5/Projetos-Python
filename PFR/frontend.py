import threading
import tkinter as tk
from backend import AutomacaoPfr
import sys
from PIL import ImageTk


class InterfaceGrafica:
    def __init__(self, janela, lista_pfr_preenchidas, lista_pfr_com_erro):
        self.janela = janela
        self.janela.title("Confirmação de PFR's")
        self.janela.geometry("350x320")

        # Configurar ícone da aplicação
        self.icon = ImageTk.PhotoImage(file="../PFR/icon/list_notes_930.ico")
        self.janela.iconphoto(True, self.icon)

        # Status da aplicação
        self.event = threading.Event()
        self.lista_pfr_preenchidas = lista_pfr_preenchidas
        self.lista_com_erros = lista_pfr_com_erro
        self.total_linhas = app.carregar_planilha()[1]

        # Frame dos Botoes
        self.frame_botoes = tk.Frame(self.janela)
        self.frame_botoes.pack(side=tk.BOTTOM, padx=5, pady=4)

        # Botão "Iniciar"
        self.botao_iniciar = tk.Button(self.frame_botoes, text="Iniciar Processo", command=self.iniciar, width=15, height=3)
        self.botao_iniciar.pack(side=tk.LEFT, padx=5, pady=4)

        # Botão "Finalizar"
        self.botao_finalizar = tk.Button(self.frame_botoes, text="Parar Processo", command=self.finalizar, width=15, height=3)
        self.botao_finalizar.pack(side=tk.RIGHT, padx=10, pady=4)


        # Frame dos ListBox

        self.frame_listbox = tk.Frame(self.janela)
        self.frame_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Rótulo acima da Listbox
        self.label_lista_ok = tk.Label(self.janela,
                                    text=f" < -- PFR's confirmada: {len(self.lista_pfr_preenchidas)} "
                                         f"de {self.total_linhas}")
        self.label_lista_ok.pack(side=tk.TOP, anchor=tk.CENTER, padx=5, pady=2)

        # Lista de PFRs preenchidas (widget)
        self.lista_pfr_widget = tk.Listbox(self.frame_listbox)
        self.lista_pfr_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Rótulo acima da Listbox
        self.label_lista_nok = tk.Label(self.janela, text=f"PFR's com erro --> : {len(self.lista_com_erros)}")
        self.label_lista_nok.pack(side=tk.BOTTOM, anchor=tk.CENTER, padx=5, pady=2)

        # Lista de PFRs com erro (widget)
        self.lista_pfr_com_erro_widget = tk.Listbox(self.frame_listbox)
        self.lista_pfr_com_erro_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Callback que atualiza a listagem na Interface Grafica
        app.set_callback_ok(self.atualizar_lista_ok)
        app.set_callback_nok(self.atualizar_lista_nok)

    def atualizar_lista_nok(self, pfr):
        self.lista_pfr_com_erro_widget.insert(tk.END, pfr)

    def atualizar_lista_ok(self, pfr):
        try:
            self.lista_pfr_widget.insert(tk.END, pfr)
            self.atualizar_label()
        except TypeError:
            print("Não foi possivel atualizar a lista")

    def atualizar_label(self):
        total_elementos = len(self.lista_pfr_widget.get(0, tk.END))
        self.label_lista_ok.config(text=f" < -- PFR's confirmada: {len(lista_pfr_preenchidas)} "
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
        self.janela.destroy()
        sys.exit()


if __name__ == "__main__":
    janela_principal = tk.Tk()
    app = AutomacaoPfr()
    lista_pfr_preenchidas = app.lista_pfr_preenchidas
    lista_pfr_com_erro = app.lista_pfr_naorealizadas
    tela = InterfaceGrafica(janela_principal, lista_pfr_preenchidas, lista_pfr_com_erro)
    janela_principal.mainloop()
