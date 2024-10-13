import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import sqlite3
import os
import sys

# Função para conectar ao banco de dados
def conectar_banco():
    try:
        conn = sqlite3.connect(caminho_banco)
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

# Detecta se está rodando como executável ou como script Python
if getattr(sys, 'frozen', False):
    os.environ["ENVIRONMENT"] = "production"
else:
    os.environ["ENVIRONMENT"] = "development"

# Obtenha o caminho absoluto do diretório atual
basedir = os.path.dirname(os.path.abspath(__file__))

# Definir o caminho do banco de dados com base no ambiente
if os.environ.get("ENVIRONMENT") == "production":
    caminho_banco = "C:/Users/ICARO/Desktop/db/estoque.db"
else:
    caminho_banco = os.path.join(basedir, 'estoque.db')

# Função para centralizar a janela
def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

# Função para abrir a janela de carregar o arquivo
def abrir_janela_carregar():
    janela_carregar = tk.Toplevel()
    janela_carregar.title("Carregar Arquivo XLS")

    # Função para obter a lista de projetos do banco de dados
    def obter_projetos():
        conn = conectar_banco()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM Projetos")
            projetos = cursor.fetchall()
            conn.close()
            if not projetos:
                messagebox.showwarning("Atenção", "Nenhum projeto encontrado no banco de dados.")
            return [projeto[0] for projeto in projetos]
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Falha ao obter projetos: {e}")
            return []

    # Função para verificar se o projeto já tem componentes
    def verificar_componentes(projeto):
        conn = conectar_banco()
        if conn is None:
            return True
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM componentes WHERE id_projeto = (SELECT id FROM Projetos WHERE nome = ?)", (projeto,))
            count = cursor.fetchone()[0]
            conn.close()
            return count > 0
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Falha ao verificar componentes: {e}")
            return True

    # Função para carregar os dados do arquivo XLS no projeto selecionado
    def carregar_dados(arquivo, projeto_selecionado):
        try:
            # Buscar o id_projeto com base no nome do projeto selecionado
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM Projetos WHERE nome = ?", (projeto_selecionado,))
            id_projeto = cursor.fetchone()

            if id_projeto is None:
                messagebox.showerror("Erro", "Projeto não encontrado no banco de dados.")
                return

            id_projeto = id_projeto[0]  # Extrai o id do projeto
            conn.close()

            if verificar_componentes(projeto_selecionado):
                messagebox.showerror("Erro", "Este projeto já possui componentes. A tabela não pode ser carregada.")
                return

            df = pd.read_excel(arquivo)

            colunas_esperadas = ['Código', 'Nome do Componente', 'Quantidade por Placa', 'Quantidade Disponível']
            if not all(col in df.columns for col in colunas_esperadas):
                messagebox.showerror("Erro", "O arquivo XLS não contém as colunas necessárias.")
                return

            conn = conectar_banco()
            if conn is None:
                return

            cursor = conn.cursor()

            for index, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO componentes (id_projeto, codigo, nome, quantidade_por_placa, quantidade_disponivel)
                    VALUES (?, ?, ?, ?, ?)
                """, (id_projeto, row['Código'], row['Nome do Componente'], row['Quantidade por Placa'], row['Quantidade Disponível']))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Dados carregados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar o arquivo: {e}")

    # Função para selecionar o arquivo XLS
    def selecionar_arquivo():
        arquivo = filedialog.askopenfilename(
            title="Selecione um arquivo XLS",
            filetypes=[("Arquivo Excel", "*.xls *.xlsx")]
        )
        if arquivo:
            projeto_selecionado = combobox_projetos.get()
            if projeto_selecionado:
                carregar_dados(arquivo, projeto_selecionado)
            else:
                messagebox.showwarning("Atenção", "Selecione um projeto antes de carregar o arquivo.")

    # Combobox para selecionar o projeto
    label_projeto = tk.Label(janela_carregar, text="Selecione o projeto:")
    label_projeto.pack(pady=10)

    combobox_projetos = ttk.Combobox(janela_carregar, state="readonly")
    combobox_projetos.pack(pady=5)

    # Preencher o combobox com os projetos do banco de dados
    projetos = obter_projetos()
    if projetos:
        combobox_projetos['values'] = projetos

    # Botão para selecionar o arquivo
    botao_selecionar = tk.Button(janela_carregar, text="Selecionar Arquivo", command=selecionar_arquivo)
    botao_selecionar.pack(pady=20)

    janela_carregar.geometry("400x200")
    centralizar_janela(janela_carregar, 400, 200)

    janela_carregar.mainloop()

# Exemplo de uso para abrir a janela
# root = tk.Tk()
# root.withdraw()  # Esconde a janela principal
# abrir_janela_carregar()
