from books import Book
from user import Reader, Librarian
from datetime import datetime as dt
import settings

class Library:
    def __init__(self):
        self.bookid = 0
        self.books = {} # book class instances in a dictionary
        self.readers = {} # readers - key:lib_card, value: Reader object
        self.lib_card_num = 0
        self.librarian = Librarian(settings.librarian_username,settings.librarian_password)

    def add_book(self,name,author,year,genre,quantity):
        if quantity > 0: # cannot add 0 or negative of book
            new_book = Book(name,author,year,genre,quantity)
            for id, existing_book in self.books.items():
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

    def all_readers(self):
        for value in self.readers.values():
            print(value.lib_card, value.username) # value.books_borrowed

    def borrow_book(self,book_id,lib_card):
        current_date = dt.now().date().strftime("%Y-%m-%d")
        return_date = 0
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
            try:
                borrowed_before = bool(reader.books_borrowed[book_id][1]) # check if book return date is present
            except (KeyError, IndexError):
                borrowed_before = False
            if book_id not in reader.books_borrowed or borrowed_before: # test if book was borrowed previously
                reader.books_borrowed[book_id] = [current_date, return_date] # if book is taken 2nd time, record will be rewritten
                book.borrowed_cur += 1
                # stores borrowed book_id as key and current date as value
                # append to user books borrowed as well
                print(f'Knyga "{book.name}" sėkmingai paimta ({current_date})')
                return True
            else:
                print("Knyga jau paimta")
                return False
        else:
            print("Nepakankamas likutis")
            return False
    
    def return_book(self,book_id,lib_card):
        return_date = dt.now().date().strftime("%Y-%m-%d")
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
        if book_id in reader.books_borrowed:
            reader.books_borrowed[book_id][1] = return_date # {bookd_id: [borrow_date, return_date]}
            book.borrowed_cur -= 1
            # stores borrowed book_id as key and current date as value
            # append to user books borrowed as well
            print(f'Knyga "{book.name}" sėkmingai grąžinta ({return_date})')
            return True
        else:
            print("Klaida")
            return False
        pass
        
        
    def add_reader(self,username):
        self.lib_card_num += 1 # increment the library card ID number
        lib_card = f'BIB{self.lib_card_num:05}'
        books_borrowed = {} # dictionary where key is book ID, and value is borrowing date
        reader = Reader(username,lib_card,books_borrowed)
        self.readers[lib_card] = reader
        return lib_card
    
    def find_books_by_name(self,book_name):
        found_books = []
        for book_id in self.books:
            name = self.books[book_id].name
            if book_name.lower() in name.lower():
                found_books.append(self.books[book_id])
        
        if found_books:
            for book in found_books:
                print(book)
        else:
            print(f'Knygų su pavadinimu "{book_name}" nerasta')
            return False
        return found_books

    def find_books_by_author(self,book_author):
        found_books = []
        for book_id in self.books:
            author = self.books[book_id].author
            if book_author.lower() in author.lower():
                found_books.append(self.books[book_id])
        
        if found_books:
            for book in found_books:
                print(book)
        else:
            print(f'Knygų su autoriumi "{book_author}" nerasta')
            return False
        return found_books


if __name__ == "__main__":
    lib = Library()
    # for i in range(3):
    #     lib.add_book("Svetimas","Alberas Kamiu",1942,"romanas",12)
    for i in range(9):
        lib.add_book("Lustu karas","Chris Miller",2024,"publicistika",2)
    lib.add_book("Atominiai iprociai","Hanes Clear",2019,"dalykine",-1)
    lib.add_book("Atominiai iprociai","Hanes Clear",2019,"dalykine",10)
    lib.add_book("Fear no evil","Natan",1988,"zanras",2)
    lib._remove_book(4)
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
    
    # print(lib.librarian.username)
    # print(lib.librarian.password)
    lib.borrow_book(2,"BIB00002")
    lib.borrow_book(2,"BIB00002")
    lib.borrow_book(2,"BIB0002")
    lib.borrow_book(1,"BIB00002")
    lib.borrow_book(0,"BIB00001")
    lib.borrow_book(1,"BIB00001")
    lib.borrow_book(2,"BIB00001")
    lib.return_book(2,"BIB00001")
    



#     for value in lib.readers.values():
#         print(value.lib_card, value.username, value.books_borrowed) # value.books_borrowed

#     a = lib.readers['BIB00001'].books_borrowed[2][1]
#     print(a)
#     print(bool(a))
#     print(lib.readers)
    print("nuo cia")
            # whole_str = self.books[book_id]
            # name = self.books[book_id].name
            # author = self.books[book_id].author
            # genre = self.books[book_id].genre
    lib.find_books_by_name(1)
