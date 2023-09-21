from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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
    peso1 = planilha_carregada.loc[i,'Peso'] 
    peso_formatado = "{:.2f}".format(peso1)
    measure = "KG"

    
    data_hora_coleta = planilha_carregada.loc[i,'Data e Horário da Coleta']
    # Parseando a informação de coleta em variaveis 
    dia_coleta = datetime.fromtimestamp(data_hora_coleta.timestamp()).strftime('%d')
    mes_coleta = datetime.fromtimestamp(data_hora_coleta.timestamp()).strftime('%b')
    ano_coleta = datetime.fromtimestamp(data_hora_coleta.timestamp()).strftime('%Y')
    hora_coleta = datetime.fromtimestamp(data_hora_coleta.timestamp()).strftime('%H:%M')

    # Parseando a informação de entrega em variaveis 
    data_hora_entrega = planilha_carregada.loc[i,'Previsão de Entrega']
    dia_entrega = datetime.fromtimestamp(data_hora_entrega.timestamp()).strftime('%d')
    mes_entrega = datetime.fromtimestamp(data_hora_entrega.timestamp()).strftime('%b')
    ano_entrega = datetime.fromtimestamp(data_hora_entrega.timestamp()).strftime('%Y')
    hora_entrega = datetime.fromtimestamp(data_hora_entrega.timestamp()).strftime('%H:%M')


    # Descobrindo a quantidade de Looping da seleção da transportadora
    match codigo_transportadora:
        case 372052: # ARMANI
            loop_transportadora = 31
        case 375317: # VF
            loop_transportadora = 37
        case 361822: # MODULAR
            loop_transportadora = 26
        case 316937: # TW
            loop_transportadora = 13
        

    # Clicando em Search
    navegador.find_element('xpath','//*[@id="left_navigation"]/ul/li[4]/a').click()
    time.sleep(5)

    # Preenchendo as informações em cada campo

    # Campo PFR e search 
    navegador.find_element('xpath','//*[@id="pfNumber"]').send_keys(pfr)
    time.sleep(2)
    navegador.find_element('xpath','//*[@id="content_center"]/table/tbody/tr[10]/td/center/a[1]').click()
    time.sleep(5)

    # CLicando na PRF localizada
    navegador.find_element('xpath','//*[@id="table01"]/tbody/tr/td[1]/a').click()
    time.sleep(5)

    # Buscando o Carrier na lista
    navegador.find_element('xpath','//*[@id="pendingConfList0.carrier"]').click()

    # Clicando com a seta \/ para selecionar a transportadora de acordo com o codigo
    count = 0
    while (count < loop_transportadora):
        navegador.find_element('xpath','//*[@id="pendingConfList0.carrier"]').send_keys(Keys.UP)
        count += 1

    time.sleep(1)

    # Preenchendo o Tipo de numero de referencia
    navegador.find_element('xpath','//*[@id="pendingConfList0.referenceType"]').send_keys(tipo_numero_referencia)
    time.sleep(1)

    # Preenchendo o CTe
    navegador.find_element('xpath','//*[@id="ConfirmTD_0"]/fieldset/table/tbody/tr[4]/td[2]/input').send_keys(cte)
    time.sleep(1)

    # Preenchendo o Valor do Frete
    navegador.find_element('xpath','//*[@id="pendingConfList0.invoiceAmount"]').send_keys(valor_frete)
    time.sleep(1)

    # Preenchendo o currency
    navegador.find_element('xpath','//*[@id="pendingConfList0.currencyCode"]').send_keys(currency)
    time.sleep(1)
    
    # Preenchendo o peso
    navegador.find_element('xpath','//*[@id="ConfirmTD_0"]/fieldset/table/tbody/tr[7]/td[2]/input').send_keys(peso_formatado)
    time.sleep(1)
    
    # Preenchendo o measure
    navegador.find_element('xpath','//*[@id="pendingConfList0.unitOfMeasure"]').send_keys(measure)
    time.sleep(1)
    
    # Preenchendo Data de Coleta
    navegador.find_element('xpath','//*[@id="pendingConfList0.pickupETADate.dayVal"]').send_keys(dia_coleta)
    time.sleep(0.5)
    
    navegador.find_element('xpath','//*[@id="ConfirmTD_0"]/fieldset/table/tbody/tr[11]/td[2]/div/font/select').send_keys(mes_coleta)
    time.sleep(0.5)

    navegador.find_element(By.NAME,'pendingConfList0.pickupETADate.yearVal').send_keys(ano_coleta)     
    time.sleep(0.5)    

    time.sleep(900000)
    
