import tkinter as tk
from tkinter import ttk, messagebox

def abrir_janela(projeto_list, componente_dict):
    janela_deletar = tk.Toplevel()
    janela_deletar.title("Deletar Componente")
    janela_deletar.geometry("850x500")

    # Adicionando logo
    try:
        logo = tk.PhotoImage(file="logo.png")
        logo = logo.subsample(4, 4)
        tk.Label(janela_deletar, image=logo).pack(pady=10)
        janela_deletar.logo = logo
    except tk.TclError:
        print("Erro ao carregar a imagem da logo para deletar componentes.")

    # Adicionando texto abaixo da logo
    texto = "Deletar Componente"
    tk.Label(janela_deletar, text=texto, font=("Arial", 16)).pack(pady=10)

    # Adicionando seleção de projeto
    tk.Label(janela_deletar, text="Selecione o Projeto:").pack(anchor="w", padx=10, pady=5)
    projeto_selecionado = tk.StringVar()
    projeto_selecionado.set(projeto_list[0] if projeto_list else "Nenhum Projeto")

    menu_projeto = tk.OptionMenu(janela_deletar, projeto_selecionado, *projeto_list)
    menu_projeto.pack(fill="x", padx=10, pady=5)

    # Frame para tabela de componentes
    frame_tabela = tk.Frame(janela_deletar)
    frame_tabela.pack(fill="both", expand=True, padx=10, pady=10)

    # Barra de rolagem
    scrollbar = tk.Scrollbar(frame_tabela)
    scrollbar.pack(side="right", fill="y")

    colunas = ("Código", "Nome", "Quantidade por Placa", "Quantidade Disponível")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", yscrollcommand=scrollbar.set)
    
    scrollbar.config(command=tabela.yview)

    # Definindo cabeçalhos da tabela
    for coluna in colunas:
        tabela.heading(coluna, text=coluna, anchor=tk.CENTER)

    tabela.pack(fill="both", expand=True)

    # Populando a tabela
    def atualizar_tabela():
        tabela.delete(*tabela.get_children())
        projeto = projeto_selecionado.get()
        if projeto in componente_dict:
            for componente in componente_dict[projeto]:
                tabela.insert("", "end", iid=componente["codigo"], values=(
                    componente["codigo"],
                    componente["nome"],
                    componente["quantidade_por_placa"],
                    componente["quantidade_disponivel"]
                ))
        else:
            tk.Label(janela_deletar, text=f"Nenhum componente encontrado para o projeto '{projeto}'.").pack(pady=10)

    def deletar_componente():
        selecionado = tabela.selection()
        if selecionado:
            codigo = tabela.item(selecionado[0], 'values')[0]
            projeto = projeto_selecionado.get()
            if projeto in componente_dict:
                componentes = componente_dict[projeto]
                for comp in componentes:
                    if comp["codigo"] == codigo:
                        componentes.remove(comp)
                        tabela.delete(selecionado[0])
                        print(f"Componente '{codigo}' deletado do projeto '{projeto}'.")
                        break
        else:
            messagebox.showwarning("Seleção inválida", "Selecione um componente para deletar.")

    # Frame para os botões de atualizar, deletar e cancelar
    frame_botoes = tk.Frame(janela_deletar)
    frame_botoes.pack(pady=10)

    # Botão para atualizar a tabela
    tk.Button(frame_botoes, text="Atualizar", command=atualizar_tabela).pack(side=tk.LEFT, padx=5)

    # Botão para deletar o componente selecionado
    tk.Button(frame_botoes, text="Deletar Componente", command=deletar_componente).pack(side=tk.LEFT, padx=5)

    # Botão para cancelar e fechar a janela
    tk.Button(frame_botoes, text="Cancelar", command=janela_deletar.destroy).pack(side=tk.LEFT, padx=5)

    janela_deletar.mainloop()
