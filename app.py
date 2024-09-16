import tkinter as tk
from tkinter import PhotoImage
import cadastro_projeto
import cadastro_componente
import adicionar_estoque
import listar_componentes
import deletar_componente
import editar_projeto  # Importa o módulo para editar projetos

# Inicialização das listas e dicionários
projetos = []  # Lista de projetos
componentes = {}  # Dicionário para armazenar componentes por projeto

def abrir_cadastro_projeto():
    cadastro_projeto.abrir_janela_cadastro_projeto(projetos, componentes)

def abrir_cadastro_componente():
    cadastro_componente.abrir_janela(projetos, componentes)

def abrir_adicionar_estoque():
    adicionar_estoque.abrir_janela(projetos, componentes)

def abrir_listar_componentes():
    listar_componentes.abrir_aba_listar_componentes(projetos, componentes)

def abrir_deletar_componente():
    deletar_componente.abrir_janela(projetos, componentes)

def abrir_editar_projeto():
    editar_projeto.abrir_janela_editar_projeto(projetos, componentes)

# Criação da janela principal
root = tk.Tk()
root.title("Controle de Estoque")
root.geometry("600x400")

# Adicionando logo
try:
    logo = PhotoImage(file="logo.png")
    logo = logo.subsample(3, 3)
    tk.Label(root, image=logo).grid(row=0, column=0, columnspan=2, pady=10)
    root.logo = logo
except tk.TclError:
    print("Erro ao carregar a imagem do logotipo para a página principal.")

# Adicionando texto abaixo do logotipo
texto = "Controle do estoque de Hardware P&D"
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


# Ajustar as colunas e linhas para expandirem com a janela
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)

# Executando a aplicação
root.mainloop()
