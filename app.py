import os
import tkinter as tk
from tkinter import PhotoImage, messagebox
import sqlite3
import sys

# Função para obter o caminho correto do banco de dados e outros arquivos
def get_file_path(filename):
    if getattr(sys, 'frozen', False):  # Se estiver rodando como um executável
        base_path = sys._MEIPASS  # Diretório temporário usado pelo PyInstaller
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, filename)

def conectar_banco():
    try:
        conn = sqlite3.connect(get_file_path('estoque.db'))
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

def verificar_estoque_minimo():
    conn = conectar_banco()
    if conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.nome, SUM(c.quantidade_disponivel), p.limite_minimo
                FROM Projetos p
                JOIN Componentes c ON p.id = c.id_projeto
                GROUP BY p.id
            """)
            projetos = cursor.fetchall()

            projetos_com_estoque_baixo = [
                p[0] for p in projetos if p[1] is not None and p[1] <= p[2]
            ]

            if projetos_com_estoque_baixo:
                projetos = ', '.join(projetos_com_estoque_baixo)
                mensagem = f"AVISO: Estoque insuficiente para os projetos: {projetos}"
            else:
                # Verifica se existe algum projeto cadastrado
                if projetos:
                    mensagem = ""  # Não exibe mensagem se há projetos cadastrados
                else:
                    mensagem = "Nenhum projeto cadastrado."  # Exibe mensagem se não houver projetos

            # Atualiza o label de status com a mensagem
            status_label.config(text=mensagem)
    
    # Reexecutar a função após 1 segundo
    root.after(10000, verificar_estoque_minimo)


# Função para abrir diferentes janelas
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
root.geometry("810x500")

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

# Adicionando um label para mostrar o status de estoque
status_label = tk.Label(root, text="Verificando estoque...", font=("Arial", 12), fg="red")
status_label.grid(row=5, column=0, columnspan=2, pady=10)

# Chama a função para verificar o estoque mínimo inicialmente
verificar_estoque_minimo()

# Remover espaço extra da linha do rodapé
rodape_texto = "Developed by: Icaro Quimaia Rodrigues"
rodape_label = tk.Label(root, text=rodape_texto, font=("Arial", 8), anchor='e')
rodape_label.grid(row=6, column=1, padx=10, pady=0, sticky="se")

root.grid_rowconfigure(6, weight=1)  # Deixar o rodapé na última linha

# Ajustar as colunas e linhas para expandirem com a janela
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)

# Inicia a interface principal
root.mainloop()
