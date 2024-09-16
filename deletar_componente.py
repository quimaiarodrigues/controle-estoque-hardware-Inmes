import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def abrir_janela():
    def obter_projetos():
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM projetos")
        projetos = [row[0] for row in cursor.fetchall()]
        conn.close()
        return projetos

    def obter_componentes(projeto):
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        
        # Obter o id do projeto
        cursor.execute("SELECT id FROM projetos WHERE nome = ?", (projeto,))
        projeto_id = cursor.fetchone()
        
        if projeto_id is None:
            conn.close()
            return []  # Nenhum projeto encontrado
        
        projeto_id = projeto_id[0]
        
        # Obter componentes associados ao projeto
        cursor.execute("""
            SELECT c.codigo, c.nome, c.quantidade_por_placa, c.quantidade_disponivel
            FROM componentes c
            WHERE c.id_projeto = ?
        """, (projeto_id,))
        
        componentes = [
            {"codigo": row[0], "nome": row[1], "quantidade_por_placa": row[2], "quantidade_disponivel": row[3]}
            for row in cursor.fetchall()
        ]
        
        conn.close()
        return componentes

    def atualizar_tabela():
        tabela.delete(*tabela.get_children())
        projeto = projeto_selecionado.get()
        if projeto:
            componentes = obter_componentes(projeto)
            if componentes:
                for componente in componentes:
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
            confirmar = messagebox.askyesno("Confirmar Exclusão", f"Você tem certeza que deseja deletar o componente '{codigo}'?")
            if confirmar:
                conn = sqlite3.connect('estoque.db')
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM componentes
                    WHERE codigo = ?
                """, (codigo,))
                conn.commit()
                conn.close()
                tabela.delete(selecionado[0])
                messagebox.showinfo("Info", "Componente deletado com sucesso!")
        else:
            messagebox.showwarning("Seleção inválida", "Selecione um componente para deletar.")

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
    projetos = obter_projetos()
    projeto_selecionado.set(projetos[0] if projetos else "Nenhum Projeto")

    menu_projeto = tk.OptionMenu(janela_deletar, projeto_selecionado, *projetos, command=lambda _: atualizar_tabela())
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

    # Botões para atualizar, deletar e cancelar
    frame_botoes = tk.Frame(janela_deletar)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Atualizar", command=atualizar_tabela).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Deletar Componente", command=deletar_componente).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Cancelar", command=janela_deletar.destroy).pack(side=tk.LEFT, padx=5)

    janela_deletar.mainloop()
