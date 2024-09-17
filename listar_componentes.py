import tkinter as tk
from tkinter import ttk
import sqlite3
import os

def conectar_banco():
    """Conecta ao banco de dados SQLite e retorna a conexão."""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'estoque.db')
    return sqlite3.connect(db_path)

def obter_lista_projetos():
    """Obtém a lista de nomes de projetos do banco de dados."""
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM Projetos")
    projetos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return projetos

def obter_componentes_por_projeto(projeto):
    """Obtém a lista de componentes para um projeto específico."""
    conn = conectar_banco()
    cursor = conn.cursor()

    # Buscar o ID do projeto
    cursor.execute("SELECT id FROM Projetos WHERE nome = ?", (projeto,))
    projeto_id = cursor.fetchone()
    
    if not projeto_id:
        conn.close()
        return []

    projeto_id = projeto_id[0]
    
    # Buscar componentes para o projeto
    cursor.execute("""
        SELECT codigo, nome, quantidade_por_placa, quantidade_disponivel 
        FROM Componentes 
        WHERE id_projeto = ?
    """, (projeto_id,))
    
    componentes = cursor.fetchall()
    conn.close()
    
    # Formatar os resultados
    return [{"codigo": row[0], "nome": row[1], "quantidade_por_placa": row[2], "quantidade_disponivel": row[3]} for row in componentes]

def abrir_aba_listar_componentes(projeto_list):
    janela_listar = tk.Toplevel()
    janela_listar.title("Listar Componentes")
    janela_listar.geometry("800x550")

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
        if coluna in ("Código", "Quantidade por Placa", "Quantidade Disponível"):
            tabela.column(coluna, anchor="center")
        else:
            tabela.column(coluna, anchor="w")

    tabela.pack(fill="both", expand=True)

    # Populando a tabela
    def atualizar_tabela():
        tabela.delete(*tabela.get_children())
        projeto = projeto_selecionado.get()
        componentes = obter_componentes_por_projeto(projeto)
        
        if componentes:
            for componente in componentes:
                tabela.insert("", "end", values=(
                    componente["codigo"],
                    componente["nome"],
                    componente["quantidade_por_placa"],
                    componente["quantidade_disponivel"]
                ))
        else:
            tk.Label(janela_listar, text=f"Nenhum componente encontrado para o projeto '{projeto}'.").pack(pady=10)

    # Frame para botões "Atualizar" e "Cancelar"
    frame_botoes = tk.Frame(janela_listar)
    frame_botoes.pack(pady=10)

    # Botão para atualizar a tabela
    tk.Button(frame_botoes, text="Atualizar", command=atualizar_tabela).pack(side="left", padx=10)

    # Botão para cancelar e fechar a janela
    tk.Button(frame_botoes, text="Cancelar", command=janela_listar.destroy).pack(side="left", padx=10)

    janela_listar.mainloop()

def abrir_listar_componentes():
    projetos = obter_lista_projetos()  # Obtém a lista de projetos
    abrir_aba_listar_componentes(projetos)
