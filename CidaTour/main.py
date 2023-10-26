from ttkthemes.themed_tk import ThemedTk
import tkinter as tk
from tkinter import ttk
from CidaTour.clientes.cadastroClientes import CadastroClientes
from CidaTour.clientes.listarClientes import ListaClientes
from CidaTour.viagens.cadastroViagens import CadastroViagens
from CidaTour.viagens.listarViagens import ListaViagens
from CidaTour.viagens.pagamentoViagem import RegistroPagamentoViagem
from CidaTour.viagens.viagens_clientes import AssociarClientesViagem
from CidaTour.viagens.listarViagensAssociadas import ListarClientesViagem


class TelaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("CidaTour - Gerenciamento")

        # Crie um Frame principal
        self.frame_principal = ttk.Frame(self.root, padding=10)
        self.frame_principal.grid(row=0, column=0, padx=1, pady=1)

        ######################ZONA CLIENTE######################

        # Crie uma LabelFrame para "Clientes" na coluna 1
        self.frame_clientes = ttk.LabelFrame(self.frame_principal, text="Clientes", labelanchor='n')
        self.frame_clientes.grid(row=0, column=0, padx=15, pady=15, sticky="nw")

        # Crie botões para abrir as telas relacionadas a clientes
        ttk.Button(self.frame_clientes, text="Cadastro de Clientes",
                   command=self.abrir_cadastro_clientes).grid(row=0, column=0, pady=5, padx=5)

        ttk.Button(self.frame_clientes, text="Listar Clientes",
                   command=self.abrir_lista_clientes).grid(row=1, column=0, pady=5, padx=5)

        ######################ZONA VIAGENS######################

        # Crie uma LabelFrame para "Viagens" na coluna 2
        self.frame_viagens = ttk.LabelFrame(self.frame_principal, text="Viagens", labelanchor='n')
        self.frame_viagens.grid(row=0, column=1, padx=15, pady=15, sticky="nw")

        # Crie botões para abrir as telas relacionadas a viagem
        ttk.Button(self.frame_viagens, text="Cadastro de Viagens",
                   command=self.abrir_cadastro_viagens).grid(row=0, column=1, pady=5, padx=5)

        ttk.Button(self.frame_viagens, text="Listar Viagens",
                   command=self.abrir_lista_viagens).grid(row=1, column=1, pady=5, padx=5)

        ######################ZONA CLIENTE & VIAGEM######################

        # Crie uma LabelFrame para "Cliente & Viagem" na coluna 3
        self.frame_viagens = ttk.LabelFrame(self.frame_principal, text="Cliente & Viagem", labelanchor='n')
        self.frame_viagens.grid(row=0, column=2, padx=15, pady=15, sticky="nw")

        # Crie botões para abrir as telas relacionadas a cliente & viagem
        ttk.Button(self.frame_viagens, text="Vincular Cliente & Viagem",
                   command=self.abrir_associar_cliente_viagem).grid(row=0, column=2, pady=5, padx=5)

        ttk.Button(self.frame_viagens, text="Listar Cliente & Viagem",
                   command=self.abrir_lista_clientes_associados_viagens).grid(row=1, column=2, pady=5, padx=5)


        ######################ZONA PAGAMENTOS######################

        # Crie uma LabelFrame para "Viagens" na coluna 2
        self.frame_pagamentos = ttk.LabelFrame(self.frame_principal, text="Financeiro", labelanchor='n')
        self.frame_pagamentos.grid(row=0, column=3, padx=15, pady=15, sticky="nw")

        # Crie botões para abrir as telas relacionadas a clientes
        ttk.Button(self.frame_pagamentos, text="Cadastro de Pagamentos",
                   command=self.abrir_registro_pagamentos).grid(row=0, column=3, pady=5, padx=5)



    def abrir_cadastro_clientes(self):
        CadastroClientes()

    def abrir_lista_clientes(self):
        ListaClientes()

    def abrir_cadastro_viagens(self):
        CadastroViagens()

    def abrir_lista_viagens(self):
        ListaViagens()

    def abrir_associar_cliente_viagem(self):
        AssociarClientesViagem()

    def abrir_lista_clientes_associados_viagens(self):
        ListarClientesViagem()

    def abrir_registro_pagamentos(self):
        RegistroPagamentoViagem()




if __name__ == '__main__':
    root = ThemedTk(theme="clam")
    app = TelaPrincipal(root)
    root.mainloop()
