import os
import time
import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedTk
from arquivoxlsx import ArquivoXlsx
from banco import ConexaoBancoDados


class Tela:
    def __init__(self):
        self.nome_arquivo = None
        self.arquivo = None
        self.janela = ThemedTk(theme="clearlooks")
        self.janela.title("Analise de Combustível")
        self.janela.geometry("390x200")
        self.classe_arquivo = ArquivoXlsx()
        self.banco = ConexaoBancoDados('localhost', 'root', '1234', 'analise_combustivel')


        # Criando um estilo personalizado para os botões
        self.style = ttk.Style()
        self.style.configure("Botao.TButton", foreground="black")



        self.label3 = ttk.Label(self.janela, text="Selecione o arquivo a ser inserido no banco de dados",
                                foreground="black")
        self.label3.pack(padx=5, pady=2)

        # Usando o estilo personalizado para o primeiro botão
        self.button1 = ttk.Button(self.janela, text="Selecione Arquivo:", command=self.localizar_arquivo,
                                  style="Botao.TButton")
        self.button1.pack(padx=20, pady=2)

        self.label = ttk.Label(self.janela, text=f"Arquivo selecionado: {self.arquivo}")
        self.label.pack(padx=15, pady=5)

        self.label4 = ttk.Label(self.janela, text="",
                                foreground="blue")
        self.label4.pack(padx=5, pady=2)

        # Usando o estilo personalizado para o segundo botão
        self.button2 = ttk.Button(self.janela, text="  Iniciar Aplicação  ", command=self.iniciar_aplicacao,
                                  style="Botao.TButton")
        self.button2.pack(padx=20, pady=2)

        self.label2 = ttk.Label(self.janela,)
        self.label2.pack(padx=10, pady=10)

        self.resultado_label = ttk.Label(self.janela, text="", foreground="red")
        self.resultado_label.pack(padx=10, pady=10)

    def localizar_arquivo(self):
        self.arquivo = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])
        if self.arquivo:
            self.nome_arquivo = os.path.basename(self.arquivo)
            self.label.config(text=f"Arquivo selecionado: {self.nome_arquivo}")
            self.classe_arquivo.diretorio_arquivo = self.arquivo
            self.classe_arquivo.nome_arquivo = self.nome_arquivo
            print("Arquivo selecionado:", self.classe_arquivo.diretorio_arquivo)
            print("Nome arquivo", self.classe_arquivo.nome_arquivo)

    def abrir_arquivo(self):
        planilha = self.classe_arquivo.carregar_planilha()
        #print(planilha)

    def iniciar_aplicacao(self):
        if self.arquivo is not None:
            # Mensagem de início da aplicação
            self.label2.config(text="Iniciando a aplicação...", foreground="black")

            self.abrir_arquivo()
            self.banco.insert_Banco(self.arquivo, self.nome_arquivo)

            if self.banco.resultado_consulta:
                # Mensagem de erro
                self.label2.config(text=self.banco.resultado_consulta, foreground="red")
            else:
                # Mensagem de sucesso
                self.label2.config(text="Processo Finalizado", foreground="green")

            self.arquivo = None
            self.banco.resultado_consulta = None
            self.janela.after(5000, self.reset_label)

        else:
            print("Nenhum arquivo selecionado.")
            self.label2.config(text="Nenhum arquivo selecionado", foreground="blue")
            self.janela.after(2000, self.reset_label)

    def reset_label(self):
        self.label.config(text="Arquivo selecionado: ")
        self.label2.config(text="")
        self.resultado_label.config(text="")

    def run(self):
        self.janela.mainloop()


if __name__ == "__main__":
    app = Tela()
    app.run()
