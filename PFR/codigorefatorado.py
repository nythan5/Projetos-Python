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
        self.caminho_planilha = r"C:\Users\gnd20\Downlds\Entradas  2023.xlsx"

        # Variaveis de Login
        self.login = "YFAM2IY"
        self.senha = "j918200_Mm123"

        # Lista PFR Preenchidas
        self.lista_pfr_preenchidas = []

        # Delays
        self.espera_curta = 0.5
        self.espera_media = 1.5
        self.espera_longa = 7
        self.espera_login = 30

    def bloquear_scroll(self, x, y, dx, dy):
            return False

    def carregar_planilha(self, caminho_planilha):
        try:
            caminho_planilha = caminho_planilha.strip().replace('"', '')
            planilha = pd.read_excel(caminho_planilha)
            return planilha
        except FileNotFoundError:
            print(f"Arquivo não encontrado no caminho: {caminho_planilha}")




if __name__ == "__main__":
    app = AutomacaoPfr()
    planilha_carregada = app.carregar_planilha(app.caminho_planilha)
    print(planilha_carregada)


