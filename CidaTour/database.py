import mysql.connector

class ConexaoBancoDados:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = '1234'
        self.database = 'cidatour_db'
        self.conn = None

    def conectar(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Conexão bem-sucedida")
        except mysql.connector.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def desconectar(self):
        if self.conn:
            self.conn.close()
            print("Conexão encerrada")


