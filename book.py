class Book:
    """Create book object with attributes"""
    def __init__(self, id, name, description, isbn, page_count, issued, author, year):
        self.year = year
        self.author = author
        self.issued = issued
        self.page_count = page_count
        self.isbn = isbn
        self.description = description
        self.name = name
        self.id = id

    def to_dict(self):
        """Attributes of object copy to dictionary"""
        dictionary = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'isbn': self.isbn,
            'page_count': self.page_count,
            'issued': self.issued,
            'author': self.author,
            'year': self.year
        }
        return dictionary