from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
import time
import pandas as pd
from datetime import datetime

# Preparando o navegador para entrar no site
service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service)
navegador.get("https://jdsn-pft.deere.com/pft/servlet/com.deere.u90242.premiumfreight.view.servlets.PremiumFreightServlet")

# Aguarda 1minuto para fazer login
time.sleep(60)

# Clicando em Search
navegador.find_element('xpath','//*[@id="left_navigation"]/ul/li[4]/a').click()
time.sleep(2)

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

# Laço para que ele realize cada ciclo de acordo com a quantidade de linhas da Planilha

for i , pfr in enumerate (planilha_carregada["PFR"]):
    codigo_transportadora = planilha_carregada.loc[i,'Codigo_Transportadora']
    tipo_numero_referencia = "Carrier Pro"
    cte = planilha_carregada.loc[i,'CT-e']
    valor_frete = planilha_carregada.loc[i,'Valor do Frete']
    currency = "BRL"
    peso = planilha_carregada.loc[i,'Peso']
    measure = "KG"

    data_hora_coleta = planilha_carregada.loc[i,'Data e Horário da Coleta']
    # Parseando a informação de coleta em variaveis 
    dia_coleta = datetime.fromtimestamp(data_hora_coleta.timestamp()).strftime('%d')
    mes_coleta = datetime.fromtimestamp(data_hora_coleta.timestamp()).strftime('%b')
    ano_coleta = datetime.fromtimestamp(data_hora_coleta.timestamp()).strftime('%Y')
    hora_coleta = datetime.fromtimestamp(data_hora_coleta.timestamp()).strftime('%H:%M')

    # Parseando a informação de entrega em variaveis 
    data_hora_entrega = planilha_carregada.loc[i,'Previsão de Entrega']
    dia_coleta = datetime.fromtimestamp(data_hora_entrega.timestamp()).strftime('%d')
    mes_coleta = datetime.fromtimestamp(data_hora_entrega.timestamp()).strftime('%b')
    ano_coleta = datetime.fromtimestamp(data_hora_entrega.timestamp()).strftime('%Y')
    hora_coleta = datetime.fromtimestamp(data_hora_entrega.timestamp()).strftime('%H:%M')

    # Preenchendo as informações em cada campo

    # Campo PFR e search 
    navegador.find_element('xpath','//*[@id="pfNumber"]').send_keys(pfr)
    time.sleep(2)
    navegador.find_element('xpath','//*[@id="content_center"]/table/tbody/tr[10]/td/center/a[1]').click()
    time.sleep(2)

    # CLicando na PRF localizada
    navegador.find_element('xpath','//*[@id="table01"]/tbody/tr/td[1]/a').click()
    time.sleep(2)

    