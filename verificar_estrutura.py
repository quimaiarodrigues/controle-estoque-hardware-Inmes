import sqlite3

def verificar_estrutura_tabela(tabela_nome):
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({tabela_nome})")
    colunas = cursor.fetchall()
    conn.close()
    
    print(f"Estrutura da tabela {tabela_nome}:")
    for coluna in colunas:
        print(coluna)

verificar_estrutura_tabela('projetos')
verificar_estrutura_tabela('componentes')
