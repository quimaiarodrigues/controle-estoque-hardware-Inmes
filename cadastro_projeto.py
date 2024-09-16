import tkinter as tk

def salvar_projeto(nome_projeto, projeto_list, componente_dict):
    if nome_projeto:
        projeto_list.append(nome_projeto)
        componente_dict[nome_projeto] = []  # Inicializa a lista de componentes para o novo projeto
        print(f"Projeto '{nome_projeto}' salvo.")
    else:
        print("Preencha o nome do projeto.")

def abrir_janela(projeto_list, componente_dict):
    janela = tk.Toplevel()
    janela.title("Cadastrar Projeto")
    janela.geometry("500x250")

    # Adicionando logo
    try:
        logo = tk.PhotoImage(file="logo.png")
        logo = logo.subsample(4, 4)
        tk.Label(janela, image=logo).pack(pady=10)
        janela.logo = logo
    except tk.TclError:
        print("Erro ao carregar a imagem do logotipo para o cadastro do projeto.")

    # Adicionando texto abaixo do logo
    texto = "Cadastro de Projeto"
    tk.Label(janela, text=texto, font=("Arial", 16)).pack(pady=10)

    tk.Label(janela, text="Nome do Projeto:").pack(anchor="w", padx=10, pady=5)
    entry_nome_projeto = tk.Entry(janela)
    entry_nome_projeto.pack(fill="x", padx=10, pady=5)

    # Frame para organizar os botões "Salvar" e "Cancelar"
    button_frame = tk.Frame(janela)
    button_frame.pack(pady=10)

    # Botão para salvar o projeto
    tk.Button(button_frame, text="Salvar", command=lambda: salvar_projeto(entry_nome_projeto.get(), projeto_list, componente_dict)).pack(side="left", padx=10)

    # Botão para cancelar (fechar a janela)
    tk.Button(button_frame, text="Cancelar", command=janela.destroy).pack(side="left", padx=10)

    janela.mainloop()
