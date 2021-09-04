import json
from book import Book

# Have to load books then make changes to it

# Loading books
def load_books():
    try:
        file = open('books.dat', 'r')
        books_dict = json.loads(file.read())
        books = []
        for book in books_dict:
            book_obj = Book(book['id'], book['name'], book['description'], book['isbn'], book['page_count'],
                            book['issued'], book['author'], book['year'])
            books.append(book_obj)
        return books
    except:
        return []

def save_books(books):
    json_books = []
    for book in books:
        json_books.append(book.to_dict())
    with open('books.dat', 'w') as file:
        file.write(json.dumps(json_books, indent=4))

def add_books(book):
    books = load_books()
    new_book = Book(book['id'], book['name'], book['description'], book['isbn'], book['page_count'],
                            book['issued'], book['author'], book['year'])
    save_books([*books, new_book])

