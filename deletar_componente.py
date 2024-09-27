import os
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Obtenha o caminho absoluto do diretório atual
basedir = os.path.dirname(os.path.abspath(__file__)) #PARA ERVIDOR COMENTAR 

# Definir o caminho do banco de dados com base no ambiente
if os.environ.get("ENVIRONMENT") == "production":
    caminho_banco = "C:/Users/ICARO/Desktop/db/estoque.db"
else:
    caminho_banco = os.path.join(basedir, 'estoque.db')

def conectar_banco():
    try:
        conn = sqlite3.connect(caminho_banco) 
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

def centralizar_janela(janela, largura, altura):
    # Calcula a posição x e y para centralizar a janela
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def abrir_janela():
    def obter_projetos():
        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT nome FROM Projetos")  # Certifique-se de que a tabela 'Projetos' existe
                projetos = [row[0] for row in cursor.fetchall()]
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao acessar o banco de dados: {e}")
                projetos = []
            finally:
                conn.close()
            return projetos

    def obter_componentes(projeto):
        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM Projetos WHERE nome = ?", (projeto,))
                projeto_id = cursor.fetchone()
                
                if projeto_id is None:
                    return []  # Nenhum projeto encontrado
                
                projeto_id = projeto_id[0]
                
                cursor.execute(""" 
                    SELECT c.codigo, c.nome, c.quantidade_por_placa, c.quantidade_disponivel
                    FROM Componentes c
                    WHERE c.id_projeto = ?
                """, (projeto_id,))
                
                componentes = [
                    {"codigo": row[0], "nome": row[1], "quantidade_por_placa": row[2], "quantidade_disponivel": row[3]}
                    for row in cursor.fetchall()
                ]
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao acessar o banco de dados: {e}")
                componentes = []
            finally:
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
        projeto = projeto_selecionado.get()
        selecionado = tabela.selection()
        if selecionado:
            codigo = tabela.item(selecionado[0], 'values')[0]
            confirmar = messagebox.askyesno("Confirmar Exclusão", f"Você tem certeza que deseja deletar o componente '{codigo}' do projeto '{projeto}'?")
            if confirmar:
                conn = conectar_banco()
                if conn:
                    try:
                        cursor = conn.cursor()
                        cursor.execute("SELECT id FROM Projetos WHERE nome = ?", (projeto,))
                        projeto_id = cursor.fetchone()[0]
                        
                        cursor.execute("DELETE FROM Componentes WHERE codigo = ? AND id_projeto = ?", (codigo, projeto_id))
                        conn.commit()
                        tabela.delete(selecionado[0])
                        messagebox.showinfo("Info", "Componente deletado com sucesso!")
                    except sqlite3.Error as e:
                        messagebox.showerror("Erro", f"Erro ao atualizar o banco de dados: {e}")
                    finally:
                        conn.close()
        else:
            messagebox.showwarning("Seleção inválida", "Selecione um componente para deletar.")

    janela_deletar = tk.Toplevel()
    janela_deletar.title("Gerenciar Componentes")
    janela_deletar.geometry("850x500")
    centralizar_janela(janela_deletar, 850, 500)

    # Faz com que a janela de deletar fique sempre na frente da janela principal
    janela_deletar.transient()  # A janela se torna temporária e fica na frente
    janela_deletar.focus_force()  # Traz a janela para o foco imediatamente
    janela_deletar.grab_set()  # Faz com que a janela principal não receba eventos enquanto essa estiver aberta

    # Adicionando logo
    try:
        logo = tk.PhotoImage(file=os.path.join(basedir, "logo.png"))
        logo = logo.subsample(4, 4)
        tk.Label(janela_deletar, image=logo).pack(pady=10)
        janela_deletar.logo = logo
    except tk.TclError:
        print("Erro ao carregar a imagem da logo para gerenciar componentes.")

    # Adicionando texto abaixo da logo
    texto = "GERENCIAR COMPONENTES"
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

    # Definindo cabeçalhos e alinhamento das colunas da tabela
    for coluna in colunas:
        tabela.heading(coluna, text=coluna, anchor=tk.CENTER)  # Cabeçalhos centralizados

    # Definindo alinhamento central para os valores das colunas
    tabela.column("Código", anchor=tk.CENTER, width=100)
    tabela.column("Nome", anchor=tk.CENTER, width=200)
    tabela.column("Quantidade por Placa", anchor=tk.CENTER, width=150)
    tabela.column("Quantidade Disponível", anchor=tk.CENTER, width=150)

    tabela.pack(fill="both", expand=True)

    # Botões para adicionar, deletar e cancelar
    frame_botoes = tk.Frame(janela_deletar)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Deletar Componente", command=deletar_componente).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Cancelar", command=janela_deletar.destroy).pack(side=tk.LEFT, padx=5)

    atualizar_tabela()
    janela_deletar.mainloop()

# Inicia a aplicação
if __name__ == "__main__":
    abrir_janela()
