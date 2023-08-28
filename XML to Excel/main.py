import xmltodict
import os 
import pandas as pd
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


# Variáveis globais
caminho_diretorio_NF = ""
caminho_diretorio_Excel = ""
valores = []

# Funções
def pegar_infos(nome_arquivo,valores):
    with open (f'{caminho_diretorio_NF}/{nome_arquivo}',"rb") as arquivo_xml:
        dict_arquivo = xmltodict.parse(arquivo_xml)                
        if "NFe" in dict_arquivo:
            infos_nf = dict_arquivo["NFe"]["infNFe"]
        else:
            infos_nf = dict_arquivo["nfeProc"]["NFe"]["infNFe"]  

        numero_nota = infos_nf["@Id"]
        emissor_nota = infos_nf["emit"]["xNome"]
        CNPJ_emissor = infos_nf["emit"]["CNPJ"]
        UF_emissor = infos_nf["emit"]["enderEmit"]["UF"]
        nome_cliente = infos_nf["dest"]["xNome"]
        valor_nota = infos_nf["total"]["ICMSTot"]["vNF"]
        ICMS = infos_nf["total"]["ICMSTot"]["vICMS"]
        PIS = infos_nf["total"]["ICMSTot"]["vPIS"]
        COFINS = infos_nf["total"]["ICMSTot"]["vCOFINS"]
        IPI = infos_nf["total"]["ICMSTot"]["vIPI"]
            
        valores.append([numero_nota,emissor_nota,CNPJ_emissor,UF_emissor,nome_cliente,valor_nota,ICMS,PIS,COFINS,IPI])

def processar_caminho_XML():
    global caminho_diretorio_NF
    caminho_XML = diretorio_XML.get().strip().replace('"', '')
    caminho_diretorio_NF = caminho_XML
    print(caminho_diretorio_NF)

def processar_caminho_Excel():
    global caminho_diretorio_Excel
    caminho_Excel = diretorio_Excel.get().strip().replace('"', '')
    caminho_diretorio_Excel = caminho_Excel
    print(caminho_diretorio_Excel)

def processar_Tudo():
    processar_caminho_XML()
    processar_caminho_Excel()

    for arquivo in os.listdir(caminho_diretorio_NF):
        pegar_infos(arquivo, valores)
   
    colunas = ["numero_nota","emissor_nota","CNPJ_emissor","UF_emissor","nome_cliente","valor_nota","ICMS","PIS","COFINS","IPI"]
    Tabela = pd.DataFrame(columns=colunas, data=valores) 
    nome_arquivo_excel = os.path.join(caminho_diretorio_Excel, "NotasFiscais.xlsx")
    Tabela.to_excel(nome_arquivo_excel, index=False)
    messagebox.showinfo("Concluído","Processamento foi finalizado com sucesso!")
    diretorio_XML.delete(0,END)
    diretorio_Excel.delete(0,END)
    



# Interface Gráfica
janela = Tk()
janela.title("XML to Excel")
janela.geometry("340x160")
janela.iconbitmap('C:/Users/gnd20/Desktop/Projetos Python/XML to Excel/line_chart_file_icon_256235.ico')
janela.configure(bg= "white")


# Criar estilo
style = ttk.Style()

# Definir estilo para o botão
style.configure("TButton", font=("Helvetica", 11),padding = 4,relief ="flat",foreground = "black", background = "white")

# Definir estilo para o label
style.configure("TLabel", font=("Helvetica", 11),background = "white")

# Definir estilo para o entry
style.configure("TEntry",background = "white",bordercolor = "white",foreground=[("active", "black"), ("!active", "black")],fieldbackground=[("active", "white"), ("!active", "white")])



Texto_Orientacao1 = ttk.Label(janela, text= "Diretório do XML:").place(x=20, y=10, width=300, height=25)

diretorio_XML = ttk.Entry(janela)
diretorio_XML.place(x=20, y=35, width=300, height=25)

Texto_Orientacao2 = ttk.Label(janela, text= "Diretório para Salvar o Excel: ").place(x=20, y=60, width=300, height=25)

diretorio_Excel = ttk.Entry(janela)
diretorio_Excel.place(x=20, y=85, width=300, height=25)

botao_processar = ttk.Button(janela, text="Processar", command=processar_Tudo)
botao_processar.place(x=80, y=120, width=180, height=35)






janela.mainloop()
