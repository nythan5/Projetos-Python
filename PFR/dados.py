import pandas as pd
from datetime import datetime


# Exemplo de uso da função:
caminho_planilha = r"C:\Users\Gabriel Nathan Dias\Desktop\PFR1.xls"

def carregar_planilha(caminho_planilha):
    # Remove espaços em branco e aspas do caminho da planilha fornecido pelo usuário
    caminho_planilha = caminho_planilha.strip().replace('"', '')
    planilha = pd.read_excel(caminho_planilha)
    return planilha
    

# Validação do carregamento da planilha com a função carregar_planilha
planilha_carregada = carregar_planilha(caminho_planilha)

if planilha_carregada is not None:
    print("Planilha carregada com sucesso")
else:
    print("Falha ao carregar a planilha.")

# Inicialize uma lista vazia para armazenar os dicionários
lista_de_dicionarios = []

# Itere pelas linhas da planilha
for index, row in planilha_carregada.iterrows():
    dicionario = {
        'Linha': [index+1],
        'PFR': row['PFR'],
        'Transportadora': row['Transportadora'],
        'Codigo_Transportadora': row['Codigo_Transportadora'],
        'CT-e': row['CT-e'],
        'Valor do Frete': row['Valor do Frete'],
        'Peso': row['Peso'],
        'Data e Horário da Coleta': row['Data e Horário da Coleta'],
        'Previsão de Entrega': row['Previsão de Entrega']
        
    }
    # Adicione o dicionário à lista
    lista_de_dicionarios.append(dicionario)



dicionario = lista_de_dicionarios[0]

pfr = dicionario['PFR']
codigo_transportadora = dicionario['Codigo_Transportadora']
tipo_numero_referencia = "Carrier Pro"
cte = dicionario['CT-e']
valor_frete = dicionario['Valor do Frete']
currency = "BRL"
peso = dicionario['Peso']
measure = "KG"

print(peso)


