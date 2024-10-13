import os
import tkinter as tk
from tkinter import PhotoImage, messagebox
import sqlite3
import sys


# Função para conectar ao banco de dados
def conectar_banco():
    try:
        # Use o caminho absoluto para garantir que o executável encontre o banco de dados
        conn = sqlite3.connect(caminho_banco)
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados App: {e}")
        return None

# Detecta se está rodando como executável ou como script Python
if getattr(sys, 'frozen', False):
    # Está rodando como um executável
    os.environ["ENVIRONMENT"] = "production"
else:
    # Está rodando como script Python normal
    os.environ["ENVIRONMENT"] = "development"

# Obtenha o caminho absoluto do diretório atual
basedir = os.path.dirname(os.path.abspath(__file__))

# Definir o caminho do banco de dados com base no ambiente
if os.environ.get("ENVIRONMENT") == "production":
    caminho_banco = "C:/Users/ICARO/Desktop/db/estoque.db"
else:
    caminho_banco = os.path.join(basedir, 'estoque.db')

    
def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def verificar_estoque_minimo():
    conn = conectar_banco()
    if conn:
        with conn:
            cursor = conn.cursor()
            # Seleciona o nome dos projetos, quantidade disponível, quantidade por placa e limite mínimo
            cursor.execute("""
                SELECT p.id, p.nome, c.quantidade_disponivel, c.quantidade_por_placa, p.limite_minimo
                FROM Projetos p
                JOIN Componentes c ON p.id = c.id_projeto
            """)
            componentes = cursor.fetchall()

            projetos_com_estoque_baixo = set()
            mensagem = ""

            for projeto_id, projeto_nome, quantidade_disponivel, quantidade_por_placa, limite_minimo in componentes:
                if quantidade_disponivel is not None and quantidade_por_placa is not None:
                    # Calcular montagens possíveis
                    montagens_possiveis = quantidade_disponivel // quantidade_por_placa
                    # Verifica se a quantidade disponível está abaixo do limite mínimo
                    if montagens_possiveis <= limite_minimo:
                        projetos_com_estoque_baixo.add(projeto_nome)
                        mensagem = f"AVISO: O estoque atual de {projeto_nome} é {quantidade_disponivel}, que está igual ou abaixo do limite mínimo ({limite_minimo})."

            # Se houver projetos com estoque baixo, exibe a mensagem
            if projetos_com_estoque_baixo:
                projetos = ', '.join(projetos_com_estoque_baixo)
                mensagem = f"AVISO: Limite mínimo atingido! {projetos}"

            # Se não houver componentes, mostra mensagem apropriada
            elif not componentes:
                mensagem = "Nenhum componente cadastrado."

            # Atualiza o label de status
            status_label.config(text=mensagem)

    # Chama a função novamente após 1000 ms
    root.after(1000, verificar_estoque_minimo)
    print(f"quantidade_por_placa atualizada para: {quantidade_por_placa}")
    print(f"limite_minimo atualizada para: {limite_minimo}")



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

if os.environ.get("ENVIRONMENT") == "production":
    print("Modo Produção Ativado")
else:
    print("Modo Desenvolvimento Ativado")

# Criação da janela principal
root = tk.Tk()
root.title("Controle de Estoque")
root.geometry("800x450")
centralizar_janela(root, 800, 450)

# Adicionando logo
try:
    logo_path = os.path.join(basedir, "logo.png")
    logo = PhotoImage(file=logo_path)
    logo = logo.subsample(3, 3)
    tk.Label(root, image=logo).grid(row=0, column=0, columnspan=2, pady=10)
    root.logo = logo
except tk.TclError:
    print("Erro ao carregar a imagem do logotipo para a página principal.")

# Adicionando texto abaixo do logotipo
texto = "ESTOQUE DE HARDWARE P&D"
tk.Label(root, text=texto, font=("Arial", 18)).grid(row=1, column=0, columnspan=2, pady=10)

# Adicionando botões à janela principal
button_cadastrar_projeto = tk.Button(root, text="Gerenciar Projetos", width=20, command=abrir_cadastro_projeto)
button_cadastrar_projeto.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

button_cadastrar_componente = tk.Button(root, text="Cadastrar Componentes", width=20, command=abrir_cadastro_componente)
button_cadastrar_componente.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

button_adicionar_estoque = tk.Button(root, text="Adicionar Estoque", width=20, command=abrir_adicionar_estoque)
button_adicionar_estoque.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

button_listar_componentes = tk.Button(root, text="Listar Componentes", width=20, command=abrir_listar_componentes)
button_listar_componentes.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

button_deletar_componente = tk.Button(root, text="Deletar Componentes", width=20, command=abrir_deletar_componente)
button_deletar_componente.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

button_debitar_componentes = tk.Button(root, text="Debitar Componentes", width=20, command=abrir_debitar_componentes)
button_debitar_componentes.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

# Adicionando um label para mostrar o status de estoque
status_label = tk.Label(root, text="Verificando estoque...", font=("Arial", 12), fg="red")
status_label.grid(row=5, column=0, columnspan=2, pady=10)

# Chama a função para verificar o estoque mínimo inicialmente
verificar_estoque_minimo()

# Rodapé
rodape_texto = "Developed by: Icaro Quimaia Rodrigues"
rodape_label = tk.Label(root, text=rodape_texto, font=("Arial", 8), anchor='e')
rodape_label.grid(row=6, column=1, padx=10, pady=0, sticky="se")

# Ajustes de layout
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)

# Inicia a interface principal
root.mainloop()
