import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
import sys

#finalizado

# Função para conectar ao banco de dados
def conectar_banco():
    try:
        # Use o caminho absoluto para garantir que o executável encontre o banco de dados
        conn = sqlite3.connect(caminho_banco)
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados cadastro componente: {e}")
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

# Função para centralizar a janela
def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

# Função para salvar o componente no banco de dados
def salvar_componente(projeto, nome_componente, codigo_componente, quantidade_por_placa, quantidade_disponivel, label_status):
    if projeto and nome_componente and codigo_componente and quantidade_por_placa and quantidade_disponivel:
        try:
            quantidade_por_placa = int(quantidade_por_placa)
            quantidade_disponivel = int(quantidade_disponivel)
        except ValueError:
            messagebox.showwarning("Aviso", "As quantidades devem ser números inteiros.")
            return

        conn = conectar_banco()
        if conn:
            cursor = conn.cursor()

            # Verificar se o código do componente já existe para o projeto
            cursor.execute(""" 
                SELECT c.codigo 
                FROM Componentes c 
                JOIN Projetos p ON c.id_projeto = p.id 
                WHERE c.codigo = ? AND p.nome = ?
            """, (codigo_componente, projeto))

            if cursor.fetchone():
                messagebox.showwarning("Aviso", "Código de componente já existente para este projeto.")
            else:
                # Inserir novo componente
                cursor.execute(""" 
                    INSERT INTO Componentes (nome, codigo, quantidade_por_placa, quantidade_disponivel, id_projeto) 
                    VALUES (?, ?, ?, ?, (SELECT id FROM Projetos WHERE nome = ?))
                """, (nome_componente, codigo_componente, quantidade_por_placa, quantidade_disponivel, projeto))
                conn.commit()

                label_status.config(text="Componente cadastrado com sucesso.", fg="green")
                label_status.after(3000, lambda: label_status.config(text=""))

            conn.close()
    else:
        label_status.config(text="Preencha todos os campos.", fg="red")
        label_status.after(3000, lambda: label_status.config(text=""))

# Função para atualizar a lista de projetos no menu de seleção
def atualizar_projetos(menu_projeto, projeto_selecionado):
    conn = conectar_banco()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM Projetos")
        projeto_list = [row[0] for row in cursor.fetchall()]
        conn.close()

        menu_projeto["menu"].delete(0, "end")
        for projeto in projeto_list:
            menu_projeto["menu"].add_command(label=projeto, command=tk._setit(projeto_selecionado, projeto))

# Função para abrir a janela de cadastro de componentes
def abrir_janela():
    janela = tk.Toplevel()
    janela.title("Cadastrar Componente")
    janela.geometry("800x525")

    # Centraliza a janela de edição
    centralizar_janela(janela, 800, 525)

    # Adicionando logo
    try:
        logo_path = os.path.join(basedir,'logo.png')
        logo = tk.PhotoImage(file=logo_path)
        logo = logo.subsample(4, 4)
        tk.Label(janela, image=logo).pack(pady=10)
        janela.logo = logo
    except tk.TclError:
        print("Erro ao carregar a imagem da logo.")

    # Adicionando texto abaixo do logo
    texto = "CADASTRO DE COMPONENTES"
    tk.Label(janela, text=texto, font=("Arial", 16)).pack(pady=10)

    # Adicionando seleção de projeto
    tk.Label(janela, text="Seleção do Projeto:").pack(anchor="w", padx=10, pady=5)
    projeto_selecionado = tk.StringVar()

    # Menu dropdown de projetos
    menu_projeto = tk.OptionMenu(janela, projeto_selecionado, "")
    menu_projeto.pack(fill="x", padx=10, pady=5)

    # Atualizar os projetos
    atualizar_projetos(menu_projeto, projeto_selecionado)

    # Campos de entrada de dados
    tk.Label(janela, text="Nome do Componente:").pack(anchor="w", padx=10, pady=5)
    entry_nome_componente = tk.Entry(janela)
    entry_nome_componente.pack(fill="x", padx=10, pady=5)

    tk.Label(janela, text="Código do Componente:").pack(anchor="w", padx=10, pady=5)
    entry_codigo_componente = tk.Entry(janela)
    entry_codigo_componente.pack(fill="x", padx=10, pady=5)

    tk.Label(janela, text="Quantidade por Placa:").pack(anchor="w", padx=10, pady=5)
    entry_quantidade_por_placa = tk.Entry(janela)
    entry_quantidade_por_placa.pack(fill="x", padx=10, pady=5)

    tk.Label(janela, text="Quantidade Disponível:").pack(anchor="w", padx=10, pady=5)
    entry_quantidade_disponivel = tk.Entry(janela)
    entry_quantidade_disponivel.pack(fill="x", padx=10, pady=5)

    # Frame para botões de Salvar e Cancelar
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    # Label para mostrar o status do cadastro
    label_status = tk.Label(janela, text="", font=("Arial", 10))
    label_status.pack(pady=5)

    # Botão Salvar
    tk.Button(frame_botoes, text="Salvar", command=lambda: salvar_componente(
        projeto_selecionado.get(),
        entry_nome_componente.get(),
        entry_codigo_componente.get(),
        entry_quantidade_por_placa.get(),
        entry_quantidade_disponivel.get(),
        label_status
    )).pack(side=tk.LEFT, padx=5)

    # Botão Cancelar
    tk.Button(frame_botoes, text="Cancelar", command=janela.destroy).pack(side=tk.LEFT, padx=5)

    janela.mainloop()
