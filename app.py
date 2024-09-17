import tkinter as tk
from tkinter import PhotoImage
import os
import sys

# Função para obter o caminho correto do banco de dados e outros arquivos
def get_file_path(filename):
    if getattr(sys, 'frozen', False):  # Se estiver rodando como um executável
        base_path = sys._MEIPASS  # Diretório temporário usado pelo PyInstaller
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, filename)

def abrir_cadastro_projeto():
    import cadastro_projeto
    cadastro_projeto.abrir_janela_cadastro_projeto()

def abrir_cadastro_componente():
    import cadastro_componente
    cadastro_componente.abrir_janela()

def abrir_adicionar_estoque():
    import adicionar_estoque
    adicionar_estoque.abrir_janela()

def abrir_listar_componentes():
    import listar_componentes
    projetos = listar_componentes.obter_lista_projetos()
    listar_componentes.abrir_aba_listar_componentes(projetos)

def abrir_deletar_componente():
    import deletar_componente
    deletar_componente.abrir_janela()

def abrir_debitar_componentes():
    import debitar_componentes
    debitar_componentes.debitar_componentes()

# Criação da janela principal
root = tk.Tk()
root.title("Controle de Estoque")
root.geometry("800x500")

# Adicionando logo
try:
    logo_path = get_file_path("logo.png")
    logo = PhotoImage(file=logo_path)
    logo = logo.subsample(3, 3)  # Reduz a imagem para se ajustar ao tamanho da tela
    tk.Label(root, image=logo).grid(row=0, column=0, columnspan=2, pady=10)
    root.logo = logo  # Mantém uma referência ao logo para evitar que o Python o descarte
except tk.TclError:
    print("Erro ao carregar a imagem do logotipo para a página principal.")

# Adicionando texto abaixo do logotipo
texto = "CONTROLE DO ESTOQUE DE HARDWARE P&D"
tk.Label(root, text=texto, font=("Arial", 18)).grid(row=1, column=0, columnspan=2, pady=10)

# Adicionando botões à janela principal
button_cadastrar_projeto = tk.Button(root, text="Cadastrar Projeto", width=20, command=abrir_cadastro_projeto)
button_cadastrar_projeto.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

button_cadastrar_componente = tk.Button(root, text="Cadastrar Componente", width=20, command=abrir_cadastro_componente)
button_cadastrar_componente.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

button_adicionar_estoque = tk.Button(root, text="Adicionar Estoque", width=20, command=abrir_adicionar_estoque)
button_adicionar_estoque.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

button_listar_componentes = tk.Button(root, text="Listar Componentes", width=20, command=abrir_listar_componentes)
button_listar_componentes.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

button_deletar_componente = tk.Button(root, text="Deletar Componente", width=20, command=abrir_deletar_componente)
button_deletar_componente.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

button_debitar_componentes = tk.Button(root, text="Debitar Componentes", width=20, command=abrir_debitar_componentes)
button_debitar_componentes.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

## Remover espaço extra da linha do rodapé
rodape_texto = "Developed by: Icaro Quimaia Rodrigues"
rodape_label = tk.Label(root, text=rodape_texto, font=("Arial", 8), anchor='e')
rodape_label.grid(row=5, column=1, padx=10, pady=0, sticky="se")

# Ajuste as linhas para expandirem corretamente
root.grid_rowconfigure(5, weight=1)  # Deixar o rodapé na última linha

# Ajustar as colunas e linhas para expandirem com a janela
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)

# Imprimir o caminho do banco de dados
print("Caminho do banco de dados:", get_file_path("estoque.db"))

# Executando a aplicação
root.mainloop()
