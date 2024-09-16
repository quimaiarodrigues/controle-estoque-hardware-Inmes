import tkinter as tk
from tkinter import PhotoImage
import cadastro_projeto
import cadastro_componente
import adicionar_estoque
import listar_componentes

# Inicialização das listas e dicionários
projetos = []  # Lista de projetos
componentes = {}  # Dicionário para armazenar componentes por projeto

def abrir_cadastro_projeto():
    cadastro_projeto.abrir_janela(projetos, componentes)

def abrir_cadastro_componente():
    cadastro_componente.abrir_janela(projetos, componentes)

def abrir_adicionar_estoque():
    adicionar_estoque.abrir_janela(projetos, componentes)

def abrir_listar_componentes():
    listar_componentes.abrir_aba_listar_componentes(projetos, componentes)

# Criação da janela principal
root = tk.Tk()
root.title("Controle de Estoque")
root.geometry("600x350")

# Adicionando logo
try:
    logo = PhotoImage(file="logo.png")
    logo = logo.subsample(3, 3)
    tk.Label(root, image=logo).pack(pady=10)
    root.logo = logo
except tk.TclError:
    print("Erro ao carregar a imagem do logotipo para a página principal.")

# Adicionando texto abaixo do logotipo
texto = "Controle do estoque de Hardware P&D"
tk.Label(root, text=texto, font=("Arial", 18)).pack(pady=10)

# Adicionando botões à janela principal
tk.Button(root, text="Cadastrar Projeto", command=abrir_cadastro_projeto).pack(pady=10)
tk.Button(root, text="Cadastrar Componente", command=abrir_cadastro_componente).pack(pady=10)
tk.Button(root, text="Adicionar Estoque", command=abrir_adicionar_estoque).pack(pady=10)
tk.Button(root, text="Listar Componentes", command=abrir_listar_componentes).pack(pady=10)

# Executando a aplicação
root.mainloop()
