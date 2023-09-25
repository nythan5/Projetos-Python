from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
import time
import pandas as pd
from datetime import datetime
import pytz
from pynput import mouse 


# Variaveis Globais
caminho_planilha = r"C:\Users\Gabriel Nathan Dias\Desktop\Relatorio mensal PFR-RPA.xls"
espera_curta = 0.5
espera_media = 1.5
espera_longa = 7
espera_login = 30
login = "YFAM2IY"
senha = "j918200_Mm123"
lista_pfr_preenchidas = []



# Preparando o navegador para entrar no site
service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service)
LINK = "https://jdsn-pft.deere.com/pft/servlet/com.deere.u90242.premiumfreight.view.servlets.PremiumFreightServlet"
navegador.get(LINK)


def bloquear_scroll(x, y, dx, dy):
    return False  # Retorna False para bloquear o scroll

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

# Aguarda 1 minuto para fazer voltar para a clicar no search
time.sleep(espera_longa)
navegador.find_element('xpath','//*[@id="okta-signin-username"]').send_keys(login)
time.sleep(0.5)
navegador.find_element('xpath','//*[@id="okta-signin-password"]').send_keys(senha)
time.sleep(0.5)
navegador.find_element('xpath','//*[@id="okta-signin-submit"]').click()
time.sleep(espera_longa)
navegador.find_element('xpath','//*[@id="form66"]/div[1]/div[2]/a').click()
time.sleep(espera_login)

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
    comments = planilha_carregada.loc[i,'Observações']

    # Obtém o fuso horário do Brasil
    fuso_horario_brasil = pytz.timezone('America/Sao_Paulo')

    # Obtém o campo Data e Hora de Coleta da Planilha
    data_hora_coleta = planilha_carregada.loc[i,'Data e Horário da Coleta']

    # Converte a data e hora da coleta para o fuso horário do Brasil
    data_hora_coleta_brasil = data_hora_coleta.replace(tzinfo=fuso_horario_brasil)

    # Parseando as informaçoes de data e hora ajustadas para o fuso horário do Brasil
    dia_coleta = data_hora_coleta_brasil.strftime('%d')
    mes_coleta = data_hora_coleta_brasil.strftime('%b')
    ano_coleta = data_hora_coleta_brasil.strftime('%Y')
    hora_coleta = data_hora_coleta_brasil.strftime('%I:%M %p')

    if hora_coleta.startswith('0'):  # Se a hora esta 01:00 ele coloca 1:00
        hora_coleta = hora_coleta[1:]

    # Obtém o campo Data e Hora de entrega da Planilha
    data_hora_entrega = planilha_carregada.loc[i,'Previsão de Entrega']

    # Converte a data e hora da coleta para o fuso horário do Brasil
    data_hora_entrega_brasil = data_hora_entrega.replace(tzinfo=fuso_horario_brasil)

    # Parseando as informaçoes de data e hora ajustadas para o fuso horário do Brasil
    dia_entrega = data_hora_entrega_brasil.strftime('%d')
    mes_entrega = data_hora_entrega_brasil.strftime('%b')
    ano_entrega = data_hora_entrega_brasil.strftime('%Y')
    hora_entrega = data_hora_entrega_brasil.strftime('%I:%M %p')

    if hora_entrega.startswith('0'):  # Se a hora esta 01:00 ele coloca 1:00
        hora_entrega = hora_entrega[1:]

  
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
            
        case 335060: # Piex
            loop_transportadora = 16
            
                    
    # Aguarda 5 segundos para fazer voltar para a clicar no search
    time.sleep(espera_longa)

    # Clicando em Search
    navegador.find_element('xpath','//*[@id="left_navigation"]/ul/li[4]/a').click()
    time.sleep(espera_longa)


    """     Preenchendo as informações 
                   em cada campo          """


    # Campo PFR e depois clica em search 
    navegador.find_element('xpath','//*[@id="pfNumber"]').send_keys(pfr)
    time.sleep(espera_media)
    navegador.find_element('xpath','//*[@id="content_center"]/table/tbody/tr[10]/td/center/a[1]').click()
    time.sleep(espera_longa)

    # CLicando na PRF localizada
    navegador.find_element('xpath','//*[@id="table01"]/tbody/tr/td[1]/a').click()
    time.sleep(espera_longa)

    # Bloqueando o Scroll do mouse para evitar erro

    listener_mouse = mouse.Listener(on_scroll=bloquear_scroll)
    listener_mouse.start()  # Inicia o ouvinte do mouse para travar o scroll caso acionado


    # Buscando o Carrier na lista
    navegador.find_element('xpath','//*[@id="pendingConfList0.carrier"]').click()
    
    # Clicando com a seta \/ para selecionar a transportadora de acordo com o codigo
    count = 0
    while (count < loop_transportadora):
        navegador.find_element('xpath','//*[@id="pendingConfList0.carrier"]').send_keys(Keys.DOWN)
        count += 1

    time.sleep(espera_media)

    listener_mouse.stop() # Finaliza o ouvinte do mouse para liberar o scroll

    # Preenchendo o Tipo de numero de referencia
    navegador.find_element('xpath','//*[@id="pendingConfList0.referenceType"]').send_keys(tipo_numero_referencia)
    time.sleep(espera_curta)

    # Preenchendo o CTe
    navegador.find_element('xpath','//*[@id="ConfirmTD_0"]/fieldset/table/tbody/tr[4]/td[2]/input').send_keys(cte)
    time.sleep(espera_curta)

    # Preenchendo o Valor do Frete
    navegador.find_element('xpath','//*[@id="pendingConfList0.invoiceAmount"]').send_keys(valor_frete)
    time.sleep(espera_curta)

    # Preenchendo o currency
    navegador.find_element('xpath','//*[@id="pendingConfList0.currencyCode"]').send_keys(currency)
    time.sleep(espera_curta)
    
    # Preenchendo o peso
    navegador.find_element('xpath','//*[@id="ConfirmTD_0"]/fieldset/table/tbody/tr[7]/td[2]/input').send_keys(peso_formatado)
    time.sleep(espera_curta)
    
    # Preenchendo o measure
    navegador.find_element('xpath','//*[@id="pendingConfList0.unitOfMeasure"]').send_keys(measure)
    time.sleep(espera_curta)
    
    # Preenchendo Data de Coleta
    navegador.find_element('xpath','//*[@id="pendingConfList0.pickupETADate.dayVal"]').send_keys(dia_coleta)
    time.sleep(espera_curta)
    
    navegador.find_element(By.NAME,'pendingConfList0.pickupETADate.monVal').send_keys(mes_coleta)
    time.sleep(espera_curta)

    navegador.find_element(By.NAME,'pendingConfList0.pickupETADate.yearVal').send_keys(ano_coleta)     
    time.sleep(espera_curta)    

    # Preenchendo o horario
    navegador.find_element(By.NAME,'pendingConfList0.pickupETATime').send_keys(hora_coleta)
     
   # Preenchendo Data de Entrega
    navegador.find_element('xpath','//*[@id="pendingConfList0.deliveryETADate.dayVal"]').send_keys(dia_entrega)     
    time.sleep(espera_curta)

    navegador.find_element(By.NAME,'pendingConfList0.deliveryETADate.monVal').send_keys(mes_entrega)     
    time.sleep(espera_curta)

    navegador.find_element(By.NAME,'pendingConfList0.deliveryETADate.yearVal').send_keys(ano_entrega)     
    time.sleep(espera_curta)

    navegador.find_element(By.NAME,'pendingConfList0.deliveryETATime').click()
    time.sleep(espera_curta)
    navegador.find_element(By.NAME,'pendingConfList0.deliveryETATime').send_keys(hora_entrega)     
    time.sleep(espera_curta)

    # Escrevendo os Comments 
    navegador.find_element(By.NAME,'pendingConfList0.comments').send_keys(comments)
    time.sleep(espera_curta)

    lista_pfr_preenchidas.append(pfr)
    print(f"PRF's preenchidas no site: {lista_pfr_preenchidas}")
    print("Quantidade de PRF's preenchidas",len(lista_pfr_preenchidas))
    
    # Clicando no botão de Submit
    navegador.find_element('xpath','//*[@id="content_center"]/div[2]/div[4]/div/a[3]').click()


   

print("Finalizou")