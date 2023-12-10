import sqlite3

def create_tables():
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()

    # Criação da tabela se ela não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            cpf TEXT NOT NULL,
            role TEXT NOT NULL,
            hashed_password TEXT
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
