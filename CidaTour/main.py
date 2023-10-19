from CidaTour.clientes.cadastroClientes import CadastroClientes
from CidaTour.clientes.listarClientes import ListaClientes

cadastro = CadastroClientes()
lista_clientes = ListaClientes()

if __name__ == '__main__':
    cadastro.janela_cadastro.mainloop()
    lista_clientes.janela_lista.mainloop()
