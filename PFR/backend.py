import http.client

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import pytz
from pynput import mouse
import math


class AutomacaoPfr:
    def __init__(self):
        # Variaveis Globais
        self.caminho_planilha = r"C:\Users\Gabriel Nathan Dias\OneDrive - Grupo Mirassol\RPA\PFR\Relatorio mensal PFR-RPA.xlsx"

        # Variaveis de Login
        self.login = "YFAM2IY"
        self.senha = "j918200_Mm123"

        # Lista PFR Preenchidas
        self.lista_pfr_preenchidas = []
        self.lista_pfr_naorealizadas = []

        # Delays
        self.espera_curta = 0.5
        self.espera_media = 1.5
        self.espera_longa = 7
        self.espera_login = 30

        # Service Navegador
        self.service = Service(ChromeDriverManager().install())
        self.navegador = None
        self.link = "https://jdsn-pft.deere.com/pft/servlet/com.deere.u90242.premiumfreight.view.servlets.PremiumFreightServlet"

        # Dados da planilha
        self.pfr = 0
        self.codigo_transportadora = 0
        self.loop_transportadora = 0
        self.tipo_numero_referencia = ""
        self.cte = ""
        self.valor_frete = 0
        self.currency = ""
        self.peso_formatado = 0
        self.measure = ""
        self.comments = ""
        self.dia_coleta = ""
        self.mes_coleta = ""
        self.ano_coleta = ""
        self.hora_coleta = ""
        self.dia_entrega = ""
        self.mes_entrega = ""
        self.ano_entrega = ""
        self.hora_entrega = ""

    def set_callback(self, callback):
        self.callback = callback

    def add_to_list_pfr_preenchidas(self, pfr):
        self.lista_pfr_preenchidas.append(pfr)
        if self.callback:
            self.callback(pfr)

    def bloquear_scroll(self, x, y, dx, dy):
        return False

    def carregar_planilha(self):
        try:
            caminho_planilha = self.caminho_planilha.strip().replace('"', '')
            planilha = pd.read_excel(caminho_planilha)
            total_linhas = len(planilha)
            return planilha, total_linhas
        except FileNotFoundError:
            print(f"Arquivo não encontrado no caminho: {self.caminho_planilha}")
            return None

    def iniciar_navegador(self):
        try:
            # Preparando para abrir o navegador
            self.navegador = webdriver.Chrome(service=self.service)
            link_site = self.link
            self.navegador.get(link_site)

            # Fazendo Login no site

            time.sleep(self.espera_longa)
            self.navegador.find_element('xpath', '//*[@id="okta-signin-username"]').send_keys(self.login)
            time.sleep(0.5)
            self.navegador.find_element('xpath', '//*[@id="okta-signin-password"]').send_keys(self.senha)
            time.sleep(0.5)
            self.navegador.find_element('xpath', '//*[@id="okta-signin-submit"]').click()
            time.sleep(self.espera_longa)
            self.navegador.find_element('xpath', '//*[@id="form66"]/div[1]/div[2]/a').click()
            time.sleep(self.espera_login)
        except (ConnectionRefusedError, http.client.RemoteDisconnected):
            print("Aplicação Encerrada")

    def fechar_navegador(self):
        if self.navegador:
            self.navegador.quit()
            self.service.stop()
            print("Navegador finalizado !")

        else:
            print("Navegador não iniciado !")

    def iniciar_automacao(self):
        # Processando os dados da planilha
        planilha_carregada = self.carregar_planilha()[0]

        if planilha_carregada is not None:
            print("Planilha carregada !")

        # Laço para rodar todas as linhas da planilha
        for i, self.pfr in enumerate(planilha_carregada["PFR"]):
            self.codigo_transportadora = planilha_carregada.loc[i, 'Codigo_Transportadora']
            self.tipo_numero_referencia = "Carrier Pro"
            self.cte = planilha_carregada.loc[i, 'CT-e']
            self.valor_frete = planilha_carregada.loc[i, 'Valor do Frete']
            self.currency = "BRL"
            peso1 = planilha_carregada.loc[i, 'Peso']
            self.peso_formatado = "{:.2f}".format(peso1)
            self.measure = "KG"
            self.comments = str(planilha_carregada.loc[i, 'Observações'])
            if pd.isnull(self.comments):
                self.comments = "-"

            if self.peso_formatado.startswith("0"):
                self.peso_formatado = "1"

            # Tratamento de Data e Hora

            # Pegando fuso horário do Brasil
            fuso_horario_brasil = pytz.timezone('America/Sao_Paulo')

            # Obtém o campo Data e Hora de Coleta da Planilha sem formatacao
            data_hora_coleta = planilha_carregada.loc[i, 'Data e Horário da Coleta']

            # Converte a data e hora da coleta para o fuso horário do Brasil
            data_hora_coleta_brasil = data_hora_coleta.replace(tzinfo=fuso_horario_brasil)

            # Parseando as informaçoes de data e hora ajustadas para o fuso horário do Brasil
            self.dia_coleta = data_hora_coleta_brasil.strftime('%d')
            self.mes_coleta = data_hora_coleta_brasil.strftime('%b')
            self.ano_coleta = data_hora_coleta_brasil.strftime('%Y')
            self.hora_coleta = data_hora_coleta_brasil.strftime('%I:%M %p')

            if self.hora_coleta.startswith('0'):  # Se a hora esta 01:00 ele coloca 1:00
                self.hora_coleta = self.hora_coleta[1:]

            # Obtém o campo Data e Hora de entrega da Planilha
            data_hora_entrega = planilha_carregada.loc[i, 'Previsão de Entrega']

            # Converte a data e hora da coleta para o fuso horário do Brasil
            data_hora_entrega_brasil = data_hora_entrega.replace(tzinfo=fuso_horario_brasil)
            if pd.isnull(data_hora_entrega_brasil):
                print("")

            else:
                # Parseando as informaçoes de data e hora ajustadas para o fuso horário do Brasil
                self.dia_entrega = data_hora_entrega_brasil.strftime('%d')
                self.mes_entrega = data_hora_entrega_brasil.strftime('%b')
                self.ano_entrega = data_hora_entrega_brasil.strftime('%Y')
                self.hora_entrega = data_hora_entrega_brasil.strftime('%I:%M %p')

            if self.hora_entrega.startswith('0'):  # Se a hora esta 01:00 ele coloca 1:00
                self.hora_entrega = self.hora_entrega[1:]

            # Descobrindo a quantidade de Looping da seleção da transportadora
            match self.codigo_transportadora:
                case 372052:  # ARMANI
                    self.loop_transportadora = 31

                case 375317:  # VF
                    self.loop_transportadora = 37

                case 361822:  # MODULAR
                    self.loop_transportadora = 26

                case 316937:  # TW
                    self.loop_transportadora = 13

                case 335060:  # Piex
                    self.loop_transportadora = 16

                case 359070:  # Expresso Mirassol
                    self.loop_transportadora = 24

            # Se um desses itens esta vazio ele ignora e salva numa lista de nao realizados
            if (pd.isnull(self.codigo_transportadora) or (pd.isnull(self.pfr)) or
                    (pd.isnull(data_hora_entrega_brasil))
                    or (pd.isnull(self.cte))):
                i += 1
                print("Lista de Arquivos Faltantes")
                self.lista_pfr_naorealizadas.append(("Linha", i, "N° PFR ", self.pfr))
                print(self.lista_pfr_naorealizadas)
                continue

            self.preencher_formulario()

            return total_linhas

        self.navegador.quit()
        self.service.stop()

    def preencher_formulario(self):
        time.sleep(self.espera_longa)

        try:
            try:  # Clicar em Search
                self.navegador.find_element('xpath', '//*[@id="left_navigation"]/ul/li[4]/a').click()
                time.sleep(3)

            except selenium.common.exceptions.NoSuchElementException:
                time.sleep(self.espera_longa)
                self.navegador.find_element('xpath', '//*[@id="left_navigation"]/ul/li[4]/a').click()

            # Digitando a PFR
            self.navegador.find_element('xpath', '//*[@id="pfNumber"]').send_keys(self.pfr)

            # Clicando no search final da pag
            self.navegador.find_element('xpath', '//*[@id="content_center"]/table/tbody/tr[10]/td/center/a[1]').click()
            time.sleep(self.espera_longa)

            # Clicando na PFR encontrada
            self.navegador.find_element('xpath', '//*[@id="table01"]/tbody/tr/td[1]/a').click()
            time.sleep(self.espera_longa)

            listener_mouse = mouse.Listener(on_scroll=self.bloquear_scroll)
            listener_mouse.start()  # Bloqueia o Scroll do mouse para evitar erro

            # Clicando na lista de carrier
            self.navegador.find_element('xpath', '//*[@id="pendingConfList0.carrier"]').click()

            # Apertando a seta para baixo ate o transportador correto
            count_carrier = 0

            while count_carrier < self.loop_transportadora:
                self.navegador.find_element('xpath', '//*[@id="pendingConfList0.carrier"]').send_keys(Keys.DOWN)
                count_carrier += 1

            time.sleep(self.espera_curta)
            listener_mouse.stop()

            # Preenchendo o tipo de numero de referencia
            self.navegador.find_element('xpath', '//*[@id="pendingConfList0.referenceType"]').send_keys(
                self.tipo_numero_referencia)
            time.sleep(self.espera_curta)

            # Preenchendo o CTe
            self.navegador.find_element('xpath',
                                        '//*[@id="ConfirmTD_0"]/fieldset/table/tbody/tr[4]/td[2]/input').send_keys(
                self.cte)
            time.sleep(self.espera_curta)

            # Preenchendo o Valor do Frete
            self.navegador.find_element('xpath', '//*[@id="pendingConfList0.invoiceAmount"]').send_keys(
                str(self.valor_frete))
            time.sleep(self.espera_curta)

            # Preenchendo o currency
            self.navegador.find_element('xpath', '//*[@id="pendingConfList0.currencyCode"]').send_keys(self.currency)
            time.sleep(self.espera_curta)

            # Preenchendo o peso
            self.navegador.find_element('xpath',
                                        '//*[@id="ConfirmTD_0"]/fieldset/table/tbody/tr[7]/td[2]/input').send_keys(
                self.peso_formatado)
            time.sleep(self.espera_curta)

            # Preenchendo o measure
            self.navegador.find_element('xpath', '//*[@id="pendingConfList0.unitOfMeasure"]').send_keys(self.measure)
            time.sleep(self.espera_curta)

            # Preenchendo Data de Coleta
            self.navegador.find_element('xpath', '//*[@id="pendingConfList0.pickupETADate.dayVal"]').send_keys(
                self.dia_coleta)
            time.sleep(self.espera_curta)

            self.navegador.find_element(By.NAME, 'pendingConfList0.pickupETADate.monVal').send_keys(self.mes_coleta)
            time.sleep(self.espera_curta)

            self.navegador.find_element(By.NAME, 'pendingConfList0.pickupETADate.yearVal').send_keys(self.ano_coleta)
            time.sleep(self.espera_curta)

            # Preenchendo o horario
            self.navegador.find_element(By.NAME, 'pendingConfList0.pickupETATime').send_keys(self.hora_coleta)

            # Preenchendo Data de Entrega
            self.navegador.find_element('xpath', '//*[@id="pendingConfList0.deliveryETADate.dayVal"]').send_keys(
                self.dia_entrega)
            time.sleep(self.espera_curta)

            self.navegador.find_element(By.NAME, 'pendingConfList0.deliveryETADate.monVal').send_keys(self.mes_entrega)
            time.sleep(self.espera_curta)

            self.navegador.find_element(By.NAME, 'pendingConfList0.deliveryETADate.yearVal').send_keys(self.ano_entrega)
            time.sleep(self.espera_curta)

            self.navegador.find_element(By.NAME, 'pendingConfList0.deliveryETATime').click()
            time.sleep(self.espera_curta)

            # Preenchendo a hora de entrega
            self.navegador.find_element(By.NAME, 'pendingConfList0.deliveryETATime').send_keys(self.hora_entrega)
            time.sleep(self.espera_curta)

            # Escrevendo os Comments
            self.navegador.find_element(By.NAME, 'pendingConfList0.comments').send_keys(self.comments)
            time.sleep(self.espera_curta)

            # Clicando no botão de Submit
            self.navegador.find_element('xpath', '//*[@id="content_center"]/div[2]/div[4]/div/a[3]').click()

            self.add_to_list_pfr_preenchidas(self.pfr)
            print(f"PRF's preenchidas no site: {self.lista_pfr_preenchidas}")

        except (ConnectionRefusedError, http.client.RemoteDisconnected):
            print("Aplicação Encerrada")
