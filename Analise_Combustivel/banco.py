import json
from datetime import datetime
from arquivoxlsx import ArquivoXlsx
import mysql.connector


class ConexaoBancoDados:
    def __init__(self, host, usuario, senha, banco_de_dados):
        self.host = host
        self.usuario = usuario
        self.senha = senha
        self.banco_de_dados = banco_de_dados
        self.conexao = None

    def conectar(self):
        try:
            self.conexao = mysql.connector.connect(
                host=self.host,
                user=self.usuario,
                password=self.senha,
                database=self.banco_de_dados
            )
            print("Conexão estabelecida com sucesso")
            return self.conexao

        except mysql.connector.Error as err:
            print(f"Não foi possível conectar ao Banco de Dados {err}")
            return None

    def desconectar(self):
        if self.conexao:
            self.conexao.close()
            print("Conexão interrompida com sucesso")



    def insert_Banco(self):

        # Abrindo o arquivo XLSX e ignorando as 10 primeiras linhas
        arquivo = ArquivoXlsx()
        planilha = arquivo.carregar_planilha()


        conexao = self.conectar()

        if conexao:

            # Criando um cursor
            cursor = conexao.cursor()

            for index, row in planilha.iterrows():
                data_da_colecao = datetime.strftime(row['DATA DA COLETA'], '%Y/%m/%d')
                consulta = """ 
                
                    SELECT COUNT (*) FROM revenda_combustiveis
                    WHERE cnpj = %s
                    AND produto = %s
                    AND data_da_coleta = %s
                
                """

                cursor.execute(consulta, (row['CNPJ'], row['PRODUTO'], data_da_colecao))
                resultado = cursor.fetchone()

                if resultado[0] > 0:

                    print(f"Já existe um registro com o CNPJ {row['CNPJ']}, Produto {row['PRODUTO']} e Data {data_da_colecao}. Não será inserido.")

                else:
                    insercao = """
                    
                        INSERT INTO revenda_combustiveis (cnpj, razao,
                        municipio, estado, bandeira, produto, unidade_de_medida, preco_de_revenda, data_da_coleta)
                        
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        
                                """
                    # Converter a data para o formato 'YYYY-MM-DD'
                    data_da_colecao = datetime.strftime(row['DATA DA COLETA'], '%Y/%m/%d')

                    dados_to_insert = []
                    dados = (
                        row['CNPJ'],
                        row['RAZÃO'],
                        row['MUNICÍPIO'],
                        row['ESTADO'],
                        row['BANDEIRA'],
                        row['PRODUTO'],
                        row['UNIDADE DE MEDIDA'],
                        row['PREÇO DE REVENDA'],
                        data_da_colecao  # Data convertida para o formato 'YYYY-MM-DD'
                    )
                    dados_to_insert.append(dados)
                    cursor.executemany(insercao, dados_to_insert)

            # Comitar as inserções
            conexao.commit()
            print("Processo Finalizado")




