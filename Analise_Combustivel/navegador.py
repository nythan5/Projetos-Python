import time

import selenium.common.exceptions

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


class BaixarExcel:
    def __init__(self):
        # Service Navegador
        self.service = Service(ChromeDriverManager().install())
        self.navegador = None
        self.link = 'https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/levantamento-de-precos-de-combustiveis-ultimas-semanas-pesquisadas'




    def abri_navegador(self):
        self.navegador = webdriver.Chrome(service=self.service)
        link_site = self.link
        self.navegador.get(link_site)

        time.sleep(2)




        # Ele sai do invólucro criado para forçar um login
        self.navegador.find_element('xpath', '/html/body').click()
        time.sleep(1)
        #self.navegador.find_element('xpath', '//*[@id="parent-fieldname-text"]/ul[1]/li[2]/a')

        self.navegador.find_element('xpath', '//*[@id="parent-fieldname-text"]/ul[1]/li[2]/a')



        time.sleep(90000)





# Criar uma instância da classe BaixarExcel
app = BaixarExcel()

# Chamar o método abri_navegador na instância
app.abri_navegador()
