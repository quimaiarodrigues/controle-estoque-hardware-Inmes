import tkinter as tk

def salvar_componente(projeto, nome_componente, codigo_componente, quantidade_por_placa, quantidade_disponivel, componente_dict):
    if projeto and nome_componente and codigo_componente and quantidade_por_placa and quantidade_disponivel:
        if projeto in componente_dict:
            componente_dict[projeto].append({
                "nome": nome_componente,
                "codigo": codigo_componente,
                "quantidade_por_placa": int(quantidade_por_placa),
                "quantidade_disponivel": int(quantidade_disponivel)
            })
            print(f"Componente '{nome_componente}' salvo para o projeto '{projeto}'.")
        else:
            print(f"Projeto '{projeto}' não encontrado.")
    else:
        print("Preencha todos os campos.")

def atualizar_projetos(projeto_list, menu_projeto, projeto_selecionado):
    menu_projeto["menu"].delete(0, "end")
    for projeto in projeto_list:
        menu_projeto["menu"].add_command(label=projeto, command=tk._setit(projeto_selecionado, projeto))

def abrir_janela(projeto_list, componente_dict):
    janela = tk.Toplevel()
    janela.title("Cadastrar Componente")
    janela.geometry("500x500")

    # Adicionando logo
    try:
        logo = tk.PhotoImage(file="logo.png")
        logo = logo.subsample(4, 4)
        tk.Label(janela, image=logo).pack(pady=10)
        janela.logo = logo
    except tk.TclError:
        print("Erro ao carregar a imagem do logotipo para o cadastro de componente.")

    # Adicionando texto abaixo do logo
    texto = "Cadastro de Componente"
    tk.Label(janela, text=texto, font=("Arial", 16)).pack(pady=10)

    # Adicionando seleção de projeto
    tk.Label(janela, text="Seleção do Projeto:").pack(anchor="w", padx=10, pady=5)
    projeto_selecionado = tk.StringVar()
    projeto_selecionado.set(projeto_list[0] if projeto_list else "Nenhum Projeto")
    menu_projeto = tk.OptionMenu(janela, projeto_selecionado, *projeto_list)
    menu_projeto.pack(fill="x", padx=10, pady=5)

    # Atualizar os projetos quando a lista mudar
    atualizar_projetos(projeto_list, menu_projeto, projeto_selecionado)

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

    # Botão Salvar
    tk.Button(frame_botoes, text="Salvar", command=lambda: salvar_componente(
        projeto_selecionado.get(),
        entry_nome_componente.get(),
        entry_codigo_componente.get(),
        entry_quantidade_por_placa.get(),
        entry_quantidade_disponivel.get(),
        componente_dict
    )).pack(side=tk.LEFT, padx=5)

    # Botão Cancelar
    tk.Button(frame_botoes, text="Cancelar", command=janela.destroy).pack(side=tk.LEFT, padx=5)

    janela.mainloop()
