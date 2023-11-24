import pandas as pd

class ArquivoFrequencia:
    def __init__(self):
        self.diretorio_arquivo = None
        self.nome_arquivo = None

    def carregar_planilha(self):
        #caminho_planilha = self.diretorio_arquivo
        caminho_planilha = r"C:\Users\Gabriel Nathan Dias\Desktop\Python\Projetos-Python\Analise_Frequencia_ILC\Arquivos Excel\frequencia_2023-11-24_16-13-55.xls"
        planilha = pd.read_excel(caminho_planilha)
        return planilha

    def filtrar_fornecedores(self):
        fornecedores = self.carregar_planilha()
        fornecedores = fornecedores.loc[
            fornecedores['FREQUENCIA_ATUAL'].str.contains('SEG'), ['FORNECEDOR', 'CLIENTE', 'FREQUENCIA_ATUAL']]
        fornecedores.groupby('FORNECEDOR')['CLIENTE']
        fornecedores.to_excel('Fornecedores de Segunda Feira.xlsx', index=False)

        print(fornecedores)


if __name__ == '__main__':
    app = ArquivoFrequencia()
    app.filtrar_fornecedores()




