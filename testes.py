import os
import sys

def obter_caminho_arquivo(nome_arquivo):
    """Retorna o caminho correto para o arquivo, considerando o ambiente do executável."""
    if getattr(sys, 'frozen', False):
        # Se estiver rodando como um executável
        caminho_base = sys._MEIPASS
    else:
        # Se estiver rodando no ambiente de desenvolvimento
        caminho_base = os.path.dirname(__file__)
    return os.path.join(caminho_base, nome_arquivo)

print(f"Caminho da logo: {obter_caminho_arquivo('logo.png')}")
