import json

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

    def realizar_consulta(self):
        consulta = "SELECT * FROM usuario"
        cursor = self.conexao.cursor()

        try:
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            return resultado
        except mysql.connector.Error as err:
            print(f"Erro ao consultar a tabela usuario: {err}")
            return None
        finally:
            cursor.close()


# Exemplo de uso:
conexao_bd = ConexaoBancoDados("localhost", "root", "1234", "sql_json")
conexao_bd.conectar()
usuarios = conexao_bd.realizar_consulta()

for usuario in usuarios:
    usuario_json = json.dumps(usuario, indent=4)
    print(usuario_json)
