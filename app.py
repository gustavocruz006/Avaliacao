import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'chave-secreta-prova-ds1'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = os.path.join('static', 'uploads')
EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

db = SQLAlchemy(app)


class Categoria(db.Model):
    _tablename_ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    produtos = db.relationship('Produto', backref='categoria', lazy=True)


class Produto(db.Model):
    _tablename_ = 'produto'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(200), nullable=False, default='padrao.png')
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)


def extensao_valida(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS


def apagar_imagem_segura(nome_arquivo):
    if nome_arquivo and nome_arquivo != 'padrao.png':
        caminho = os.path.join(UPLOAD_FOLDER, nome_arquivo)
        if os.path.exists(caminho):
            os.remove(caminho)


def salvar_imagem(arquivo):
    if not arquivo or arquivo.filename == '':
        return 'padrao.png', None

    if not extensao_valida(arquivo.filename):
        return None, 'Extensão de imagem inválida! Use PNG, JPG, JPEG, GIF ou WEBP.'

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    nome_seguro = secure_filename(arquivo.filename)
    caminho = os.path.join(UPLOAD_FOLDER, nome_seguro)
    arquivo.save(caminho)
    return nome_seguro, None


def validar_dados_produto(nome_raw, preco_raw, categoria_id_raw):
    nome = (nome_raw or '').strip()
    if len(nome) < 3:
        return None, 'O nome do produto deve ter pelo menos 3 caracteres.'

    if not preco_raw:
        return None, 'Informe um preço válido.'

    try:
        preco = float(preco_raw.replace(',', '.'))
    except (ValueError, TypeError):
        return None, 'Preço inválido! Digite apenas números.'

    if preco <= 0:
        return None, 'O preço deve ser maior que zero.'

    if not categoria_id_raw:
        return None, 'Selecione uma categoria.'

    try:
        categoria_id = int(categoria_id_raw)
    except (ValueError, TypeError):
        return None, 'Categoria inválida.'

    if not db.session.get(Categoria, categoria_id):
        return None, 'A categoria selecionada não existe.'

    return {'nome': nome, 'preco': preco, 'categoria_id': categoria_id}, None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dados, erro = validar_dados_produto(
            request.form.get('nome'),
            request.form.get('preco'),
            request.form.get('categoria_id')
        )
        if erro:
            flash(erro, 'danger')
            return redirect(url_for('index'))

        imagem_salva, erro_img = salvar_imagem(request.files.get('imagem'))
        if erro_img:
            flash(erro_img, 'danger')
            return redirect(url_for('index'))

        novo_produto = Produto(
            nome=dados['nome'],
            preco=dados['preco'],
            categoria_id=dados['categoria_id'],
            imagem=imagem_salva
        )
        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('index'))

    busca = (request.args.get('busca') or '').strip()
    query = Produto.query
    if busca:
        query = query.filter(Produto.nome.ilike(f'%{busca}%'))

    produtos = query.order_by(Produto.nome.asc()).all()
    categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
    return render_template('index.html', categorias=categorias, produtos=produtos, busca=busca)


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    produto = Produto.query.get_or_404(id)
    categorias = Categoria.query.order_by(Categoria.nome.asc()).all()

    if request.method == 'POST':
        dados, erro = validar_dados_produto(
            request.form.get('nome'),
            request.form.get('preco'),
            request.form.get('categoria_id')
        )
        if erro:
            flash(erro, 'danger')
            return redirect(url_for('editar', id=produto.id))

        arquivo_foto = request.files.get('imagem')
        if arquivo_foto and arquivo_foto.filename != '':
            nova_imagem, erro_img = salvar_imagem(arquivo_foto)
            if erro_img:
                flash(erro_img, 'danger')
                return redirect(url_for('editar', id=produto.id))

            foto_antiga = produto.imagem
            produto.imagem = nova_imagem
            apagar_imagem_segura(foto_antiga)

        produto.nome = dados['nome']
        produto.preco = dados['preco']
        produto.categoria_id = dados['categoria_id']
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('index'))

    return render_template('editar.html', produto=produto, categorias=categorias)


@app.route('/excluir/<int:id>')
def excluir(id):
    produto = Produto.query.get_or_404(id)
    foto = produto.imagem
    db.session.delete(produto)
    db.session.commit()
    apagar_imagem_segura(foto)
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('index'))


with app.app_context():
    db.create_all()
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    if not Categoria.query.first():
        c1 = Categoria(nome='Eletrônicos')
        c2 = Categoria(nome='Roupas')
        c3 = Categoria(nome='Alimentos')
        db.session.add_all([c1, c2, c3])
        db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)