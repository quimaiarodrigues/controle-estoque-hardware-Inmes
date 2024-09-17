import os
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Obtenha o caminho absoluto do diretório atual
basedir = os.path.dirname(os.path.abspath(__file__))

def conectar_banco():
    try:
        # Use o caminho absoluto para garantir que o executável encontre o banco de dados
        conn = sqlite3.connect(os.path.join(basedir, 'estoque.db'))
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

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

    def adicionar_componente():
        projeto = projeto_selecionado.get()
        if projeto:
            adicionar_janela = tk.Toplevel()
            adicionar_janela.title("Adicionar Componente")
            adicionar_janela.geometry("400x250")

            tk.Label(adicionar_janela, text="Código do Componente:").pack(anchor="w", padx=10, pady=5)
            codigo_entry = tk.Entry(adicionar_janela)
            codigo_entry.pack(fill="x", padx=10, pady=5)

            tk.Label(adicionar_janela, text="Nome do Componente:").pack(anchor="w", padx=10, pady=5)
            nome_entry = tk.Entry(adicionar_janela)
            nome_entry.pack(fill="x", padx=10, pady=5)

            tk.Label(adicionar_janela, text="Quantidade por Placa:").pack(anchor="w", padx=10, pady=5)
            quantidade_por_placa_entry = tk.Entry(adicionar_janela)
            quantidade_por_placa_entry.pack(fill="x", padx=10, pady=5)

            tk.Label(adicionar_janela, text="Quantidade Disponível:").pack(anchor="w", padx=10, pady=5)
            quantidade_disponivel_entry = tk.Entry(adicionar_janela)
            quantidade_disponivel_entry.pack(fill="x", padx=10, pady=5)

            def salvar_componente():
                codigo = codigo_entry.get().strip()
                nome = nome_entry.get().strip()
                try:
                    quantidade_por_placa = int(quantidade_por_placa_entry.get().strip())
                    quantidade_disponivel = int(quantidade_disponivel_entry.get().strip())
                except ValueError:
                    messagebox.showwarning("Aviso", "Quantidade deve ser um número inteiro.")
                    return
                
                if codigo and nome:
                    conn = conectar_banco()
                    if conn:
                        try:
                            cursor = conn.cursor()
                            cursor.execute("SELECT id FROM Projetos WHERE nome = ?", (projeto,))
                            projeto_id = cursor.fetchone()[0]
                            
                            cursor.execute("""
                                INSERT INTO Componentes (codigo, nome, quantidade_por_placa, quantidade_disponivel, id_projeto)
                                VALUES (?, ?, ?, ?, ?)
                            """, (codigo, nome, quantidade_por_placa, quantidade_disponivel, projeto_id))
                            conn.commit()
                            adicionar_janela.destroy()
                            atualizar_tabela()
                            messagebox.showinfo("Info", "Componente adicionado com sucesso!")
                        except sqlite3.Error as e:
                            messagebox.showerror("Erro", f"Erro ao atualizar o banco de dados: {e}")
                        finally:
                            conn.close()
                else:
                    messagebox.showwarning("Aviso", "Código e nome do componente não podem estar vazios.")

            tk.Button(adicionar_janela, text="Salvar", command=salvar_componente).pack(pady=10)
            tk.Button(adicionar_janela, text="Cancelar", command=adicionar_janela.destroy).pack(pady=10)

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
    janela_deletar.geometry("800x500")

    # Adicionando logo
    try:
        logo = tk.PhotoImage(file=os.path.join(basedir, "logo.png"))
        logo = logo.subsample(4, 4)
        tk.Label(janela_deletar, image=logo).pack(pady=10)
        janela_deletar.logo = logo
    except tk.TclError:
        print("Erro ao carregar a imagem da logo para gerenciar componentes.")

    # Adicionando texto abaixo da logo
    texto = "Gerenciar Componentes"
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

    # Botões para atualizar, adicionar, deletar e cancelar
    frame_botoes = tk.Frame(janela_deletar)
    frame_botoes.pack(pady=10)

    #tk.Button(frame_botoes, text="Atualizar", command=atualizar_tabela).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Deletar Componente", command=deletar_componente).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Cancelar", command=janela_deletar.destroy).pack(side=tk.LEFT, padx=5)

    atualizar_tabela()
    janela_deletar.mainloop()

# Inicia a aplicação
if __name__ == "__main__":
    abrir_janela()
