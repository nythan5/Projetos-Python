import tkinter as tk
import time
from tkinter import ttk


# Função que contém o código que será executado
def codigo_a_executar():
    while executar_codigo:
        print("Executando o código...")
        # Coloque aqui o seu código
        time.sleep(1)

# Função para iniciar a execução do código
def iniciar_codigo():
    global executar_codigo
    executar_codigo = True
    # Inicie uma thread para executar o código em segundo plano
    import threading
    thread = threading.Thread(target=codigo_a_executar)
    thread.start()

# Função para parar a execução do código
def parar_codigo():
    print("Parando o código...")
    global executar_codigo
    executar_codigo = False

# Criar a janela principal do Tkinter
janela = tk.Tk()
janela.geometry("300x100")
janela.title("Execução de Código")
janela.configure(bg= "white")

# Criar estilo
style = ttk.Style()
# Definir estilo para o botão
style.configure("TButton", font=("Helvetica", 11), padding=4, relief="flat", foreground="black", background="white", borderwidth=0)


# Botão "Iniciar"
botao_iniciar = ttk.Button(janela, text="Iniciar Código", command=iniciar_codigo)
botao_iniciar.pack()

# Botão "Parar"
botao_parar = ttk.Button(janela, text="Parar Código", command=parar_codigo)
botao_parar.pack()

# Variável de controle para a execução do código
executar_codigo = False

# Iniciar a interface gráfica
janela.mainloop()
