from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask import request
import hashlib

app = Flask(__name__, template_folder="templates")
app.secret_key = 'internetemSI2023Jorge'

# Adicionar a função len() ao contexto global do Jinja2
app.jinja_env.globals.update(len=len)
usuario = ""

# variáveis globais para armazenar os itens do carrinho e o total
cartItems = {}
cartTotal = 0

@app.route('/adicionar-ao-carrinho', methods=['POST'])
def adicionarAoCarrinho():
    # extrair o nome do celular do id do botão
    nomeCelular = request.form['nome-celular']

    conn = sqlite3.connect('celulares.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM celulares")
    celulares = cur.fetchall()
    cur.close()
    conn.close()

    # encontrar o celular na lista de celulares
    celular = [celular for celular in celulares if celular[1] == nomeCelular]

    # verificar se o celular foi encontrado
    if celular:
        # atualiza o objeto do carrinho
        itemId = celular[1]
        itemPreco = float(celular[3])
        if cartItems.get(itemId):
            cartItems[itemId]['quantidade'] += 1
            cartItems[itemId]['total'] = itemPreco * cartItems[itemId]['quantidade']
        else:
            cartItems[itemId] = {
                'nome': celular[2],
                'preco': itemPreco,
                'quantidade': 1,
                'total': itemPreco
            }
        # atualiza o total do carrinho
        cartTotal += itemPreco

        # retorna uma resposta vazia, já que o HTML será atualizado por meio de JavaScript
        return ''
    else:
        # retorna uma mensagem de erro
        return 'Celular não encontrado: ' + nomeCelular


@app.route('/')
def market():
    conn = sqlite3.connect('celulares.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM celulares")
    celulares = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('market.html', celulares=celulares)

@app.route('/index')
def index():
    if 'autenticado' in session:
        conn = sqlite3.connect('celulares.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM celulares")
        celulares = cur.fetchall()
        cur.execute('SELECT usuario FROM usuarios WHERE id = 1')
        usuario = cur.fetchone()[0]
        print (usuario)
        cur.close()
        conn.close()

        return render_template('index.html', celulares=celulares, usuario=usuario)
    return redirect(url_for('login'))

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('autenticado', None)
    
    return redirect(url_for('login'))

    
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

