import os
import tkinter as tk
from tkinter import messagebox
import sqlite3
import sys

# Obtenha o caminho absoluto do diretório atual
basedir = os.path.dirname(os.path.abspath(__file__))

def conectar_banco():
    try:
        # Use o caminho absoluto para garantir que o executável encontre o banco de dados
        conn = sqlite3.connect(os.path.join(basedir, 'estoque.db'))
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

def criar_tabela_projetos():
    conn = conectar_banco()
    if conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Projetos (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome TEXT NOT NULL UNIQUE)''')

def abrir_janela_cadastro_projeto():
    def salvar_projeto():
        nome_projeto = nome_entry.get().strip()
        if nome_projeto:
            try:
                conn = conectar_banco()
                if conn:
                    with conn:
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO Projetos (nome) VALUES (?)", (nome_projeto,))
                        conn.commit()  # Commit após inserção
                        atualizar_lista_projetos()
                        nome_entry.delete(0, tk.END)
            except sqlite3.IntegrityError:
                messagebox.showwarning("Aviso", "O nome do projeto já existe.")
        else:
            messagebox.showwarning("Aviso", "O nome do projeto não pode estar vazio.")

    def atualizar_lista_projetos():
        lista_projetos.delete(0, tk.END)
        conn = conectar_banco()
        if conn:
            with conn:
                cursor = conn.cursor()
                cursor.execute("SELECT nome FROM Projetos ORDER BY nome")
                projetos = cursor.fetchall()
                for projeto in projetos:
                    lista_projetos.insert(tk.END, projeto[0])

    def editar_projeto():
        projeto_selecionado = lista_projetos.get(tk.ACTIVE)
        if projeto_selecionado:
            editar_janela = tk.Toplevel()
            editar_janela.title("Editar Nome do Projeto")
            editar_janela.geometry("400x200")

            tk.Label(editar_janela, text="Novo Nome do Projeto:").pack(anchor="w", padx=10, pady=5)
            novo_nome_entry = tk.Entry(editar_janela)
            novo_nome_entry.pack(fill="x", padx=10, pady=5)
            novo_nome_entry.insert(0, projeto_selecionado)

            def salvar_edicao():
                novo_nome = novo_nome_entry.get().strip()
                if novo_nome and projeto_selecionado:
                    try:
                        conn = conectar_banco()
                        if conn:
                            with conn:
                                cursor = conn.cursor()
                                cursor.execute("UPDATE Projetos SET nome = ? WHERE nome = ?", (novo_nome, projeto_selecionado))
                                conn.commit()  # Commit após atualização
                                atualizar_lista_projetos()
                                editar_janela.destroy()
                    except sqlite3.IntegrityError:
                        messagebox.showwarning("Aviso", "Já existe um projeto com esse nome.")

            frame_botoes_edicao = tk.Frame(editar_janela)
            frame_botoes_edicao.pack(pady=10, fill="x")
            tk.Button(frame_botoes_edicao, text="Salvar", command=salvar_edicao).pack(side="left", padx=10)
            tk.Button(frame_botoes_edicao, text="Cancelar", command=editar_janela.destroy).pack(side="left", padx=10)

    def deletar_projeto():
        projeto_selecionado = lista_projetos.get(tk.ACTIVE)
        if projeto_selecionado:
            confirmar = messagebox.askyesno("Confirmar Exclusão", f"Você tem certeza que deseja excluir o projeto '{projeto_selecionado}'?")
            if confirmar:
                conn = conectar_banco()
                if conn:
                    with conn:
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM Projetos WHERE nome = ?", (projeto_selecionado,))
                        conn.commit()  # Commit após exclusão
                        atualizar_lista_projetos()

    janela_projeto = tk.Toplevel()
    janela_projeto.title("Cadastrar Projeto")
    janela_projeto.geometry("800x400")

    # Adicionando logo
    try:
        logo_path = os.path.join(basedir, "logo.png")
        logo = tk.PhotoImage(file=logo_path)
        logo = logo.subsample(3, 3)  # Reduz a imagem para se ajustar ao tamanho da tela
        logo_label = tk.Label(janela_projeto, image=logo)
        logo_label.grid(row=0, column=0, columnspan=2, pady=10)
        janela_projeto.logo = logo  # Mantém uma referência ao logo para evitar que o Python o descarte
    except tk.TclError:
        print("Erro ao carregar a imagem do logotipo para a janela de cadastro de projeto.")

    # Adicionando texto abaixo do logotipo
    texto = "Cadastro de Projetos"
    tk.Label(janela_projeto, text=texto, font=("Arial", 18)).grid(row=1, column=0, columnspan=2, pady=10)

    tk.Label(janela_projeto, text="Nome do Projeto:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    nome_entry = tk.Entry(janela_projeto)
    nome_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    frame_botoes = tk.Frame(janela_projeto)
    frame_botoes.grid(row=3, column=0, columnspan=2, pady=10)

    tk.Button(frame_botoes, text="Salvar", command=salvar_projeto).pack(side="left", padx=10)
    tk.Button(frame_botoes, text="Editar Projeto", command=editar_projeto).pack(side="left", padx=10)
    tk.Button(frame_botoes, text="Deletar Projeto", command=deletar_projeto).pack(side="left", padx=10)
    tk.Button(frame_botoes, text="Cancelar", command=janela_projeto.destroy).pack(side="left", padx=10)

    tk.Label(janela_projeto, text="Projetos Cadastrados:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    lista_projetos = tk.Listbox(janela_projeto)
    lista_projetos.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
    atualizar_lista_projetos()

    janela_projeto.grid_rowconfigure(5, weight=1)
    janela_projeto.grid_columnconfigure(1, weight=1)

if __name__ == "__main__":
    criar_tabela_projetos()
    # Não abra a janela principal aqui. A janela principal deve ser aberta a partir do main_app.py
