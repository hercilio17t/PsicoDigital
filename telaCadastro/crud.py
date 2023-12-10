import sqlite3
import bcrypt

def insert_usuario(email, cpf, role, hashed_password):
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO usuarios (email, cpf, role, hashed_password) VALUES (?, ?, ?, ?)',
                   (email, cpf, role, hashed_password))

    conn.commit()
    conn.close()

def get_usuario_by_email(email):
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
    usuario = cursor.fetchone()

    conn.close()
    return usuario
