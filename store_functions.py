import json
from book import Book


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
    except ValueError:
        return []


def save_books(books):
    json_books = []
    for book in books:
        json_books.append(book.to_dict())
    with open('books.dat', 'w') as file:
        file.write(json.dumps(json_books, indent=4))


def update_book(book):
    book = Book(book['id'], book['name'], book['description'], book['isbn'], book['page_count'],
                    book['issued'], book['author'], book['year'])
    books = load_books()
    if book is not None:
        books = list(filter(lambda bk: int(bk.id) == int(book.id), books))
        books.pop()
        books.append(book)
        save_books(books)


def add_books(book):
    """
    Load books to variable from file using load_books func.
    Create new book using Book class and put it as args to save books func.
    """
    books = load_books()
    new_book = Book(book['id'], book['name'], book['description'], book['isbn'], book['page_count'],
                            book['issued'], book['author'], book['year'])
    new_book.set_id(new_book.id, books)  # if id is the same use set_id to change id as unique.
    save_books([*books, new_book])


def get_issued_books():
    books = load_books()
    return list(filter(lambda book: book.issued is True, books))


def get_unissued_books():
    books = load_books()
    return list(filter(lambda book: book.issued is False, books))


def find_book(book_id):
    books = load_books()
    for book in books:
        if book.id == int(book_id):
            return book
    return None


def delete_book(id):
    books = load_books()
    books = list(filter(lambda bk: int(bk.id) != int(id), books))
    save_books(books)
