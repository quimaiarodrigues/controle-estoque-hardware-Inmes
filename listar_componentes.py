import tkinter as tk
from tkinter import ttk

def abrir_aba_listar_componentes(projeto_list, componente_dict):
    janela_listar = tk.Toplevel()
    janela_listar.title("Listar Componentes")
    janela_listar.geometry("850x500")

    # Adicionando logo
    try:
        logo = tk.PhotoImage(file="logo.png")
        logo = logo.subsample(4, 4)
        tk.Label(janela_listar, image=logo).pack(pady=10)
        janela_listar.logo = logo
    except tk.TclError:
        print("Erro ao carregar a imagem da logo para listar componentes.")

    # Adicionando texto abaixo da logo
    texto = "Listar Componentes"
    tk.Label(janela_listar, text=texto, font=("Arial", 16)).pack(pady=10)

    # Adicionando seleção de projeto
    tk.Label(janela_listar, text="Selecione o Projeto:").pack(anchor="w", padx=10, pady=5)
    projeto_selecionado = tk.StringVar()
    projeto_selecionado.set(projeto_list[0] if projeto_list else "Nenhum Projeto")

    menu_projeto = tk.OptionMenu(janela_listar, projeto_selecionado, *projeto_list)
    menu_projeto.pack(fill="x", padx=10, pady=5)

    # Frame para tabela de componentes
    frame_tabela = tk.Frame(janela_listar)
    frame_tabela.pack(fill="both", expand=True, padx=10, pady=10)

    # Barra de rolagem
    scrollbar = tk.Scrollbar(frame_tabela)
    scrollbar.pack(side="right", fill="y")

    colunas = ("Código", "Nome", "Quantidade por Placa", "Quantidade Disponível")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", yscrollcommand=scrollbar.set)
    
    scrollbar.config(command=tabela.yview)

    # Definindo cabeçalhos da tabela
    for coluna in colunas:
        tabela.heading(coluna, text=coluna)

    tabela.pack(fill="both", expand=True)

    # Populando a tabela
    def atualizar_tabela():
        tabela.delete(*tabela.get_children())
        projeto = projeto_selecionado.get()
        if projeto in componente_dict:
            for componente in componente_dict[projeto]:
                tabela.insert("", "end", values=(
                    componente["codigo"],
                    componente["nome"],
                    componente["quantidade_por_placa"],
                    componente["quantidade_disponivel"]
                ))
        else:
            tk.Label(janela_listar, text=f"Nenhum componente encontrado para o projeto '{projeto}'.").pack(pady=10)

    # Botão para atualizar a tabela
    tk.Button(janela_listar, text="Atualizar", command=atualizar_tabela).pack(pady=10)

    janela_listar.mainloop()
