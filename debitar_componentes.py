import os
import tkinter as tk
from tkinter import PhotoImage, messagebox
import sqlite3
import sys

# Obtenha o caminho absoluto do diretório atual
basedir = os.path.dirname(os.path.abspath(__file__))

def verificar_estoque_minimo(projeto_id):
    conn = conectar_banco()
    if conn:
        with conn:
            cursor = conn.cursor()
            # Obtém o limite mínimo e o estoque atual do projeto
            cursor.execute("SELECT limite_minimo FROM Projetos WHERE id = ?", (projeto_id,))
            limite_minimo = cursor.fetchone()
            
            if limite_minimo:
                limite_minimo = limite_minimo[0]
                cursor.execute("SELECT SUM(quantidade_disponivel) FROM Componentes WHERE id_projeto = ?", (projeto_id,))
                estoque_atual = cursor.fetchone()[0]

                if estoque_atual is not None and estoque_atual <= limite_minimo:
                    messagebox.showwarning("Aviso", f"O estoque atual é {estoque_atual}, o que está igual ou abaixo do limite mínimo ({limite_minimo}) para este projeto.")
                else:
                    print(f"Estoque atual ({estoque_atual}) está acima do limite mínimo ({limite_minimo}).")

def get_file_path(filename):
    if getattr(sys, 'frozen', False):  # Se estiver rodando como um executável
        base_path = sys._MEIPASS  # Diretório temporário usado pelo PyInstaller
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, filename)

def conectar_banco():
    try:
        conn = sqlite3.connect(get_file_path('estoque.db'))
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

def obter_id_projeto(nome_projeto):
    conn = conectar_banco()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM Projetos WHERE nome = ?", (nome_projeto,))
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0]
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao acessar o banco de dados: {e}")
        finally:
            conn.close()
    return None

def debitar_componentes():
    def obter_projetos():
        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT nome FROM Projetos")
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
                cursor.execute(""" 
                    SELECT c.nome, c.quantidade_disponivel, c.quantidade_por_placa
                    FROM Componentes c
                    JOIN Projetos p ON c.id_projeto = p.id
                    WHERE p.nome = ?
                """, (projeto,))
                componentes = [
                    {"nome": row[0], "quantidade_disponivel": row[1], "quantidade_por_placa": row[2]}
                    for row in cursor.fetchall()
                ]
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao acessar o banco de dados: {e}")
                componentes = []
            finally:
                conn.close()
            return componentes

    def debitar():
        projeto_selecionado = projeto_selecionado_var.get()
        if projeto_selecionado:
            confirmar = messagebox.askyesno("Confirmar Débito", f"Você tem certeza que deseja debitar os componentes do projeto '{projeto_selecionado}'?")
            if confirmar:
                componentes = obter_componentes(projeto_selecionado)
                if componentes:
                    conn = conectar_banco()
                    if conn:
                        try:
                            cursor = conn.cursor()
                            projeto_id = obter_id_projeto(projeto_selecionado)  # Obtém o projeto_id
                            for comp in componentes:
                                nova_quantidade = comp["quantidade_disponivel"] - comp["quantidade_por_placa"]
                                nova_quantidade = max(nova_quantidade, 0)
                                # Atualizando a quantidade de componentes para o projeto específico
                                cursor.execute("""
                                    UPDATE Componentes
                                    SET quantidade_disponivel = ?
                                    WHERE nome = ? AND id_projeto = ?
                                """, (nova_quantidade, comp["nome"], projeto_id))
                            conn.commit()
                            messagebox.showinfo("Info", "Componentes debitados com sucesso.")
                            verificar_estoque_minimo(projeto_id)  # Verifica o estoque mínimo após o débito
                        except sqlite3.Error as e:
                            messagebox.showerror("Erro", f"Erro ao atualizar o banco de dados: {e}")
                        finally:
                            conn.close()
                        janela.destroy()  # Fecha a janela de débito após sucesso
                    else:
                        messagebox.showwarning("Aviso", "Nenhum componente encontrado para o projeto selecionado.")
                else:
                    janela.destroy()  # Fecha a janela se o usuário cancelar
            else:
                janela.destroy()  # Fecha a janela se o usuário cancelar
        else:
            messagebox.showwarning("Aviso", "Selecione um projeto.")

    # Criar janela de débito
    janela = tk.Toplevel()
    janela.title("Debitar Componentes")
    janela.geometry("430x260")  # Ajuste o tamanho da janela 

    # Adicionando logo
    try:
        logo_path = os.path.join(basedir, "logo.png")
        logo = tk.PhotoImage(file=logo_path)
        logo = logo.subsample(4, 4)  # Reduz a imagem para se ajustar ao tamanho da tela
        logo_label = tk.Label(janela, image=logo) # Cria o Label com a imagem do logo
        logo_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
        janela.logo = logo  # Mantém uma referência ao logo para evitar que o Python o descarte
    except tk.TclError:
        print("Erro ao carregar a imagem do logotipo para a janela de cadastro de projeto.")

    # Adicionando seleção de projetos e botão
    tk.Label(janela, text="Selecione um Projeto", font=('Arial', 12, 'bold')).grid(row=1, column=0, columnspan=2, pady=10)
    
    projeto_selecionado_var = tk.StringVar(janela)
    projetos = obter_projetos()
    if projetos:
        projeto_menu = tk.OptionMenu(janela, projeto_selecionado_var, *projetos)
        projeto_menu.grid(row=2, column=0, columnspan=2, pady=10, padx=20)
        
        tk.Button(janela, text="Debitar Componentes", command=debitar, width=20, height=2).grid(row=3, column=0, columnspan=2, pady=10)
    else:
        tk.Label(janela, text="Nenhum projeto encontrado.", font=('Arial', 12)).grid(row=2, column=0, columnspan=2, pady=10)

    janela.mainloop()
