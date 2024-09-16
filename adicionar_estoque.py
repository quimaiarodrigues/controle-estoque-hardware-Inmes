import tkinter as tk
from tkinter import PhotoImage

def pesquisar_componente(codigo_componente, projeto, componentes_dict, label_nome_componente, label_quantidade, label_quantidade_por_projeto):
    componentes = componentes_dict.get(projeto, [])
    for comp in componentes:
        if comp["codigo"] == codigo_componente:
            label_nome_componente.config(text=f"Nome do Componente: {comp['nome']}")
            label_quantidade.config(text=f"Quantidade em Estoque: {comp['quantidade_disponivel']}")
            label_quantidade_por_projeto.config(text=f"Quantidade por Projeto: {comp['quantidade_por_placa']}")
            return
    label_nome_componente.config(text="Componente não encontrado.")
    label_quantidade.config(text="")
    label_quantidade_por_projeto.config(text="")

def adicionar_estoque(projeto, codigo_componente, quantidade, componentes_dict):
    if projeto and codigo_componente and quantidade:
        try:
            quantidade = int(quantidade)
        except ValueError:
            print("A quantidade deve ser um número inteiro.")
            return

        for comp in componentes_dict.get(projeto, []):
            if comp["codigo"] == codigo_componente:
                comp["quantidade_disponivel"] += quantidade
                print(f"Adicionado {quantidade} unidades de {codigo_componente} ao projeto '{projeto}'.")
                return
        print("Componente não encontrado no projeto.")
    else:
        print("Preencha todos os campos.")

def abrir_janela(projeto_list, componentes_dict):
    janela = tk.Toplevel()
    janela.title("Adicionar Estoque")
    janela.geometry("500x480")

    # Adicionando logo
    try:
        logo = tk.PhotoImage(file="logo.png")
        logo = logo.subsample(4, 4)
        tk.Label(janela, image=logo).pack(pady=10)
        janela.logo = logo
    except tk.TclError:
        print("Erro ao carregar a imagem da logo para adicionar estoque.")

    # Adicionando texto abaixo da logo
    texto = "Adicionar Estoque"
    tk.Label(janela, text=texto, font=("Arial", 16)).pack(pady=10)

    tk.Label(janela, text="Selecione o Projeto:").pack(anchor="w", padx=10, pady=5)
    projeto_selecionado = tk.StringVar()
    projeto_selecionado.set(projeto_list[0] if projeto_list else "Nenhum Projeto")

    menu_projeto = tk.OptionMenu(janela, projeto_selecionado, *projeto_list)
    menu_projeto.pack(fill="x", padx=10, pady=5)

    tk.Label(janela, text="Código do Componente:").pack(anchor="w", padx=10, pady=5)
    entry_codigo_componente = tk.Entry(janela)
    entry_codigo_componente.pack(fill="x", padx=10, pady=5)

    # Labels para mostrar informações do componente
    label_nome_componente = tk.Label(janela, text="Nome do Componente:")
    label_nome_componente.pack(anchor="w", padx=10, pady=5)

    label_quantidade = tk.Label(janela, text="Quantidade em Estoque:")
    label_quantidade.pack(anchor="w", padx=10, pady=5)

    # Novo campo: Quantidade por Projeto
    label_quantidade_por_projeto = tk.Label(janela, text="Quantidade por Projeto:")
    label_quantidade_por_projeto.pack(anchor="w", padx=10, pady=5)

    tk.Label(janela, text="Quantidade a Adicionar:").pack(anchor="w", padx=10, pady=5)
    entry_quantidade = tk.Entry(janela)
    entry_quantidade.pack(fill="x", padx=10, pady=5)

    # Botões para pesquisar, adicionar estoque e cancelar
    button_frame = tk.Frame(janela)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Pesquisar", command=lambda: pesquisar_componente(
        entry_codigo_componente.get(),
        projeto_selecionado.get(),
        componentes_dict,
        label_nome_componente,
        label_quantidade,
        label_quantidade_por_projeto)).grid(row=0, column=0, padx=5)

    tk.Button(button_frame, text="Adicionar", command=lambda: adicionar_estoque(
        projeto_selecionado.get(),
        entry_codigo_componente.get(),
        entry_quantidade.get(),
        componentes_dict)).grid(row=0, column=1, padx=5)

    tk.Button(button_frame, text="Cancelar", command=janela.destroy).grid(row=0, column=2, padx=5)

    janela.mainloop()
