import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tkinter import ttk
from tkinter import messagebox


class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Divisão de Carteira")
        self.root.geometry("350x180")

        # Variável para armazenar o caminho dos arquivos
        self.caminho_carteira = ""
        self.caminho_relatorio = ""

        self.nomes_ilc = []

        # Adicione um botão para selecionar o arquivo auxiliar
        self.label_carteira = tk.Label(root, text="Carteira Fornecedores:", anchor='w')
        self.label_carteira.pack()

        self.button_auxiliar = tk.Button(root, text="Procurar", command=self.selecionar_carteira, anchor='w')
        self.button_auxiliar.pack()

        # Adicione um botão para selecionar o arquivo do Relatório
        self.label_relatorio = tk.Label(root, text="Relatório Fora de Frequência:", anchor='w')
        self.label_relatorio.pack()

        self.button_relatorio = tk.Button(root, text="Procurar", command=self.selecionar_relatorio, anchor='w')
        self.button_relatorio.pack()

        # Selecionar planejador ILC
        self.label_nomes_ilc = tk.Label(root, text="Planejador ILC:", anchor='w')
        self.label_nomes_ilc.pack()

        self.combobox_nomes_ilc = ttk.Combobox(root, values=sorted(self.nomes_ilc), state="readonly")
        self.combobox_nomes_ilc.pack()

        # Adicione um botão para filtrar os dados
        self.button_filtrar = tk.Button(root, text="Filtrar Dados", command=self.filtrar_dados, anchor='w')
        self.button_filtrar.pack()

    def selecionar_carteira(self):
        self.caminho_carteira = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])
        if self.caminho_carteira:
            self.listar_nomes_planejadoresILC()
            nome_arquivo = os.path.basename(self.caminho_carteira)  # Obtém somente o nome do arquivo
            self.label_carteira.config(text=f"Arquivo Selecionado: {nome_arquivo}", foreground='White', background='Green')

    def selecionar_relatorio(self):
        self.caminho_relatorio = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])
        if self.caminho_relatorio:
            nome_arquivo = os.path.basename(self.caminho_relatorio)  # Obtém somente o nome do arquivo
            self.label_relatorio.config(text=f"Arquivo do Relatório Selecionado: {nome_arquivo}", foreground='White',
                                        background='Green')

    def listar_nomes_planejadoresILC(self):
        if self.caminho_carteira:
            df_carteira = pd.read_excel(self.caminho_carteira, sheet_name='DIVISÃO')
            nomes_ilc = df_carteira['Planejador ILC'].unique()
            self.nomes_ilc = [str(nome) for nome in nomes_ilc if str(nome) != 'nan']
            self.combobox_nomes_ilc['values'] = sorted(self.nomes_ilc)

    def filtrar_dados(self):
        if self.caminho_carteira and self.caminho_relatorio:
            nome_selecionado = self.combobox_nomes_ilc.get()
            if nome_selecionado:
                df_carteira = pd.read_excel(self.caminho_carteira, sheet_name='DIVISÃO')
                df_relatorio = pd.read_excel(self.caminho_relatorio)
                df_relatorio = df_relatorio.rename(columns={'Fornecedor': 'NOME INTEGRATOR'})
                df_auxiliar_filtrado = df_carteira[df_carteira['Planejador ILC'] == nome_selecionado]
                df_completo = df_relatorio.merge(df_auxiliar_filtrado, on='NOME INTEGRATOR', how='inner')

                # Obtenha valores únicos na coluna "MRP Controller Name"
                nomes_planejadoresjd = df_completo['MRP Controller Name'].unique()

                # Pasta de documentos do usuário
                documentos_path = os.path.expanduser('~\\Documents')

                for nome in nomes_planejadoresjd:
                    df_individual = df_completo[df_completo['MRP Controller Name'] == nome]
                    colunas_para_salvar = ['Cliente', 'NOME INTEGRATOR', 'Data programação', 'PN Cliente', 'Status',
                                           'Status Atual', 'Dia', 'Frequência']
                    df_individual = df_individual[colunas_para_salvar]
                    nome_arquivo = os.path.join(documentos_path, f"Fora de Frequencia {nome}.xlsx")
                    df_individual.to_excel(nome_arquivo, index=False)
                    print(f"Dados filtrados para {nome} salvos em {nome_arquivo}")

                messagebox.showinfo(f"Processo finalizado!", "Arquivos salvos em MEUS DOCUMENTOS")

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
