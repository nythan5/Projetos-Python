import pandas as pd

# Exemplo de uso da função:
caminho_da_planilha = r"C:\Users\Gabriel Nathan Dias\Desktop\PFR.xls"

def carregar_planilha(caminho):
    # Remova espaços em branco e aspas do caminho fornecido pelo usuário
    caminho = caminho.strip().replace('"', '')

    # Tente carregar a planilha
    try:
        planilha = pd.read_excel(caminho)
        return planilha
    except Exception as e:
        print(f"Erro ao carregar a planilha: {str(e)}")
        return None


planilha_carregada = carregar_planilha(caminho_da_planilha)

if planilha_carregada is not None:
    print(planilha_carregada)
else:
    print("Falha ao carregar a planilha.")


for indice, linha in planilha_carregada.iterrows():

    # Colunas da planilha 
    pfr = planilha_carregada['PFR']
    transportadora = planilha_carregada['Transportadora']
    cte = planilha_carregada ['CT-e']
    valor_frete = planilha_carregada ['Valor do Frete']
    peso = planilha_carregada ['Peso']
    data_hora_coleta = planilha_carregada ['Data e Horário da Coleta']
    data_hora_entrega = planilha_carregada ['Previsão de Entrega']
    
    # Executar o processo de entrar no site 







