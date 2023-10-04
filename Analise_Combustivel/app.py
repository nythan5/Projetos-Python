from arquivoxlsx import ArquivoXlsx
from banco import ConexaoBancoDados


if __name__ == "__main__":

    # realizando conexao com o DB
    app = ConexaoBancoDados('localhost', 'root', '1234', 'analise_combustivel')
    app.insert_Banco()



