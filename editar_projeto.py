import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

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

def abrir_janela_editar_projeto(projeto_list, componente_dict):
    def salvar_edicao():
        projeto_selecionado = lista_projetos.get(tk.ACTIVE)
        novo_nome = novo_nome_entry.get().strip()
        if novo_nome and novo_nome not in projeto_list and projeto_selecionado:
            projeto_list.remove(projeto_selecionado)
            projeto_list.append(novo_nome)
            projeto_list.sort()
            componente_dict[novo_nome] = componente_dict.pop(projeto_selecionado, [])

            # Atualizar o banco de dados
            conn = conectar_banco()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE Projetos SET nome = ? WHERE nome = ?", (novo_nome, projeto_selecionado))
                    conn.commit()
                except sqlite3.Error as e:
                    messagebox.showerror("Erro", f"Erro ao atualizar o banco de dados: {e}")
                finally:
                    conn.close()

            atualizar_lista_projetos()
            editar_janela.destroy()
        elif novo_nome in projeto_list:
            messagebox.showwarning("Aviso", "Já existe um projeto com esse nome.")

    def atualizar_lista_projetos():
        lista_projetos.delete(0, tk.END)
        for projeto in projeto_list:
            lista_projetos.insert(tk.END, projeto)

    editar_janela = tk.Toplevel()
    editar_janela.title("Editar Nome do Projeto")
    editar_janela.geometry("400x300")

    tk.Label(editar_janela, text="Selecione o Projeto para Editar:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    lista_projetos = tk.Listbox(editar_janela)
    lista_projetos.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
    atualizar_lista_projetos()

    tk.Label(editar_janela, text="Novo Nome do Projeto:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    novo_nome_entry = tk.Entry(editar_janela)
    novo_nome_entry.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

    # Criar um Frame para os botões
    button_frame = tk.Frame(editar_janela)
    button_frame.grid(row=4, column=0, pady=10, padx=10, sticky="nsew")

    # Adicionar botões ao Frame
    salvar_button = tk.Button(button_frame, text="Salvar", command=salvar_edicao)
    cancelar_button = tk.Button(button_frame, text="Cancelar", command=editar_janela.destroy)

    salvar_button.grid(row=0, column=0, padx=10, pady=10)
    cancelar_button.grid(row=0, column=1, padx=10, pady=10)

    # Configurar o Frame para expansão
    button_frame.grid_rowconfigure(0, weight=1)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)

    # Configurar a janela para expansão
    editar_janela.grid_rowconfigure(1, weight=1)
    editar_janela.grid_columnconfigure(0, weight=1)

    editar_janela.mainloop()

# Exemplo de uso (simulação)
#projeto_list = ["Projeto 1", "Projeto 2", "Projeto 3"]
#componente_dict = {
 #   "Projeto 1": [],
  #  "Projeto 2": [],
   # "Projeto 3": []
#}

root = tk.Tk()
root.withdraw()  # Esconde a janela principal
#abrir_janela_editar_projeto(projeto_list, componente_dict)
