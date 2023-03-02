from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib

app = Flask(__name__, template_folder="templates")
app.secret_key = 'internetemSI2023Jorge'

# Adicionar a função len() ao contexto global do Jinja2
app.jinja_env.globals.update(len=len)

@app.route('/')
def index():
    if 'autenticado' in session:
        conn = sqlite3.connect('celulares.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM celulares")
        celulares = cur.fetchall()
        conn.close()
        return render_template('index.html', celulares=celulares)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('autenticado', None)
    return redirect(url_for('index'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
         # Insere o usuário e senha na tabela de usuários
        conn = sqlite3.connect('celulares.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO usuarios (usuario, senha) VALUES (?, ?)', (usuario, senha))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('login'))
    return render_template('cadastro.html')

    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        # Verifica se o usuário e senha são válidos
        conn = sqlite3.connect('celulares.db')
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM usuarios WHERE usuario = ? AND senha = ?', (usuario, senha))
        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        if resultado[0] == 1:
            session['autenticado'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', erro='Usuário ou senha invalidos')
    return render_template('login.html')

    


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor = request.form['valor']
        quantidade = request.form['quantidade']

        conn = sqlite3.connect('celulares.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO celulares (nome, descricao, valor, quantidade) VALUES (?, ?, ?, ?)", (nome, descricao, valor, quantidade))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    else:
        return render_template('add.html')

@app.route('/delete')
def delete():
    id = request.args.get('id')

    conn = sqlite3.connect('celulares.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM celulares WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/update/<id>', methods=['POST'])
def update(id):

    nome = request.form['nome']
    descricao = request.form['descricao']
    valor = request.form['valor']
    quantidade = request.form['quantidade']

    conn = sqlite3.connect('celulares.db')
    cur = conn.cursor()
    cur.execute("UPDATE celulares SET nome=?, descricao=?, valor=?, quantidade=? WHERE id=?", (nome, descricao, valor, quantidade, id))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


@app.route('/edit')
def edit():
    id = request.args.get('id')

    conn = sqlite3.connect('celulares.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM celulares WHERE id=?", (id,))
    celular = cur.fetchone()
    conn.close()

    return render_template('edit.html', celular=celular)


if __name__ == '__main__':
    app.run(debug=True)
