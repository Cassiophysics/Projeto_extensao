import tkinter as tk
from tkinter import ttk
import sqlite3

import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

def fazer_login_administrativo():
    # Fechar a janela principal
    root.withdraw()
    
    # Criar a janela de login
    janela_login = tk.Toplevel()
    janela_login.title("Login Administrativo")

    # Widgets de login
    label_usuario = tk.Label(janela_login, text="Usuário:")
    label_usuario.grid(row=0, column=0, padx=10, pady=5)
    entry_usuario = tk.Entry(janela_login)
    entry_usuario.grid(row=0, column=1, padx=10, pady=5)

    label_senha = tk.Label(janela_login, text="Senha:")
    label_senha.grid(row=1, column=0, padx=10, pady=5)
    entry_senha = tk.Entry(janela_login, show="*")
    entry_senha.grid(row=1, column=1, padx=10, pady=5)

    btn_login = tk.Button(janela_login, text="Login", command=lambda: verificar_credenciais(entry_usuario.get(), entry_senha.get()))
    btn_login.grid(row=2, columnspan=2, padx=10, pady=5)

    # Função para verificar as credenciais de login
    def verificar_credenciais(username, password):
        # Conectar ao banco de dados e verificar as credenciais
        conn = sqlite3.connect('biblioteca.db')
        c = conn.cursor()
        c.execute('SELECT * FROM usuarios WHERE username=? AND password=?', (username, password))
        usuario = c.fetchone()
        conn.close()

        if usuario:
            abrir_interface_administrativa()
            janela_login.destroy()  # Fechar a janela de login após o login bem-sucedido
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha incorretos.")

def abrir_interface_administrativa():
    # Criar a janela da interface administrativa
    janela_administrativa = tk.Toplevel()
    janela_administrativa.title("Interface Administrativa")

    # Adicionar widgets e funcionalidades da interface administrativa aqui
    label_titulo = tk.Label(janela_administrativa, text="Bem-vindo à Interface Administrativa")
    label_titulo.pack(padx=10, pady=10)

    # Botão "Adicionar Livro"
    btn_adicionar_livro = tk.Button(janela_administrativa, text="Adicionar Livro", command=adicionar_livro)
    btn_adicionar_livro.pack(pady=5)

    # Botão "Remover Livro"
    btn_remover_livro = tk.Button(janela_administrativa, text="Remover Livro", command=remover_livro)
    btn_remover_livro.pack(pady=5)

    # Botão "Editar Livro"
    btn_editar_livro = tk.Button(janela_administrativa, text="Editar Livro", command=editar_livro)
    btn_editar_livro.pack(pady=5)

    # Botão "Voltar para o Sistema de Bibliotecas Comunitárias"
    btn_voltar = tk.Button(janela_administrativa, text="Voltar", command=lambda: voltar_para_principal(janela_administrativa))
    btn_voltar.pack(pady=5)

def voltar_para_principal(janela_atual):
    # Mostrar a janela principal e fechar a janela atual
    root.deiconify()
    janela_atual.destroy()

def adicionar_livro():
    # Abrir uma nova janela para inserção dos dados do novo livro
    janela_adicionar = tk.Toplevel()
    janela_adicionar.title("Adicionar Livro")

    # Widgets para inserção dos dados do livro
    label_titulo = tk.Label(janela_adicionar, text="Título:")
    label_titulo.grid(row=0, column=0, padx=10, pady=5)
    entry_titulo = tk.Entry(janela_adicionar)
    entry_titulo.grid(row=0, column=1, padx=10, pady=5)

    label_ano = tk.Label(janela_adicionar, text="Ano de Publicação:")
    label_ano.grid(row=1, column=0, padx=10, pady=5)
    entry_ano = tk.Entry(janela_adicionar)
    entry_ano.grid(row=1, column=1, padx=10, pady=5)

    # Botão para confirmar a adição do livro
    btn_confirmar = tk.Button(janela_adicionar, text="Confirmar", command=lambda: confirmar_adicao(entry_titulo.get(), entry_ano.get()))
    btn_confirmar.grid(row=2, columnspan=2, padx=10, pady=5)

    # Função para confirmar a adição do livro ao banco de dados
    def confirmar_adicao(titulo, ano):
        # Conectar ao banco de dados e executar a inserção dos dados
        conn = sqlite3.connect('biblioteca.db')
        c = conn.cursor()
        c.execute('INSERT INTO livros (titulo, ano_publicacao) VALUES (?, ?)', (titulo, ano))
        conn.commit()
        conn.close()

        # Fechar a janela de adicionar livro
        janela_adicionar.destroy()

        # Atualizar a visualização dos livros na interface principal
        filtrar_livros()

