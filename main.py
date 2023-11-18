from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contatos.db'
db = SQLAlchemy(app)

class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(9), nullable=False)
    email = db.Column(db.String(30), nullable=False)

    def __init__(self, nome, sobrenome, telefone, email):
        self.nome = nome
        self.sobrenome = sobrenome
        self.telefone = telefone
        self.email = email

@app.route('/')
def index():
    with app.app_context():
        contatos = Contato.query.all()
    return render_template('index.html', contatos=contatos)

@app.route('/visualizacao')
def visualizacao():
    with app.app_context():
        contatos = Contato.query.all()
    return render_template('visualizacao.html', contatos=contatos)

@app.route('/adicionar_contato', methods=['POST'])
def adicionar_contato():
    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        telefone = request.form['telefone']
        email = request.form['email']

        novo_contato = Contato(nome=nome, sobrenome=sobrenome, telefone=telefone, email=email)

        with app.app_context():
            db.session.add(novo_contato)
            db.session.commit()

    return redirect(url_for('visualizacao'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
