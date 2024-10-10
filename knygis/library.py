from books import Book
from user import Reader, Librarian
from datetime import datetime as dt

class Library:
    def __init__(self):
        self.bookid = 0
        self.books = {} # book class instances in a dictionary
        self.readers = {} # readers - key:lib_card, value: Reader object
        self.lib_card_num = 0
        self.librarian = Librarian("Bibliotekininkas","Skaitau2000")

    def add_book(self,name,author,year,genre,quantity):
        book = Book(name,author,year,genre,quantity)
        existing_books = self.books
        for id, existing_book in existing_books.items():
            if existing_book == book:
                current_quantity = existing_book.quantity
                new_quantity = current_quantity + quantity
                existing_book.quantity = new_quantity
#               print("book already exists")
                return
        
        self.books[self.bookid] = book # dict[key] = value
        self.bookid += 1

    def _remove_book(self,bookid): #be careful, no safety checks at all
        try:
            removed_book = self.books.pop(bookid)
            print(f'Knyga "{removed_book}" pašalinta')
        except KeyError:
            print(f'Knyga su id {bookid} nerasta')

    def all_books(self):
        for id, object in self.books.items():
            print(f'ID: {id}, Knyga: {object}')

    def borrow_book(self,book_id):
        #current_date = dt.now().date() 
        # append to user books borrowed as well
        book = self.books[book_id]
        if book.quantity > book.borrowed_cur:
            book.borrowed_cur += 1
            return True
        else:
            return False
        
    def add_reader(self,username):
        self.lib_card_num += 1 # increment the library card ID number
        lib_card = f'BIB{self.lib_card_num:05}'
        books_borrowed = {} # dictionary where key is book ID, and value is borrowing date
        reader = Reader(username,lib_card,books_borrowed)
        self.readers[lib_card] = reader
        return lib_card



if __name__ == "__main__":
    lib = Library()
    # for i in range(3):
    #     lib.add_book("Svetimas","Alberas Kamiu",1942,"romanas",12)
    for i in range(9):
        lib.add_book("Lustu karas","Chris Miller",2024,"publicistika",1)
    lib.add_book("Atominiai iprociai","Hanes Clear",2019,"dalykine",1)
    lib.add_book("Atominiai iprociai","Hanes Clear",2019,"dalykine",10)
    lib.add_book("Fear no evil","Natan",1988,"zanras",1)
    lib._remove_book(1)
    print(lib.borrow_book(2))
    print(lib.borrow_book(2))

    # for i in range(2):
    #     name = f'pavadinimas {i}'
    #     lib.add_book(name,"autorius","metai ","zanras","kiekis ")
    # lib.all_books()
    # lib.remove_book(25)
    # lib.remove_book(3)
    lib.all_books()
    for i in range (3):
        lib.add_reader("Jonas Jonauskas")
    lib.add_reader("Tomas")
    for value in lib.readers.values():
        print(value.lib_card, value.username) # value.books_borrowed
    print(lib.librarian.username)
    print(lib.librarian.password)