def remover_livro():
    # Função para remover um livro do banco de dados
    janela_remover = tk.Toplevel()
    janela_remover.title("Remover Livro")

    # Barra de pesquisa para escolher o livro a ser removido
    label_pesquisa_remover = tk.Label(janela_remover, text="Pesquisar Livro:")
    label_pesquisa_remover.grid(row=0, column=0, padx=10, pady=5)
    entry_pesquisa_remover = tk.Entry(janela_remover)
    entry_pesquisa_remover.grid(row=0, column=1, padx=10, pady=5)

    btn_pesquisar_remover = tk.Button(janela_remover, text="Pesquisar", command=lambda: pesquisar_livro_remover(entry_pesquisa_remover.get()))
    btn_pesquisar_remover.grid(row=0, column=2, padx=10, pady=5)

    # Função para pesquisar o livro a ser removido
    def pesquisar_livro_remover(termo_pesquisa):
        conn = sqlite3.connect('biblioteca.db')
        c = conn.cursor()
        c.execute('SELECT * FROM livros WHERE titulo LIKE ?', ('%' + termo_pesquisa + '%',))
        livros = c.fetchall()
        conn.close()

        if livros:
            # Mostrar os livros encontrados em uma lista
            lista_livros = tk.Listbox(janela_remover)
            lista_livros.grid(row=1, columnspan=3, padx=10, pady=5)

            for livro in livros:
                lista_livros.insert(tk.END, livro[1])

            # Botão para confirmar a remoção do livro selecionado
            btn_confirmar_remover = tk.Button(janela_remover, text="Remover", command=lambda: confirmar_remocao(lista_livros.get(tk.ACTIVE)))
            btn_confirmar_remover.grid(row=2, columnspan=3, padx=10, pady=5)
        else:
            messagebox.showinfo("Livro não encontrado", "Nenhum livro correspondente foi encontrado.")

    # Função para confirmar a remoção do livro selecionado
    def confirmar_remocao(titulo_livro):
        conn = sqlite3.connect('biblioteca.db')
        c = conn.cursor()
        c.execute('DELETE FROM livros WHERE titulo=?', (titulo_livro,))
        conn.commit()
        conn.close()
        janela_remover.destroy()
        filtrar_livros()

def editar_livro():
    # Função para editar um livro no banco de dados
    janela_editar = tk.Toplevel()
    janela_editar.title("Editar Livro")

    # Barra de pesquisa para escolher o livro a ser editado
    label_pesquisa_editar = tk.Label(janela_editar, text="Pesquisar Livro:")
    label_pesquisa_editar.grid(row=0, column=0, padx=10, pady=5)
    entry_pesquisa_editar = tk.Entry(janela_editar)
    entry_pesquisa_editar.grid(row=0, column=1, padx=10, pady=5)

    btn_pesquisar_editar = tk.Button(janela_editar, text="Pesquisar", command=lambda: pesquisar_livro_editar(entry_pesquisa_editar.get()))
    btn_pesquisar_editar.grid(row=0, column=2, padx=10, pady=5)

    # Função para pesquisar o livro a ser editado
    def pesquisar_livro_editar(termo_pesquisa):
        conn = sqlite3.connect('biblioteca.db')
        c = conn.cursor()
        c.execute('SELECT * FROM livros WHERE titulo LIKE ?', ('%' + termo_pesquisa + '%',))
        livros = c.fetchall()
        conn.close()

        if livros:
            # Mostrar os livros encontrados em uma lista
            lista_livros = tk.Listbox(janela_editar)
            lista_livros.grid(row=1, columnspan=3, padx=10, pady=5)

            for livro in livros:
                lista_livros.insert(tk.END, livro[1])

            # Botão para confirmar a edição do livro selecionado
            btn_confirmar_editar = tk.Button(janela_editar, text="Editar", command=lambda: abrir_janela_edicao(lista_livros.get(tk.ACTIVE)))
            btn_confirmar_editar.grid(row=2, columnspan=3, padx=10, pady=5)
        else:
            messagebox.showinfo("Livro não encontrado", "Nenhum livro correspondente foi encontrado.")

