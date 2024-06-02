import requests
import pandas as pd

# Função para buscar livros por autor ou assunto
def search_books(subject):
    url = f'https://openlibrary.org/subjects/{subject}.json?limit=100'
    response = requests.get(url)
    data = response.json()
    books = data['works']
    return books

# Buscar livros sobre literatura brasileira
books = search_books('brazilian_literature')

# Extrair título e ano de publicação
book_list = []
for book in books:
    title = book['title']
    year = book.get('first_publish_year', 'Desconhecido')
    book_list.append({'Título': title, 'Ano de Publicação': year})

# Criar um DataFrame
df = pd.DataFrame(book_list)

# Exibir os primeiros registros
print(df.head())

# Salvar em um arquivo CSV
df.to_csv('livros_brasileiros.csv', index=False)

import requests
import pandas as pd

# Função para buscar livros por autor ou título
def search_books(query):
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=40'
    response = requests.get(url)
    data = response.json()
    books = data['items']
    return books

# Buscar livros sobre literatura brasileira
books = search_books('literatura brasileira')

# Extrair título e ano de publicação
book_list = []
for book in books:
    volume_info = book['volumeInfo']
    title = volume_info.get('title', 'Desconhecido')
    year = volume_info.get('publishedDate', 'Desconhecido')[:4]  # Pega apenas o ano
    book_list.append({'Título': title, 'Ano de Publicação': year})

# Criar um DataFrame
df2 = pd.DataFrame(book_list)

# Exibir os primeiros registros
print(df.head())

# Salvar em um arquivo CSV
df2.to_csv('livros_brasileiros_google_books.csv', index=False)


#df_c = df.merge(df2, how='inner', on=['Título', 'Ano de Publicação'])

df_c = pd.concat([df, df2], ignore_index=True)
df_c.to_csv('livros_brasileiros_completos.csv', index=False)

