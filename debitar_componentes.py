import tkinter as tk
from tkinter import messagebox
import sqlite3

def debitar_componentes():
    def obter_projetos():
        try:
            conn = sqlite3.connect('estoque.db')
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM projetos")
            projetos = [row[0] for row in cursor.fetchall()]
            conn.close()
            return projetos
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao acessar o banco de dados: {e}")
            return []

    def obter_componentes(projeto):
        try:
            conn = sqlite3.connect('estoque.db')
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.nome, c.quantidade_disponivel, c.quantidade_por_placa
                FROM componentes c
                JOIN projetos p ON c.id_projeto = p.id
                WHERE p.nome = ?
            """, (projeto,))
            componentes = [
                {"nome": row[0], "quantidade_disponivel": row[1], "quantidade_por_placa": row[2]}
                for row in cursor.fetchall()
            ]
            conn.close()
            return componentes
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao acessar o banco de dados: {e}")
            return []

    def debitar():
        projeto_selecionado = projeto_selecionado_var.get()
        if projeto_selecionado:
            confirmar = messagebox.askyesno("Confirmar Débito", f"Você tem certeza que deseja debitar os componentes do projeto '{projeto_selecionado}'?")
            if confirmar:
                componentes = obter_componentes(projeto_selecionado)
                if componentes:
                    try:
                        conn = sqlite3.connect('estoque.db')
                        cursor = conn.cursor()
                        for comp in componentes:
                            nova_quantidade = comp["quantidade_disponivel"] - comp["quantidade_por_placa"]
                            nova_quantidade = max(nova_quantidade, 0)
                            cursor.execute("""
                                UPDATE componentes
                                SET quantidade_disponivel = ?
                                WHERE nome = ?
                            """, (nova_quantidade, comp["nome"]))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Info", "Componentes debitados com sucesso!")
                    except sqlite3.Error as e:
                        messagebox.showerror("Erro", f"Erro ao atualizar o banco de dados: {e}")
                else:
                    messagebox.showwarning("Aviso", "Nenhum componente encontrado para o projeto selecionado.")
                janela_debito.destroy()
            else:
                janela_debito.destroy()
        else:
            messagebox.showwarning("Aviso", "Nenhum projeto selecionado.")

    janela_debito = tk.Toplevel()
    janela_debito.title("Debitar Componentes")
    janela_debito.geometry("400x130")

    tk.Label(janela_debito, text="Selecione o Projeto:").pack(anchor="w", padx=10, pady=5)
    
    projeto_selecionado_var = tk.StringVar()
    projetos = obter_projetos()
    projeto_selecionado_var.set(projetos[0] if projetos else '')  # Define um valor padrão

    projeto_combobox = tk.OptionMenu(janela_debito, projeto_selecionado_var, *projetos)
    projeto_combobox.pack(fill="x", padx=10, pady=5)

    frame_botoes = tk.Frame(janela_debito)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Debitar", command=debitar).pack(side="left", padx=10)
    tk.Button(frame_botoes, text="Cancelar", command=janela_debito.destroy).pack(side="left", padx=10)

# Para iniciar a função
# debitar_componentes()
