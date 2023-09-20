from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
import time
from selenium.webdriver.common.keys import Keys
import pyperclip

service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service)
navegador.get("https://web.whatsapp.com")
<<<<<<< HEAD
time.sleep(30)


=======
time.sleep(20)

mensagem = """Olá! Estou testando a automação de mensagens.
Como você está?(Mensagem de Teste)"""

lista_contatos = ["Meu Numero","Amore Mio","Anotações"]

#Enviar a mensagem para meu proprio numero para depois encaminhar para a lista de contatos
#clicar na lupa
navegador.find_element('xpath','//*[@id="side"]/div[1]/div/div/button/div[2]/span').click()
time.sleep(1.5)

#escrever meu numero
navegador.find_element('xpath','//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p').send_keys("Você")
time.sleep(1)

#dar enter
navegador.find_element('xpath','//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p').send_keys(Keys.ENTER)
time.sleep(1)

#Mandar mensagem para eu mesmo
pyperclip.copy(mensagem)
navegador.find_element('xpath','//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p').send_keys(Keys.CONTROL + "v")
time.sleep(1)
navegador.find_element('xpath','//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p').send_keys(Keys.ENTER)
time.sleep(1)

#calcular a quantidades de vezes necessarias lembrando que envia de 5 em 5 pessoas
qtde_contatos = len(lista_contatos)
if qtde_contatos % 5 == 0:
    qtde_blocos = int(qtde_contatos) / 5
else:
    qtde_blocos = int(qtde_contatos/5) + 1


#seleciona os 5 contatos
for i in range(qtde_blocos):
    i_inicial = i*5
    i_final = (i+1) * 5
    lista_enviar = lista_contatos[i_inicial : i_final]


    from selenium.webdriver.common.action_chains import ActionChains
    #seleciona o box da mensagem ora encaminhar
    lista_elementos =  navegador.find_elements('class name','_2AOIt')
    for item in lista_elementos:
        mensagem = mensagem.replace('\n',"")
        texto = item.text.replace('\n',"")
        if mensagem in texto:
            elemento = item
            break

    #seleciona a mensagem que vc mandou pra vc mesmo pra encaminhar ela
    ActionChains(navegador).move_to_element(elemento).perform()
    time.sleep(2)
    elemento.find_element('class name','_3u9t-').click()
    time.sleep(2)
    #clica no botao de encaminhar
    navegador.find_element('xpath','//*[@id="app"]/div/span[4]/div/ul/div/li[3]/div').click()
    time.sleep(2)

    for nome in lista_enviar:
        navegador.find_element('xpath','//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div[1]/p').send_keys("nome")
        time.sleep(1)
        #dar enter
        navegador.find_element('xpath','//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div[1]/p').send_keys(Keys.ENTER)
        time.sleep(1)
        #apagar o nome escrito
        navegador.find_element('xpath','//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div[1]/p').send_keys(Keys.DELETE)
        time.sleep(1)


#clicando em enviar
navegador.find_element('xpath','//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/span/div/div/div/span').click()
time.sleep(5)
>>>>>>> dc771c0c230b28d1c343242e69331776e718224f
