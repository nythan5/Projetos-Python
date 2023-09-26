from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pynput import mouse
import time
import pandas as pd
import pytz
import math

# Variáveis Globais
caminho_planilha = r"C:\Users\Gabriel Nathan Dias\Desktop\Relatorio mensal PFR-RPA.xls"
login = "YFAM2IY"
senha = "j918200_Mm123"
lista_pfr_preenchidas = []

# delay's 
espera_curta = 0.5
espera_media = 1.5
espera_longa = 7
espera_login = 30

# funções 