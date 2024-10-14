# controle-estoque-hardware-Inmes

Autor: Icaro Dão Quimaia Rodrigues  14/10/2024

Controle de Estoque de Componentes - INMES

Este projeto foi desenvolvido para o INMES , com o objetivo de facilitar e otimizar o controle de estoque de componentes eletrônicos usados ​​na montagem de máquinas de marcenaria. O sistema permite gerenciar o cadastro de componentes, controlar o estoque, registrar o uso de componentes em projetos específicos e emitir alertas sobre a disponibilidade de peças.

Funcionalidades

Cadastro de Projetos : Cadastre novos projetos com informações sobre os componentes necessários.

Cadastro de Componentes : Adicione e edite informações de componentes, incluindo quantidade em estoque e especificações.

Controle de Estoque : Adicione ou debite componentes usados ​​em projetos, com verificação automática da quantidade disponível.

Avisos de Estoque : Alertas automáticos são exibidos quando o estoque é insuficiente para a montagem de uma nova unidade, ajudando a evitar paradas de produção.

Tecnologias Utilizadas

Linguagem : Python

Banco de Dados : SQLite

Interface Gráfica : Visual Studio Code

Bibliotecas : PyInstaller (para criação), Pandas (para manipulação de dados)

Instalação e Configuração

Clone o Repositório : 
[git clone https://github.com/usuario/inmes-estoque-componentes.git](https://github.com/quimaiarodrigues/controle-estoque-hardware-Inmes?tab=readme-ov-file)

cd inmes-estoque-componentes

Instale as Dependências : Certifique-se de que o Python e o pip estão instalados. Em seguida, execute:
python -m pip install -r requirements.txt

Execução do Sistema : Para executar o sistema, basta rodar o arquivo principal:
python main.py

Criação do Executável : Para gerar o seguintevel, use o comando:
pyinstaller --onefile main.py


Contribuição

Este sistema é uma solução interna para o INMES, mas as melhorias são sempre bem-vindas. Se desejar contribuir, faça um fork deste repositório, crie um branch para suas alterações e envie um pull request .

Licença

Este projeto é de uso interno para o INMES e está sob uma licença restrita. Para mais informações, entre em contato com o setor de engenharia.



