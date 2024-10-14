import sqlite3
import os
from tkinter import messagebox
import sys

#finalizado 

# Função para conectar ao banco de dados
def conectar_banco():
    try:
        # Use o caminho absoluto para garantir que o executável encontre o banco de dados
        conn = sqlite3.connect(caminho_banco)
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados atualiza db: {e}")
        return None

# Detecta se está rodando como executável ou como script Python
if getattr(sys, 'frozen', False):
    # Está rodando como um executável
    os.environ["ENVIRONMENT"] = "production"
else:
    # Está rodando como script Python normal
    os.environ["ENVIRONMENT"] = "development"

# Obtenha o caminho absoluto do diretório atual
basedir = os.path.dirname(os.path.abspath(__file__))

# Definir o caminho do banco de dados com base no ambiente
if os.environ.get("ENVIRONMENT") == "production":
    caminho_banco = "C:/Users/ICARO/Desktop/db/estoque.db"
else:
    caminho_banco = os.path.join(basedir, 'estoque.db')

# Função para adicionar a coluna limite_minimo
def adicionar_coluna_limite_minimo():
    conn = conectar_banco()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                ALTER TABLE Projetos
                ADD COLUMN limite_minimo INTEGER DEFAULT 0
            ''')
            print("Coluna 'limite_minimo' adicionada com sucesso.")
            conn.commit()
        except sqlite3.OperationalError as e:
            print(f"Erro ao adicionar a coluna: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    adicionar_coluna_limite_minimo()
