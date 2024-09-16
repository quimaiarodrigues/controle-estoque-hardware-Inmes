import tkinter as tk
from tkinter import messagebox

def abrir_janela_editar_projeto(projeto_list, componente_dict):
    def salvar_edicao():
        projeto_selecionado = lista_projetos.get(tk.ACTIVE)
        novo_nome = novo_nome_entry.get().strip()
        if novo_nome and novo_nome not in projeto_list and projeto_selecionado:
            projeto_list.remove(projeto_selecionado)
            projeto_list.append(novo_nome)
            projeto_list.sort()
            componente_dict[novo_nome] = componente_dict.pop(projeto_selecionado, [])
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
    
    tk.Label(editar_janela, text="Selecione o Projeto para Editar:").pack(anchor="w", padx=10, pady=5)
    lista_projetos = tk.Listbox(editar_janela)
    lista_projetos.pack(fill="both", expand=True, padx=10, pady=5)
    atualizar_lista_projetos()
    
    tk.Label(editar_janela, text="Novo Nome do Projeto:").pack(anchor="w", padx=10, pady=5)
    novo_nome_entry = tk.Entry(editar_janela)
    novo_nome_entry.pack(fill="x", padx=10, pady=5)
    
    tk.Button(editar_janela, text="Salvar", command=salvar_edicao).pack(pady=10)
    tk.Button(editar_janela, text="Cancelar", command=editar_janela.destroy).pack(pady=10)