# Função para abrir a janela de edição do livro selecionado
    def abrir_janela_edicao(titulo_livro):
        janela_edicao = tk.Toplevel()
        janela_edicao.title("Editar Livro")

        # Recuperar os detalhes do livro selecionado para edição
        conn = sqlite3.connect('biblioteca.db')
        c = conn.cursor()
        c.execute('SELECT * FROM livros WHERE titulo=?', (titulo_livro,))
        livro = c.fetchone()
        conn.close()

        # Widgets para a edição dos dados do livro
        label_titulo = tk.Label(janela_edicao, text="Título:")
        label_titulo.grid(row=0, column=0, padx=10, pady=5)
        entry_titulo = tk.Entry(janela_edicao)
        entry_titulo.insert(0, livro[1])
        entry_titulo.grid(row=0, column=1, padx=10, pady=5)

        label_ano = tk.Label(janela_edicao, text="Ano de Publicação:")
        label_ano.grid(row=1, column=0, padx=10, pady=5)
        entry_ano = tk.Entry(janela_edicao)
        entry_ano.insert(0, livro[2])
        entry_ano.grid(row=1, column=1, padx=10, pady=5)

        # Botão para confirmar a edição do livro
        btn_confirmar_edicao = tk.Button(janela_edicao, text="Confirmar", command=lambda: confirmar_edicao(titulo_livro, entry_titulo.get(), entry_ano.get()))
        btn_confirmar_edicao.grid(row=2, columnspan=2, padx=10, pady=5)

    # Função para confirmar a edição do livro
        def confirmar_edicao(titulo_atual, novo_titulo, novo_ano):
            conn = sqlite3.connect('biblioteca.db')
            c = conn.cursor()
            c.execute('UPDATE livros SET titulo=?, ano_publicacao=? WHERE titulo=?', (novo_titulo, novo_ano, titulo_atual))
            conn.commit()
            conn.close()
            janela_edicao.destroy()
            filtrar_livros()


def filtrar_livros(event=None):
    termo_pesquisa = entry_pesquisa.get()
    # Limpar a lista de livros
    for row in tree.get_children():
        tree.delete(row)
    
    # Conectar ao banco de dados e pesquisar livros
    conn = sqlite3.connect('biblioteca.db')
    c = conn.cursor()
    c.execute('SELECT * FROM livros WHERE titulo LIKE ?', ('%' + termo_pesquisa + '%',))
    livros = c.fetchall()
    
    # Adicionar cada livro encontrado à lista
    for livro in livros:
        tree.insert('', 'end', values=livro)
    
    conn.close()

# Configuração da janela principal
root = tk.Tk()
root.title("Sistema de Bibliotecas Comunitárias")

# Botão "Administrativo"
btn_administrativo = tk.Button(root, text="Administrativo", command=fazer_login_administrativo)
btn_administrativo.grid(row=0, column=0, padx=10, pady=5)

# Barra de Pesquisa
label_pesquisa = tk.Label(root, text="Pesquisar:")
label_pesquisa.grid(row=0, column=1, padx=10, pady=5)
entry_pesquisa = tk.Entry(root)
entry_pesquisa.grid(row=0, column=2, padx=10, pady=5)
entry_pesquisa.bind("<KeyRelease>", filtrar_livros)

# Lista de Livros
tree = ttk.Treeview(root, columns=('ID', 'Título', 'Ano de Publicação', 'Disponibilidade', 'Data de Empréstimo', 'Data de Entrega'))
tree.heading('ID', text='ID')
tree.heading('Título', text='Título')
tree.heading('Ano de Publicação', text='Ano de Publicação')
tree.heading('Disponibilidade', text='Disponibilidade')
tree.heading('Data de Empréstimo', text='Data de Empréstimo')
tree.heading('Data de Entrega', text='Data de Entrega')
tree.grid(row=1, column=0, columnspan=6, padx=5, pady=10)

# Chamar a função filtrar_livros() para carregar os livros ao iniciar o aplicativo
filtrar_livros()

root.mainloop()



