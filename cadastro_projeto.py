# arquivo: cadastro_projeto.py

import tkinter as tk
from tkinter import messagebox
import sqlite3

def conectar_banco():
    try:
        conn = sqlite3.connect('estoque.db')
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

def criar_tabela_projetos():
    conn = conectar_banco()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Projetos (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL UNIQUE)''')
        conn.commit()
        conn.close()

def abrir_janela_cadastro_projeto():
    def salvar_projeto():
        nome_projeto = nome_entry.get().strip()
        if nome_projeto:
            try:
                conn = conectar_banco()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO Projetos (nome) VALUES (?)", (nome_projeto,))
                    conn.commit()
                    conn.close()
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
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM Projetos ORDER BY nome")
            projetos = cursor.fetchall()
            conn.close()
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
                            cursor = conn.cursor()
                            cursor.execute("UPDATE Projetos SET nome = ? WHERE nome = ?", (novo_nome, projeto_selecionado))
                            conn.commit()
                            conn.close()
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
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM Projetos WHERE nome = ?", (projeto_selecionado,))
                    conn.commit()
                    conn.close()
                    atualizar_lista_projetos()

    janela_projeto = tk.Toplevel()
    janela_projeto.title("Cadastrar Projeto")
    janela_projeto.geometry("600x400")

    tk.Label(janela_projeto, text="Nome do Projeto:").pack(anchor="w", padx=10, pady=5)
    nome_entry = tk.Entry(janela_projeto)
    nome_entry.pack(fill="x", padx=10, pady=5)

    frame_botoes = tk.Frame(janela_projeto)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Salvar", command=salvar_projeto).pack(side="left", padx=10)
    tk.Button(frame_botoes, text="Editar Projeto", command=editar_projeto).pack(side="left", padx=10)
    tk.Button(frame_botoes, text="Deletar Projeto", command=deletar_projeto).pack(side="left", padx=10)
    tk.Button(frame_botoes, text="Cancelar", command=janela_projeto.destroy).pack(side="left", padx=10)

    tk.Label(janela_projeto, text="Projetos Cadastrados:").pack(anchor="w", padx=10, pady=5)
    lista_projetos = tk.Listbox(janela_projeto)
    lista_projetos.pack(fill="both", expand=True, padx=10, pady=5)
    atualizar_lista_projetos()

if __name__ == "__main__":
    criar_tabela_projetos()
    # Não abra a janela principal aqui. A janela principal deve ser aberta a partir do main_app.py
