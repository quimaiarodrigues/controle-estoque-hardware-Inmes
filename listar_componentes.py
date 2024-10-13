import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sys
from tkinter import messagebox
from tkinter import PhotoImage

# Função para conectar ao banco de dados
def conectar_banco():
    try:
        conn = sqlite3.connect(caminho_banco)
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados listar componentes: {e}")
        return None

# Detecta se está rodando como executável ou como script Python
if getattr(sys, 'frozen', False):
    os.environ["ENVIRONMENT"] = "production"
else:
    os.environ["ENVIRONMENT"] = "development"

# Obtenha o caminho absoluto do diretório atual
basedir = os.path.dirname(os.path.abspath(__file__))

# Definir o caminho do banco de dados com base no ambiente
if os.environ.get("ENVIRONMENT") == "production":
    caminho_banco = "C:/Users/ICARO/Desktop/db/estoque.db"
else:
    caminho_banco = os.path.join(basedir, 'estoque.db')

# Função para centralizar a janela
def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

# Função para obter a lista de projetos
def obter_lista_projetos():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM Projetos")
    projetos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return projetos

# Função para obter componentes de um projeto específico
def obter_componentes_por_projeto(projeto):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Projetos WHERE nome = ?", (projeto,))
    projeto_id = cursor.fetchone()
    
    if not projeto_id:
        conn.close()
        return []

    projeto_id = projeto_id[0]
    
    cursor.execute(""" 
        SELECT codigo, nome, quantidade_por_placa, quantidade_disponivel 
        FROM Componentes 
        WHERE id_projeto = ?
    """, (projeto_id,))
    
    componentes = cursor.fetchall()
    conn.close()
    
    return [{"codigo": row[0], "nome": row[1], "quantidade_por_placa": row[2], "quantidade_disponivel": row[3]} for row in componentes]

# Função para editar a quantidade de um componente
def editar_quantidade(componente, tabela, projeto_selecionado, janela_listar):
    """Abre uma janela para editar a quantidade por placa do componente selecionado."""
    
    def salvar_edicao():
        nova_quantidade = entry_quantidade.get()
        try:
            nova_quantidade = int(nova_quantidade)
            if nova_quantidade < 0:
                raise ValueError("A quantidade não pode ser negativa.")
            
            # Conectar ao banco de dados e atualizar a quantidade
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute(""" 
                UPDATE Componentes
                SET quantidade_por_placa = ?
                WHERE codigo = ?
            """, (nova_quantidade, componente["codigo"]))
            conn.commit()
            conn.close()

            # Exibir mensagem de sucesso
            messagebox.showinfo("Sucesso", "Quantidade atualizada com sucesso!")
            janela_editar.destroy()

            # Atualiza a tabela e o status de estoque após a edição
            atualizar_tabela(tabela, projeto_selecionado, janela_listar)

        except ValueError as ve:
            messagebox.showerror("Erro", str(ve))
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao atualizar quantidade: {e}")
    
    # Janela para editar a quantidade
    janela_editar = tk.Toplevel()
    janela_editar.title("Editar Quantidade")
    janela_editar.geometry("300x200")

    centralizar_janela(janela_editar, 300, 200)

    # Exibir informações do componente
    tk.Label(janela_editar, text=f"Editar quantidade para {componente['nome']} ({componente['codigo']})").pack(pady=10)

    # Campo de entrada para nova quantidade
    tk.Label(janela_editar, text="Nova Quantidade:").pack(pady=5)
    entry_quantidade = tk.Entry(janela_editar)
    entry_quantidade.pack(pady=5)
    entry_quantidade.insert(0, componente["quantidade_por_placa"])  # Preencher com a quantidade atual

    entry_quantidade.focus_set()  # Colocar o foco no campo de entrada

    # Botão para salvar a nova quantidade
    tk.Button(janela_editar, text="Salvar", command=salvar_edicao).pack(pady=10)

