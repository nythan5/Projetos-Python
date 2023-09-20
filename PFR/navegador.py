from selenium import webdriver
import pyperclip
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
import time


service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service)
navegador.get("https://jdsn-pft.deere.com/pft/servlet/com.deere.u90242.premiumfreight.view.servlets.PremiumFreightServlet")

# Aguarda 1minuto para fazer login
time.sleep(60)

# Clicando em search
navegador.find_element('xpath','//*[@id="left_navigation"]/ul/li[4]/a').click()
time.sleep(2)

# Enviando o numero da PRF e dando Enter
navegador.find_element('xpath','//*[@id="pfNumber"]').send_keys(811457)
time.sleep(2)
navegador.find_element('xpath','//*[@id="content_center"]/table/tbody/tr[10]/td/center/a[1]').click()

# CLicando na PRF localizada
navegador.find_element('xpath','//*[@id="table01"]/tbody/tr/td[1]/a').click()
time.sleep(3000000)

# Digitando informações em cada campo 

