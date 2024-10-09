from books import Book

class Library:
    def __init__(self):
        self.bookid = 0
        self.books = {}

    def add_book(self,name,author,year,genre,quantity):
        book = Book(name,author,year,genre,quantity)
        existing_books = self.books
        for id, existing_book in existing_books.items():
            if existing_book == book:
                current_quantity = existing_book.get_quantity()
                new_quantity = current_quantity + quantity
                existing_book.update_quantity(new_quantity)
#               print("book already exists")
                return
        
        self.books[self.bookid] = book # dict[key] = value
        self.bookid += 1

    def all_books(self):
        for id, object in self.books.items():
            print(f'ID: {id}, Book: {object}')

if __name__ == "__main__":
    lib = Library()
    for i in range(3):
        lib.add_book("Svetimas","Alberas Kamiu",1942,"romanas",12)
    for i in range(3):
        lib.add_book("Lustu karas","Chris Miller",2024,"publicistika",5)
    lib.all_books()