# Função para atualizar a tabela de componentes
def atualizar_tabela(tabela, projeto_selecionado, janela_listar):
    """Função para atualizar a tabela de componentes exibida na interface."""
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
        if not hasattr(atualizar_tabela, 'mensagem_label'):
            atualizar_tabela.mensagem_label = tk.Label(janela_listar, text=f"Nenhum componente encontrado para o projeto '{projeto}'.")
            atualizar_tabela.mensagem_label.pack(pady=10)
        else:
            atualizar_tabela.mensagem_label.config(text=f"Nenhum componente encontrado para o projeto '{projeto}'.")

# Função para abrir a janela de listagem de componentes
def abrir_aba_listar_componentes(projeto_list):
    janela_listar = tk.Toplevel()
    janela_listar.title("Listar Componentes")
    janela_listar.geometry("820x550")

    centralizar_janela(janela_listar, 820, 550)

    try:
        logo_path = os.path.join(basedir, "logo.png")
        logo = PhotoImage(file=logo_path)
        logo = logo.subsample(4, 4)
        tk.Label(janela_listar, image=logo).pack(pady=10)
        janela_listar.logo = logo
    except tk.TclError:
        print("Erro ao carregar a imagem da logo para listar componentes.")

    texto = "LISTAR COMPONENTES"
    tk.Label(janela_listar, text=texto, font=("Arial", 16)).pack(pady=10)

    tk.Label(janela_listar, text="Selecione o Projeto:").pack(anchor="w", padx=10, pady=5)
    
    # Aqui adicionamos o OptionMenu para selecionar o projeto
    projeto_selecionado = tk.StringVar()
    projeto_menu = tk.OptionMenu(janela_listar, projeto_selecionado, *projeto_list)
    projeto_menu.pack(fill="x", padx=10, pady=5)

    if projeto_list:
        projeto_selecionado.set(projeto_list[0])  # Seleciona o primeiro projeto por padrão

    frame_tabela = tk.Frame(janela_listar)
    frame_tabela.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(frame_tabela)
    scrollbar.pack(side="right", fill="y")

    colunas = ("Código", "Nome", "Quantidade por Placa", "Quantidade Disponível")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", yscrollcommand=scrollbar.set)
    
    scrollbar.config(command=tabela.yview)

    for coluna in colunas:
        tabela.heading(coluna, text=coluna)
        if coluna in ("Código", "Quantidade por Placa", "Quantidade Disponível"):
            tabela.column(coluna, anchor="center")
        else:
            tabela.column(coluna, anchor="w")

    tabela.pack(fill="both", expand=True)

    # Chama a função atualizar_tabela para preencher a tabela pela primeira vez
    atualizar_tabela(tabela, projeto_selecionado, janela_listar)

    # Frame para botões "Atualizar", "Editar" e "Cancelar"
    frame_botoes = tk.Frame(janela_listar)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Atualizar", command=lambda: atualizar_tabela(tabela, projeto_selecionado, janela_listar)).pack(side="left", padx=10)

    def editar_componente():
        selecionado = tabela.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um componente para editar.")
            return
        
        item = tabela.item(selecionado)
        componente = {
            "codigo": item["values"][0],
            "nome": item["values"][1],
            "quantidade_por_placa": item["values"][2],
                        "quantidade_disponivel": item["values"][3]
        }
        editar_quantidade(componente, tabela, projeto_selecionado, janela_listar)

    # Botão para editar a quantidade do componente selecionado
    tk.Button(frame_botoes, text="Editar Quantidade", command=editar_componente).pack(side="left", padx=10)

    # Botão para fechar a janela
    tk.Button(frame_botoes, text="Cancelar", command=janela_listar.destroy).pack(side="left", padx=10)

    janela_listar.mainloop()

# Função para abrir a listagem de componentes
def abrir_listar_componentes():
    projetos = obter_lista_projetos()  # Obtém a lista de projetos
    if projetos:
        abrir_aba_listar_componentes(projetos)
    else:
        messagebox.showwarning("Atenção", "Nenhum projeto encontrado no banco de dados.")

# Exemplo de uso: Chamar a função para listar componentes (seria chamada a partir da interface principal)
# root = tk.Tk()
# abrir_listar_componentes()
# root.mainloop()

