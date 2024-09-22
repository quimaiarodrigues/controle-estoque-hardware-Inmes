import sqlite3
import os

# Função para obter o caminho do banco de dados
def get_db_path():
    basedir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(basedir, 'estoque.db')

def adicionar_coluna_limite_minimo():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    try:
        cursor.execute('''
            ALTER TABLE Projetos
            ADD COLUMN limite_minimo INTEGER DEFAULT 0
        ''')
        print("Coluna 'limite_minimo' adicionada com sucesso.")
    except sqlite3.OperationalError as e:
        print(f"Erro ao adicionar a coluna: {e}")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    adicionar_coluna_limite_minimo()
