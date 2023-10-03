import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class BaixarExcel:
    def __init__(self):
        # Service Navegador
        self.service = Service(ChromeDriverManager().install())
        self.navegador = None
        self.link = "https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/levantamento-de-precos-de-combustiveis-ultimas-semanas-pesquisadas"

    def abri_navegador(self):
        self.navegador = webdriver.Chrome(service=self.service)
        link_site = self.link
        self.navegador.get(link_site)

        # Texto que ele vai procurar para clicar no link


        time.sleep(90000)





# Criar uma instância da classe BaixarExcel
app = BaixarExcel()

# Chamar o método abri_navegador na instância
app.abri_navegador()
