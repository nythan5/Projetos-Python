import xmltodict
import os 
import pandas as pd
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


# Variáveis globais
caminho_diretorio_nf = ""
caminho_diretorio_excel = ""
valores = []

# Funções
def pegar_infos(nome_arquivo,valores):
    with open (f'{caminho_diretorio_nf}/{nome_arquivo}', "rb") as arquivo_xml:
        dict_arquivo = xmltodict.parse(arquivo_xml)  

        if "soap12:Envelope" in dict_arquivo:
            infos_nf = dict_arquivo["soap12:Envelope"]["soap12:Body"]["nfeDadosMsg"]["enviNFe"]["NFe"]["infNFe"]
        
        elif "NFe" in dict_arquivo:
            infos_nf = dict_arquivo["NFe"]["infNFe"]
        
        else:
            infos_nf = dict_arquivo["nfeProc"]["NFe"]["infNFe"]  

        numero_nota = infos_nf["@Id"]
        emissor_nota = infos_nf["emit"]["xNome"]
        cnpj_emissor = infos_nf["emit"]["CNPJ"]
        uf_emissor = infos_nf["emit"]["enderEmit"]["UF"]
        try:
            nome_cliente = infos_nf["dest"]["xNome"]
        except KeyError:
            nome_cliente = "Cliente não encontrado"
        valor_nota = infos_nf["total"]["ICMSTot"]["vNF"]
        icms = infos_nf["total"]["ICMSTot"]["vICMS"]
        pis = infos_nf["total"]["ICMSTot"]["vPIS"]
        cofins = infos_nf["total"]["ICMSTot"]["vCOFINS"]
        ipi = infos_nf["total"]["ICMSTot"]["vIPI"]
            
        valores.append([numero_nota,emissor_nota,cnpj_emissor,uf_emissor,nome_cliente,valor_nota,icms,pis,cofins,ipi])

def processar_caminho_xml():
    global caminho_diretorio_nf
    caminho_xml = diretorio_xml.get().strip().replace('"', '')
    caminho_diretorio_nf = caminho_xml
    #print(caminho_diretorio_nf)

def processar_caminho_excel():
    global caminho_diretorio_excel
    caminho_excel = diretorio_excel.get().strip().replace('"', '')
    caminho_diretorio_excel = caminho_excel
    #print(caminho_diretorio_excel)

def processar_tudo():
    processar_caminho_xml()
    processar_caminho_excel()

    for arquivo in os.listdir(caminho_diretorio_nf):
        pegar_infos(arquivo, valores)
   
    colunas = ["numero_nota","emissor_nota","CNPJ_emissor","UF_emissor","nome_cliente","valor_nota","ICMS","PIS","COFINS","IPI"]
    Tabela = pd.DataFrame(columns=colunas, data=valores) 
    nome_arquivo_excel = os.path.join(caminho_diretorio_excel, "NotasFiscais.xlsx")
    Tabela.to_excel(nome_arquivo_excel, index=False)
    messagebox.showinfo("Concluído","Processamento foi finalizado com sucesso!")
    diretorio_xml.delete(0,END)
    diretorio_excel.delete(0,END)
    



# Interface Gráfica
janela = Tk()
janela.title("XML to Excel")
janela.geometry("340x160")
#janela.iconbitmap('C:/Users/Gabriel Nathan Dias/Desktop/Python/Projetos-Python/XML to Excel/line_chart_file_icon_256235.ico')
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

diretorio_xml = ttk.Entry(janela)
diretorio_xml.place(x=20, y=35, width=300, height=25)

Texto_Orientacao2 = ttk.Label(janela, text= "Diretório para Salvar o Excel: ").place(x=20, y=60, width=300, height=25)

diretorio_excel = ttk.Entry(janela)
diretorio_excel.place(x=20, y=85, width=300, height=25)

botao_processar = ttk.Button(janela, text="Processar", command=processar_tudo)
botao_processar.place(x=80, y=120, width=180, height=35)






janela.mainloop()
