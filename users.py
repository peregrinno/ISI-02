import sqlite3

conn = sqlite3.connect('celulares.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
''')

# Insere um usuário e senha para teste
cursor.execute('INSERT INTO usuarios (usuario, senha) VALUES (?, ?)', ('luanaraujo', 'luancasa123'))
conn.commit()

cursor.close()
conn.close()
