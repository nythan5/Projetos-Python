# Importa as bibliotecas necessárias
import tkinter as tk  # Importa a biblioteca tkinter para criar a interface gráfica
from tkinter import ttk  # Importa ttk para estilos de widgets
import threading  # Importa threading para execução de código em segundo plano
import time  # Importa time para controlar o tempo
from automacao import realizar_automacao


# Classe TelaApp para a aplicação tkinter
class TelaApp:
    # Método construtor, inicializa a janela principal e outros elementos
    def __init__(self, root):
        self.root = root  # Define a janela principal como atributo
        self.root.geometry("300x100")  # Define o tamanho da janela (largura x altura)
        self.root.title("Execução de Código")  # Define o título da janela
        self.root.configure(bg="white")  # Define a cor de fundo da janela

        # Cria um estilo para os widgets (botões)
        self.style = ttk.Style()
        # Configura o estilo para os botões com fonte, padding, relevo e cores específicas
        self.style.configure("TButton", font=("Helvetica", 11), padding=4, relief="flat",
                             foreground="black", background="white", borderwidth=0)

        # Criação do botão "Iniciar" e associação com o método iniciar_codigo
        self.botao_iniciar = ttk.Button(self.root, text="Iniciar Código", command=self.iniciar_codigo)
        self.botao_iniciar.pack()  # Empacota o botão na janela

        # Criação do botão "Parar" e associação com o método parar_codigo
        self.botao_parar = ttk.Button(self.root, text="Parar Código", command=self.parar_codigo)
        self.botao_parar.pack()  # Empacota o botão na janela

        # Variável de controle para a execução do código
        self.executar_codigo = False

    # Método que contém o código a ser executado em segundo plano
    def codigo_a_executar(self):
        while self.executar_codigo:
            print("Executando o código...")
            # Coloque aqui o seu código a ser executado em segundo plano
            realizar_automacao()
            time.sleep(1)


    # Método para iniciar a execução do código em segundo plano
    def iniciar_codigo(self):
        self.executar_codigo = True  # Define a variável de controle como True
        t = threading.Thread(target=self.codigo_a_executar)  # Cria uma thread para executar o código
        t.start()  # Inicia a thread
        
    # Método para parar a execução do código em segundo plano
    def parar_codigo(self):
        self.executar_codigo = False  # Define a variável de controle como False
        print(self.executar_codigo)
        

        

# Verifica se o arquivo está sendo executado como o programa principal
if __name__ == "__main__":
    janela = tk.Tk()  # Cria a janela principal do tkinter
    app = TelaApp(janela)  # Cria uma instância da classe TelaApp passando a janela como parâmetro
    janela.mainloop()  # Inicia o loop principal do tkinter para exibir a interface gráfica
