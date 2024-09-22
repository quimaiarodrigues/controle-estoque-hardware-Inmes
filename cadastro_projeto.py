import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Import para Treeview
import sqlite3

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
                                nome TEXT NOT NULL UNIQUE,
                                limite_minimo INTEGER DEFAULT 0)''')

def abrir_janela_cadastro_projeto():
    def salvar_projeto():
        nome_projeto = nome_entry.get().strip()
        limite_minimo = int(limite_minimo_entry.get().strip())
        if nome_projeto and limite_minimo >= 0:
            try:
                conn = conectar_banco()
                if conn:
                    with conn:
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO Projetos (nome, limite_minimo) VALUES (?, ?)", (nome_projeto, limite_minimo))
                        conn.commit()
                        atualizar_lista_projetos()
                        nome_entry.delete(0, tk.END)
                        limite_minimo_entry.delete(0, tk.END)
            except sqlite3.IntegrityError:
                messagebox.showwarning("Aviso", "O nome do projeto já existe.")
        else:
            messagebox.showwarning("Aviso", "O nome do projeto e o limite mínimo devem ser preenchidos corretamente.")

    def atualizar_lista_projetos():
        for item in tree.get_children():
            tree.delete(item)  # Limpa a Treeview antes de adicionar os novos itens
        conn = conectar_banco()
        if conn:
            with conn:
                cursor = conn.cursor()
                cursor.execute("SELECT nome, limite_minimo FROM Projetos ORDER BY nome")
                projetos = cursor.fetchall()
                for projeto in projetos:
                    limite_minimo_formatado = f"{projeto[1]:^10}"  # Centraliza o limite mínimo
                    tree.insert('', tk.END, values=(projeto[0], limite_minimo_formatado))  # Adiciona o nome e o limite mínimo

    def obter_id_projeto(nome_projeto):
        conn = conectar_banco()
        if conn:
            with conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM Projetos WHERE nome = ?", (nome_projeto,))
                resultado = cursor.fetchone()
                if resultado:
                    return resultado[0]
        return None

    def editar_projeto():
        projeto_selecionado = tree.selection()
        if projeto_selecionado:
            valores_projeto = tree.item(projeto_selecionado, 'values')
            nome_atual, limite_atual = valores_projeto[0], valores_projeto[1].strip()  # Remove espaços
            projeto_id = obter_id_projeto(nome_atual)

            editar_janela = tk.Toplevel()
            editar_janela.title("Editar Projeto")
            editar_janela.geometry("400x250")

            tk.Label(editar_janela, text="Nome do Projeto:").pack(anchor="w", padx=10, pady=5)
            nome_entry = tk.Entry(editar_janela)
            nome_entry.pack(fill="x", padx=10, pady=5)
            nome_entry.insert(0, nome_atual)

            tk.Label(editar_janela, text="Limite Mínimo:").pack(anchor="w", padx=10, pady=5)
            limite_entry = tk.Entry(editar_janela)
            limite_entry.pack(fill="x", padx=10, pady=5)
            limite_entry.insert(0, str(limite_atual))

            def salvar_edicao():
                novo_nome = nome_entry.get().strip()
                try:
                    novo_limite = int(limite_entry.get().strip())
                except ValueError:
                    messagebox.showwarning("Aviso", "O limite mínimo deve ser um número inteiro.")
                    return

                if novo_nome and novo_limite >= 0:
                    try:
                        conn = conectar_banco()
                        if conn:
                            with conn:
                                cursor = conn.cursor()
                                cursor.execute("UPDATE Projetos SET nome = ?, limite_minimo = ? WHERE id = ?", (novo_nome, novo_limite, projeto_id))
                                conn.commit()
                                atualizar_lista_projetos()
                                editar_janela.destroy()
                    except sqlite3.IntegrityError:
                        messagebox.showwarning("Aviso", "Já existe um projeto com esse nome.")
                else:
                    messagebox.showwarning("Aviso", "Preencha todos os campos corretamente.")

            frame_botoes_edicao = tk.Frame(editar_janela)
            frame_botoes_edicao.pack(pady=10, fill="x")
            tk.Button(frame_botoes_edicao, text="Salvar", command=salvar_edicao).pack(side="left", padx=10)
            tk.Button(frame_botoes_edicao, text="Cancelar", command=editar_janela.destroy).pack(side="left", padx=10)

    def excluir_projeto():
        projeto_selecionado = tree.selection()
        if projeto_selecionado:
         valores_projeto = tree.item(projeto_selecionado, 'values')
        nome_projeto = valores_projeto[0]

        if messagebox.askyesno("Confirmar Exclusão", f"Você realmente deseja excluir o projeto '{nome_projeto}'?"):
            conn = conectar_banco()
            if conn:
                with conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM Projetos WHERE nome = ?", (nome_projeto,))
                    conn.commit()
                    atualizar_lista_projetos()
                    janela_projeto.focus_force()  # Manter a janela de cadastro em primeiro plano


    janela_projeto = tk.Toplevel()
    janela_projeto.title("Cadastrar Projeto")
    janela_projeto.geometry("800x600")

    # Adicionando logo
    try:
        logo_path = os.path.join(basedir, "logo.png")
        logo = tk.PhotoImage(file=logo_path)
        logo = logo.subsample(3, 3)
        logo_label = tk.Label(janela_projeto, image=logo)
        logo_label.grid(row=0, column=0, columnspan=2, pady=10)
        janela_projeto.logo = logo
    except tk.TclError:
        print("Erro ao carregar a imagem do logotipo.")

    # Adicionando texto abaixo do logotipo
    tk.Label(janela_projeto, text="Cadastro de Projetos", font=("Arial", 18)).grid(row=1, column=0, columnspan=2, pady=10)

    tk.Label(janela_projeto, text="Nome do Projeto:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    nome_entry = tk.Entry(janela_projeto)
    nome_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    tk.Label(janela_projeto, text="Limite Mínimo:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    limite_minimo_entry = tk.Entry(janela_projeto)
    limite_minimo_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    frame_botoes = tk.Frame(janela_projeto)
    frame_botoes.grid(row=4, column=0, columnspan=2, pady=10)

    tk.Button(frame_botoes, text="Salvar", command=salvar_projeto).pack(side="left", padx=10)
    tk.Button(frame_botoes, text="Editar Projeto", command=editar_projeto).pack(side="left", padx=10)
    tk.Button(frame_botoes, text="Excluir Projeto", command=excluir_projeto).pack(side="left", padx=10)  # Botão para excluir
    tk.Button(frame_botoes, text="Cancelar", command=janela_projeto.destroy).pack(side="left", padx=10)

    tk.Label(janela_projeto, text="Projetos Cadastrados:").grid(row=5, column=0, padx=10, pady=5, sticky="w")

    # Criando a Treeview com duas colunas
    tree = ttk.Treeview(janela_projeto, columns=("nome", "limite_minimo"), show='headings', height=8)
    tree.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
    tree.heading("nome", text="Nome do Projeto")
    tree.heading("limite_minimo", text="Limite Mínimo")

    # Centraliza o texto na coluna "Limite Mínimo"
    tree.column("limite_minimo", anchor="center")  # Define o alinhamento da coluna

    atualizar_lista_projetos()

    janela_projeto.grid_rowconfigure(6, weight=1)
    janela_projeto.grid_columnconfigure(1, weight=1)

if __name__ == "__main__":
    criar_tabela_projetos()
    root = tk.Tk()
    root.title("Controle de Estoque de Componentes")
    root.geometry("300x200")

    tk.Button(root, text="Cadastrar Projeto", command=abrir_janela_cadastro_projeto).pack(pady=20)
    root.mainloop()
