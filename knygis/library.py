from books import Book
from user import Reader, Librarian
from datetime import datetime as dt

class Library:
    def __init__(self):
        self.bookid = 0
        self.books = {} # book class instances in a dictionary
        self.readers = {} # readers - key:lib_card, value: Reader object
        self.lib_card_num = 0
        self.librarian = Librarian("Bib","200")

    def add_book(self,name,author,year,genre,quantity):
        if quantity > 0: # cannot add 0 or negative of book
            new_book = Book(name,author,year,genre,quantity)
            existing_books = self.books
            for id, existing_book in existing_books.items():
                if existing_book == new_book:
                    current_quantity = existing_book.quantity
                    new_quantity = current_quantity + quantity
                    existing_book.quantity = new_quantity
    #               print("book already exists")
                    return
            
            self.books[self.bookid] = new_book # dict[key] = value
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

    def borrow_book(self,book_id,lib_card):
        current_date = dt.now().date().strftime("%Y-%m-%d")
        try:
            book = self.books[book_id]
        except:
            print("Knyga nerasta")
            return False
        try:
            reader = self.readers[lib_card]
        except:
            print("Skaitytojas nerastas")
            return False
        if book.quantity > book.borrowed_cur:
            if book_id not in reader.books_borrowed:
                reader.books_borrowed[book_id] = current_date
                book.borrowed_cur += 1
                # stores borrowed book_id as key and current date as value
                # append to user books borrowed as well
                print(f'Knyga {book.name} sėkmingai paimta ({current_date})')
                return True
            else:
                return False
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
    lib.add_book("Atominiai iprociai","Hanes Clear",2019,"dalykine",-1)
    lib.add_book("Atominiai iprociai","Hanes Clear",2019,"dalykine",10)
    lib.add_book("Fear no evil","Natan",1988,"zanras",1)
    lib._remove_book(1)
    # print(lib.borrow_book(2))
    # print(lib.borrow_book(2))

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
    
    print(lib.librarian.username)
    print(lib.librarian.password)
    lib.borrow_book(2,"BIB00002")
    lib.borrow_book(2,"BIB00002")
    lib.borrow_book(2,"BIB0002")
    lib.borrow_book(1,"BIB00002")

    for value in lib.readers.values():
        print(value.lib_card, value.username, value.books_borrowed) # value.books_borrowed

#    print(lib.readers)
