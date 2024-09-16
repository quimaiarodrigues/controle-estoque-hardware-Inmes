import tkinter as tk
from tkinter import PhotoImage
import sqlite3

# Função para conectar ao banco de dados
def conectar_banco():
    conn = sqlite3.connect('estoque.db')
    return conn

def pesquisar_componente(codigo_componente, projeto, label_nome_componente, label_quantidade, label_quantidade_por_projeto):
    conn = conectar_banco()
    cursor = conn.cursor()

    # Consultar o componente com base no código e no nome do projeto
    query = """
    SELECT c.nome, c.quantidade_disponivel, c.quantidade_por_placa 
    FROM Componentes c 
    JOIN Projetos p ON c.id_projeto = p.id 
    WHERE c.codigo = ? AND p.nome = ?
    """
    cursor.execute(query, (codigo_componente, projeto))
    componente = cursor.fetchone()

    if componente:
        label_nome_componente.config(text=f"Nome do Componente: {componente[0]}")
        label_quantidade.config(text=f"Quantidade em Estoque: {componente[1]}")
        label_quantidade_por_projeto.config(text=f"Quantidade por Projeto: {componente[2]}")
    else:
        label_nome_componente.config(text="Componente não encontrado.")
        label_quantidade.config(text="")
        label_quantidade_por_projeto.config(text="")

    conn.close()


def adicionar_estoque(projeto, codigo_componente, quantidade):
    if projeto and codigo_componente and quantidade:
        try:
            quantidade = int(quantidade)
        except ValueError:
            print("A quantidade deve ser um número inteiro.")
            return

        conn = conectar_banco()
        cursor = conn.cursor()

        # Atualizar a quantidade disponível do componente
        query = """
        UPDATE Componentes 
        SET quantidade_disponivel = quantidade_disponivel + ?
        WHERE codigo = ? AND id_projeto = (SELECT id FROM Projetos WHERE nome = ?)
        """
        cursor.execute(query, (quantidade, codigo_componente, projeto))
        if cursor.rowcount > 0:
            print(f"Adicionado {quantidade} unidades de {codigo_componente} ao projeto '{projeto}'.")
        else:
            print("Componente não encontrado no projeto.")

        conn.commit()
        conn.close()
    else:
        print("Preencha todos os campos.")


# Função para abrir a janela de adicionar estoque
def abrir_janela():
    conn = conectar_banco()
    cursor = conn.cursor()

    # Obter a lista de projetos do banco de dados
    cursor.execute("SELECT nome FROM Projetos")
    projeto_list = [row[0] for row in cursor.fetchall()]

    conn.close()

    janela = tk.Toplevel()
    janela.title("Adicionar Estoque")
    janela.geometry("600x460")

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
        label_nome_componente,
        label_quantidade,
        label_quantidade_por_projeto)).grid(row=0, column=0, padx=5)

    tk.Button(button_frame, text="Adicionar", command=lambda: adicionar_estoque(
        projeto_selecionado.get(),
        entry_codigo_componente.get(),
        entry_quantidade.get())).grid(row=0, column=1, padx=5)

    tk.Button(button_frame, text="Cancelar", command=janela.destroy).grid(row=0, column=2, padx=5)

    janela.mainloop()
