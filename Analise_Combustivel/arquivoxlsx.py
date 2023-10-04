import pandas as pd


class ArquivoXlsx:
    def __init__(self):
        self.diretorio_arquivo = None

    def carregar_planilha(self):
        caminho_planilha = self.diretorio_arquivo
        planilha = pd.read_excel(caminho_planilha, skiprows=9)
        return planilha


