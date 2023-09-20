from dados import lista_de_dicionarios

dicionario = lista_de_dicionarios[0]

pfr = dicionario['PFR']
codigo_transportadora = dicionario['Codigo_Transportadora']
tipo_numero_referencia = "Carrier Pro"
cte = dicionario['CT-e']
valor_frete = dicionario['Valor do Frete']
currency = "BRL"
peso = dicionario['Peso']
measure = "KG"

print(pfr)