import os
from flask import render_template, request, redirect, url_for
from app import app, db
from models import Produto, Categoria

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        categoria_id = request.form.get('categoria_id')
        
        # Tratamento da imagem (se não enviar, usa padrao.png)
        imagem = request.files.get('imagem')
        if imagem and imagem.filename != '':
            nome_imagem = imagem.filename
            caminho = os.path.join('app', 'static', 'uploads', nome_imagem)
            imagem.save(caminho)
            filename_salvo = nome_imagem
        else:
            filename_salvo = 'padrao.png'
            
        novo_produto = Produto(
            nome=nome, 
            preco=float(preco), 
            categoria_id=int(categoria_id), 
            imagem=filename_salvo
        )
        db.session.add(novo_produto)
        db.session.commit()
        return redirect(url_for('index'))
        
    categorias = Categoria.query.all()
    produtos = Produto.query.all()
    return render_template('index.html', categorias=categorias, produtos=produtos)