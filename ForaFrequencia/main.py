import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tkinter import ttk
from tkinter import messagebox


class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Fora de Frequência")

        # Configure o estilo do tema
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Escolha um tema que você prefira

        # Variável para armazenar o caminho dos arquivos
        self.caminho_carteira = ""
        self.caminho_relatorio = ""

        self.nomes_ilc = []

        # Crie estilos de fonte personalizados
        font_style_label = ("Helvetica", 10)
        font_style_button = ("Helvetica", 9)

        # Crie o frame principal para melhorar o espaçamento
        frame = ttk.Frame(root)
        frame.pack(padx=1, pady=1, fill="both", expand=True)

        # Adicione um botão para selecionar o arquivo auxiliar
        self.label_carteira = ttk.Label(frame, text="Carteira Fornecedores:", font=font_style_label)
        self.label_carteira.grid(row=0, column=0, sticky="w", pady=5)

        self.button_auxiliar = ttk.Button(frame, text="Procurar", command=self.selecionar_carteira, style="TButton")
        self.button_auxiliar.grid(row=0, column=4, pady=5)

        # Adicione um botão para selecionar o arquivo do Relatório
        self.label_relatorio = ttk.Label(frame, text="Relatório Fora de Frequência:", font=font_style_label)
        self.label_relatorio.grid(row=1, column=0, sticky="w", pady=5)

        self.button_relatorio = ttk.Button(frame, text="Procurar", command=self.selecionar_relatorio, style="TButton")
        self.button_relatorio.grid(row=1, column=4, pady=5)

        # Selecionar planejador ILC
        self.label_nomes_ilc = ttk.Label(frame, text="Planejador ILC:", font=font_style_label)
        self.label_nomes_ilc.grid(row=2, column=0, sticky="w", pady=5)

        self.combobox_nomes_ilc = ttk.Combobox(frame, values=sorted(self.nomes_ilc), state="readonly")
        self.combobox_nomes_ilc.grid(row=2, column=4, pady=5)

        # Adicione um botão para filtrar os dados
        self.button_filtrar = ttk.Button(frame, text="Filtrar Dados", command=self.filtrar_dados, style="TButton")
        self.button_filtrar.grid(row=3, column=4, columnspan=2, pady=5)

    def selecionar_carteira(self):
        self.caminho_carteira = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])
        if self.caminho_carteira:
            if not self.verificar_abade_divisao():
                messagebox.showerror("Erro", "A aba 'DIVISÃO' não foi encontrada no arquivo selecionado.")
                self.caminho_carteira = ""
                return

            self.listar_nomes_planejadoresILC()
            nome_arquivo = os.path.basename(self.caminho_carteira)
            self.label_carteira.config(text=f"Arquivo Selecionado: {nome_arquivo}")

    def verificar_abade_divisao(self):
        if self.caminho_carteira:
            try:
                xl = pd.ExcelFile(self.caminho_carteira)
                return 'DIVISÃO' in xl.sheet_names
            except Exception as e:
                print(f"Erro ao verificar a aba DIVISÃO: {str(e)}")
        return False

    def selecionar_relatorio(self):
        self.caminho_relatorio = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])
        if self.caminho_relatorio:
            nome_arquivo = os.path.basename(self.caminho_relatorio)
            self.label_relatorio.config(text=f"Arquivo do Relatório Selecionado: {nome_arquivo}")

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

                nomes_planejadoresjd = df_completo['MRP Controller Name'].unique()

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
