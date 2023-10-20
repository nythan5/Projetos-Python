from CidaTour.clientes.cadastroClientes import CadastroClientes
from CidaTour.clientes.listarClientes import ListaClientes
from CidaTour.viagens.cadastroViagens import CadastroViagens
from CidaTour.viagens.listarViagens import ListaViagens
from CidaTour.viagens.viagens_clientes import AssociarClientesViagem

cadastro_cliente = CadastroClientes()
lista_clientes = ListaClientes()
cadastro_viagem = CadastroViagens()
lista_viagens = ListaViagens()
associar_viagem = AssociarClientesViagem()


if __name__ == '__main__':
    cadastro_cliente.janela_cadastro.mainloop()
    lista_clientes.janela_lista.mainloop()
    cadastro_viagem.janela_cadastro.mainloop()
    lista_viagens.janela_lista.mainloop()
    associar_viagem.janela.mainloop()

