import pandas as pd


class ArquivoXlsx:
    def __init__(self):
        self.diretorio_arquivo = r"C:\Users\Gabriel Nathan Dias\Downloads\ANP\revendas_lpc_2023-09-17_2023-09-23.xlsx"

    def carregar_planilha(self):
        caminho_planilha = self.diretorio_arquivo.strip().replace('"', '')
        planilha = pd.read_excel(caminho_planilha, skiprows=9)
        return planilha


"""arquivo = ArquivoXlsx()
planilha = arquivo.carregar_planilha()


print(planilha)
"""
