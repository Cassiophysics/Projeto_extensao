import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

def adicionar_colunas():
    with sqlite3.connect('biblioteca.db') as conn:
        c = conn.cursor()
        # Verifica se a coluna já existe antes de tentar adicioná-la
        c.execute('''PRAGMA table_info(livros)''')
        columns = [column[1] for column in c.fetchall()]
        if 'disponibilidade' not in columns:
            c.execute('ALTER TABLE livros ADD COLUMN disponibilidade TEXT')
        if 'data_emprestimo' not in columns:
            c.execute('ALTER TABLE livros ADD COLUMN data_emprestimo TEXT')
        if 'data_entrega' not in columns:
            c.execute('ALTER TABLE livros ADD COLUMN data_entrega TEXT')

def inserir_dados_livros():
    df = pd.read_csv('livros_brasileiros_completos.csv')
    with sqlite3.connect('biblioteca.db') as conn:
        c = conn.cursor()
        for index, row in df.iterrows():
            c.execute('''
            INSERT INTO livros (titulo, ano_publicacao) VALUES (?, ?)
            ''', (row['Título'], row['Ano de Publicação']))

def criar_tabela_usuarios():
    with sqlite3.connect('biblioteca.db') as conn:
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
        ''')

def adicionar_usuario(username, password):
    with sqlite3.connect('biblioteca.db') as conn:
        c = conn.cursor()
        # Verifica se o usuário já existe antes de tentar adicioná-lo
        c.execute('SELECT * FROM usuarios WHERE username=?', (username,))
        existing_user = c.fetchone()
        if existing_user is None:
            c.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', (username, password))
            print(f"Usuário '{username}' adicionado com sucesso.")
        else:
            print(f"Usuário '{username}' já existe.")

def gerar_valores_aleatorios():
    with sqlite3.connect('biblioteca.db') as conn:
        c = conn.cursor()
        # Gerar valores aleatórios para disponibilidade, data_emprestimo e data_entrega para cada livro
        c.execute('SELECT id FROM livros')
        livro_ids = c.fetchall()
        for livro_id in livro_ids:
            disponibilidade = random.choice(['Disponível', 'Reservado'])
            data_emprestimo = datetime.now() - timedelta(days=random.randint(1, 30))
            data_entrega = data_emprestimo + timedelta(days=random.randint(1, 14))
            c.execute('''
            UPDATE livros 
            SET disponibilidade=?, data_emprestimo=?, data_entrega=?
            WHERE id=?
            ''', (disponibilidade, data_emprestimo.strftime('%Y-%m-%d'), data_entrega.strftime('%Y-%m-%d'), livro_id[0]))

def main():
    adicionar_colunas()
    inserir_dados_livros()
    criar_tabela_usuarios()
    adicionar_usuario('Cássio', 'hashed_password_1')
    adicionar_usuario('Costa', 'hashed_password_2')
    adicionar_usuario('Santos', 'hashed_password_3')
    gerar_valores_aleatorios()

    print("Tabelas e dados inseridos com sucesso.")

if __name__ == "__main__":
    main()
