# Sistema de Gestão de Produtos (Flask + SQLAlchemy)

Aplicação web desenvolvida em Python com Flask e Flask-SQLAlchemy para gerenciamento de produtos vinculados a categorias (relacionamento 1:N). O sistema conta com cadastro, listagem ordenada em ordem alfabética, busca por nome, edição com substituição de imagem, exclusão com limpeza automática de arquivos no disco (preservando padrao.png), validação de dados e upload de imagens.

## Tecnologias utilizadas
- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML5 / CSS3 / Jinja2

## Passo a passo para rodar o projeto localmente
1. Abra o terminal na pasta raiz do projeto.
2. Instale as dependências necessárias:
   ```bash
   pip install flask flask-sqlalchemy werkzeug
   Certifique-se de que a imagem padrão exista em static/uploads/padrao.png
   Inicie o servidor:
   python app.py
   Acesse no navegador: http://127.0.0.1:5000/
   Comandos Git utilizados
​git init — Inicializa um novo repositório Git na pasta do projeto.
​git add . — Adiciona todos os arquivos do projeto na área de preparação (staging), respeitando o .gitignore.
​git commit -m "feat: conclui CRUD, validações e documentação" — Registra as alterações no histórico local do Git com uma mensagem descritiva.
​git branch -M main — Define o nome da branch principal como main.
​git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git — Conecta o repositório local ao repositório público no GitHub.
​git push -u origin main — Envia os commits locais para o repositório remoto no GitHub.
