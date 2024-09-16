import tkinter as tk
from tkinter import messagebox

def abrir_janela_cadastro_projeto(projeto_list, componente_dict):
    def salvar_projeto():
        nome_projeto = nome_entry.get().strip()
        if nome_projeto and nome_projeto not in projeto_list:
            projeto_list.append(nome_projeto)
            projeto_list.sort()
            componente_dict[nome_projeto] = []
            atualizar_lista_projetos()
            nome_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "O nome do projeto já existe ou está vazio.")

    def atualizar_lista_projetos():
        lista_projetos.delete(0, tk.END)
        for projeto in projeto_list:
            lista_projetos.insert(tk.END, projeto)

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
                if novo_nome and novo_nome not in projeto_list and projeto_selecionado:
                    projeto_list.remove(projeto_selecionado)
                    projeto_list.append(novo_nome)
                    projeto_list.sort()
                    componente_dict[novo_nome] = componente_dict.pop(projeto_selecionado, [])
                    atualizar_lista_projetos()
                    editar_janela.destroy()
                elif novo_nome in projeto_list:
                    messagebox.showwarning("Aviso", "Já existe um projeto com esse nome.")

            tk.Button(editar_janela, text="Salvar", command=salvar_edicao).pack(side="left", padx=10, pady=10)
            tk.Button(editar_janela, text="Cancelar", command=editar_janela.destroy).pack(side="right", padx=10, pady=10)

    janela_projeto = tk.Toplevel()
    janela_projeto.title("Cadastrar Projeto")
    janela_projeto.geometry("400x300")

    tk.Label(janela_projeto, text="Nome do Projeto:").pack(anchor="w", padx=10, pady=5)
    nome_entry = tk.Entry(janela_projeto)
    nome_entry.pack(fill="x", padx=10, pady=5)

    # Frame para os botões "Salvar" e "Editar Projeto"
    frame_botoes = tk.Frame(janela_projeto)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Salvar", command=salvar_projeto).pack(side="left", padx=10)
    tk.Button(frame_botoes, text="Editar Projeto", command=editar_projeto).pack(side="left", padx=10)

    tk.Label(janela_projeto, text="Projetos Cadastrados:").pack(anchor="w", padx=10, pady=5)
    lista_projetos = tk.Listbox(janela_projeto)
    lista_projetos.pack(fill="both", expand=True, padx=10, pady=5)
    atualizar_lista_projetos()

    janela_projeto.mainloop()
