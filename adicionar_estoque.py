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
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados adicionar estoque: {e}")
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
    # Calcula a posição x e y para centralizar a janela
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def pesquisar_componente(codigo_componente, projeto, label_nome_componente, label_quantidade, label_quantidade_por_projeto):
    conn = conectar_banco()
    if conn is None:
        return
    cursor = conn.cursor()

    # Consultar o componente com base no código e no nome do projeto
    query = """
    SELECT c.nome, c.quantidade_disponivel, c.quantidade_por_placa 
    FROM Componentes c 
    JOIN Projetos p ON c.id_projeto = p.id 
    WHERE c.codigo = ? AND p.nome = ?
    """
    cursor.execute(query, (codigo_componente, projeto))
    componente = cursor.fetchone()

    if componente:
        label_nome_componente.config(text=f"Nome do Componente: {componente[0]}")
        label_quantidade.config(text=f"Quantidade em Estoque: {componente[1]}")
        label_quantidade_por_projeto.config(text=f"Quantidade por Projeto: {componente[2]}")
    else:
        label_nome_componente.config(text="Componente não encontrado.")
        label_quantidade.config(text="")
        label_quantidade_por_projeto.config(text="")

    conn.close()

def ocultar_status(label_status):
    label_status.config(text="")

def adicionar_estoque(projeto, codigo_componente, quantidade, label_status):
    if projeto and codigo_componente and quantidade:
        try:
            quantidade = int(quantidade)
        except ValueError:
            label_status.config(text="A quantidade deve ser um número inteiro.", fg="red")
            label_status.after(3000, lambda: ocultar_status(label_status))
            return

        conn = conectar_banco()
        if conn is None:
            return
        cursor = conn.cursor()

        # Atualizar a quantidade disponível do componente
        query = """
        UPDATE Componentes 
        SET quantidade_disponivel = quantidade_disponivel + ? 
        WHERE codigo = ? AND id_projeto = (SELECT id FROM Projetos WHERE nome = ?)
        """
        cursor.execute(query, (quantidade, codigo_componente, projeto))
        if cursor.rowcount > 0:
            label_status.config(text="Componente Adicionado", fg="green")
        else:
            label_status.config(text="Componente não encontrado no projeto.", fg="red")

        conn.commit()
        conn.close()
    else:
        label_status.config(text="Preencha todos os campos.", fg="red")

    label_status.after(3000, lambda: ocultar_status(label_status))

# Função para abrir a janela de adicionar estoque
def abrir_janela():
    conn = conectar_banco()
    if conn is None:
        return
    cursor = conn.cursor()

    # Obter a lista de projetos do banco de dados
    cursor.execute("SELECT nome FROM Projetos")
    projeto_list = [row[0] for row in cursor.fetchall()]

    conn.close()

    janela = tk.Toplevel()
    janela.title("Adicionar Estoque")
    janela.geometry("800x500")
    centralizar_janela(janela, 800, 500)

    # Adicionando logo
    try:
        logo_path = os.path.join(basedir, 'logo.png')  # Use o caminho absoluto para a logo
        logo = tk.PhotoImage(file=logo_path)
        logo = logo.subsample(4, 4)
        tk.Label(janela, image=logo).pack(pady=10)
        janela.logo = logo
    except tk.TclError:
        print("Erro ao carregar a imagem da logo para adicionar estoque.")

    # Adicionando texto abaixo da logo
    texto = "ADICIONAR ESTOQUE"
    tk.Label(janela, text=texto, font=("Arial", 16)).pack(pady=10)

    tk.Label(janela, text="Selecione o Projeto:").pack(anchor="w", padx=10, pady=5)
    projeto_selecionado = tk.StringVar()
    projeto_selecionado.set(projeto_list[0] if projeto_list else "Nenhum Projeto")

    menu_projeto = tk.OptionMenu(janela, projeto_selecionado, *projeto_list)
    menu_projeto.pack(fill="x", padx=10, pady=5)

    tk.Label(janela, text="Código do Componente:").pack(anchor="w", padx=10, pady=5)
    entry_codigo_componente = tk.Entry(janela)
    entry_codigo_componente.pack(fill="x", padx=10, pady=5)

    # Labels para mostrar informações do componente
    label_nome_componente = tk.Label(janela, text="Nome do Componente:")
    label_nome_componente.pack(anchor="w", padx=10, pady=5)

    label_quantidade = tk.Label(janela, text="Quantidade em Estoque:")
    label_quantidade.pack(anchor="w", padx=10, pady=5)

    label_quantidade_por_projeto = tk.Label(janela, text="Quantidade por Projeto:")
    label_quantidade_por_projeto.pack(anchor="w", padx=10, pady=5)

    tk.Label(janela, text="Quantidade a Adicionar:").pack(anchor="w", padx=10, pady=5)
    entry_quantidade = tk.Entry(janela)
    entry_quantidade.pack(fill="x", padx=10, pady=5)

    # Frame dos botões
    button_frame = tk.Frame(janela)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Pesquisar", command=lambda: pesquisar_componente(
        entry_codigo_componente.get(),
        projeto_selecionado.get(),
        label_nome_componente,
        label_quantidade,
        label_quantidade_por_projeto)).grid(row=0, column=0, padx=5)

    tk.Button(button_frame, text="Adicionar", command=lambda: adicionar_estoque(
        projeto_selecionado.get(),
        entry_codigo_componente.get(),
        entry_quantidade.get(),
        label_status)).grid(row=0, column=1, padx=5)

    tk.Button(button_frame, text="Cancelar", command=janela.destroy).grid(row=0, column=2, padx=5)

    # Label de status
    label_status = tk.Label(janela, text="", fg="green")
    label_status.pack(pady=10)

    janela.mainloop()
