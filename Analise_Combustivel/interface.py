import os
import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedTk
from arquivoxlsx import ArquivoXlsx


class Tela:
    def __init__(self):
        self.arquivo = None
        self.janela = ThemedTk(theme="clearlooks")
        self.janela.title("Minha Aplicação Tkinter com Tema Moderno")
        self.janela.geometry("400x200")
        self.classe_arquivo = ArquivoXlsx()

        self.label = ttk.Label(self.janela, text=f"Arquivo selecionado: {self.arquivo}")
        self.label.pack(padx=10, pady=10)

        self.button = ttk.Button(self.janela, text="Selecione o Arquivo:", command=self.localizar_arquivo)
        self.button.pack(padx=15, pady=10)

        self.button = ttk.Button(self.janela, text="Iniciar Aplicação", command=self.abrir_arquivo)
        self.button.pack(padx=20, pady=10)

    def localizar_arquivo(self):
        self.arquivo = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])
        if self.arquivo:
            nome_arquivo = os.path.basename(self.arquivo)
            self.label.config(text=f"Arquivo selecionado: {nome_arquivo}")
            self.classe_arquivo.diretorio_arquivo = self.arquivo
            print("Arquivo selecionado:", self.classe_arquivo.diretorio_arquivo)

    def abrir_arquivo(self):
        planilha = self.classe_arquivo.carregar_planilha()
        print(planilha)




    def run(self):
        self.janela.mainloop()





if __name__ == "__main__":
    app = Tela()
    app.run()
