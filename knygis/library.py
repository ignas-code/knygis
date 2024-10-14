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

    def all_books(self):
        books = []
        for id, object in self.books.items():
            books.append(f'ID: {id}, Knyga: {object}')
            print(f'ID: {id}, Knyga: {object}')
        return books

    def all_readers(self):
        all_readers = []
        for value in self.readers.values():
            all_readers.append(f'{value.lib_card}, {value.username}')
            print(value.lib_card, value.username) # value.books_borrowed
        return all_readers

    def borrow_book(self,book_id,lib_card):
        current_date = dt.now().date().strftime("%Y-%m-%d")
        return_date = 0
        try:
            book = self.books[book_id]
        except:
            print("Knyga nerasta")
            return "Knyga nerasta"
        try:
            reader = self.readers[lib_card]
        except:
            print("Skaitytojas nerastas")
            return "Skaitytojas nerastas"
        users_overdue_books = self.get_reader_overdue(lib_card)
        if users_overdue_books:
            print("Turite knygų negražintų laiku: ")
            for book_id in users_overdue_books:
                print(self.books[book_id].name,self.books[book_id].author)
            print("Pirmiausia grąžinkite vėluojančias knygas!")
            return "Pirmiausia grąžinkite vėluojančias knygas!"
        if book.quantity > book.borrowed_cur:
            try:
                borrowed_before = bool(reader.books_borrowed[book_id][1]) # check if book return date is present
            except (KeyError, IndexError):
                borrowed_before = False
            if book_id not in reader.books_borrowed or borrowed_before: # test if book was borrowed previously
                reader.books_borrowed[book_id] = [current_date, return_date] # if book is taken 2nd time, record will be rewritten
                book.borrowed_cur += 1
                print(f'Knyga "{book.name}" sėkmingai paimta ({current_date})')
                return f'Knyga "{book.name}" sėkmingai paimta ({current_date})'
            else:
                print("Knyga jau paimta")
                return "Knyga jau paimta"
        else:
            print("Nepakankamas likutis")
            return "Nepakankamas likutis"
    
    def return_book(self,book_id,lib_card):
        return_date = dt.now().date().strftime("%Y-%m-%d")
        try:
            book = self.books[book_id]
        except:
            print("Knyga nerasta")
            return "Knyga nerasta"
        try:
            reader = self.readers[lib_card]
        except:
            print("Skaitytojas nerastas")
            return "Skaitytojas nerastas"
        if book_id in reader.books_borrowed:
            reader.books_borrowed[book_id][1] = return_date # {bookd_id: [borrow_date, return_date]}
            book.borrowed_cur -= 1
            print(f'Knyga "{book.name}" sėkmingai grąžinta ({return_date})')
            return f'Knyga "{book.name}" sėkmingai grąžinta ({return_date})'
        else:
            print(f"Tokios knygos skaitytojas {reader.username} nebuvo paėmęs")
            return f"Tokios knygos skaitytojas **'{reader.username}'** nebuvo paėmęs"
        
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
            return [f'Knygų su pavadinimu "{book_name}" nerasta']
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
            return [f'Knygų su autoriumi "{book_author}" nerasta']
        return found_books
    
    def _remove_book(self,bookid): #be careful, no safety checks at all
        try:
            removed_book = self.books.pop(bookid)
            #print(f'Knyga "{removed_book}" pašalinta')
            return removed_book
        except KeyError:
            print(f'Knyga su id {bookid} nerasta')

    def view_obsolete_books(self,criteria):
        obsolete_books = []
        for book_id in self.books:
            book_year = self.books[book_id].year
            try:
                book_year = int(book_year) # make sure the input year is of int type
            except:
                print("Klaida `view_ob_1`")
                return False
            if book_year < criteria:
                obsolete_books.append(self.books[book_id])
        if obsolete_books:
            if len(obsolete_books) == 1:
                message = "Rasta knyga: "
            else:
                message = "Visos rastos knygos: "
            print(message)
            for book in obsolete_books:
                print(book)
            return obsolete_books
        else:
            print(f"Knygų, kurių leidimo data senesnė nei nurodyta ({criteria}m.) nerasta")
            return False

    def remove_obsolete_books(self,criteria): # does not delete book records from readers who have that book taken
                                              # add self.deleted_books = {} and put "popped" books there 
        removed_books = []
        book_ids = list(self.books.keys()) # Cannot iterate over a dictionary, which changes its size otherwise
        for book_id in book_ids:
            book_year = self.books[book_id].year
            try:
                book_year = int(book_year) # make sure the input year is of int type
            except:
                print("Klaida `rem_ob_1`")
                return False
            if book_year < criteria:
                removed_book = self._remove_book(book_id)
                removed_books.append(removed_book)
        if removed_books:
            if len(removed_books) == 1:
                message = "Pašalinta knyga: "
            else:
                message = "Visos pašalintos knygos: "
            print(message)
            for book in removed_books:
                print(book)
            return removed_books
        else:
            print("Nėra pašalintų knygų")
            return False
        
    def get_reader_overdue(self,lib_card):
        "Returns overdue book ids of a specific reader"
        reader = self.readers[lib_card]
        overdue_book_ids = reader.get_overdue()
        return overdue_book_ids
    
    def get_all_overdue(self):
        all_overdue = []
        late_readers = []
        for lib_card in self.readers:
            overdue_book_id_list = self.get_reader_overdue(lib_card)
            if overdue_book_id_list != False:
                for overdue_book_id in overdue_book_id_list:
                    late_book = self.books[overdue_book_id]
                    late_reader = self.readers[lib_card].username
                    all_overdue.append(overdue_book_id)
                    late_readers.append(lib_card)
                    print(f'Skaitytojas: {late_reader}, knyga: {late_book}')
        # for book_id in all_overdue:
        #     print()
        # for lib_card in late_readers:
        #     print(lib_card, )
        return all_overdue, late_readers
    
    def get_borrowed_by_user(self,lib_card):
        borrowed_list = []
        reader = self.readers[lib_card]
        borrowed_books = reader.view_borrowed()
        for book_id, dates in borrowed_books.items():
            borrow_date = dates[0]
            return_date = dates[1]
            if return_date == 0:
                return_date = "-"
            book_name = self.books[book_id].name
            book_author = self.books[book_id].author
            borrowed_list.append(f'ID: {book_id} Knyga: **{book_name}**, autorius: **{book_author}**, paimta: **{borrow_date}**, grąžinta: **{return_date}**')
        return borrowed_list
    
    def get_currently_borrowed_by_user(self,lib_card):
        borrowed_dict = {}
        reader = self.readers[lib_card]
        borrowed_books = reader.view_borrowed()
        for book_id, dates in borrowed_books.items():
            borrow_date = dates[0]
            return_date = dates[1]
            if return_date == 0:
                book_name = self.books[book_id].name
                book_author = self.books[book_id].author
                borrowed_dict[book_id] = f'ID: {book_id} Knyga: {book_name}, autorius: {book_author}, paimta: {borrow_date}'
            
        return borrowed_dict

        

           


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
    # lib.borrow_book(2,"BIB00002")
    # lib.borrow_book(2,"BIB00002")
    # lib.borrow_book(2,"BIB0002")
    # lib.borrow_book(1,"BIB00002")
    # lib.borrow_book(0,"BIB00001")
    # lib.borrow_book(1,"BIB00001")
    # lib.borrow_book(2,"BIB00001")
    # lib.return_book(2,"BIB00001")
    



#     for value in lib.readers.values():
#         print(value.lib_card, value.username, value.books_borrowed) # value.books_borrowed

#     a = lib.readers['BIB00001'].books_borrowed[2][1]
#     print(a)
#     print(bool(a))
#     print(lib.readers)
            # whole_str = self.books[book_id]
            # name = self.books[book_id].name
            # author = self.books[book_id].author
            # genre = self.books[book_id].genre
    lib.find_books_by_name("ato")
    lib.all_readers()
    reader1 = lib.readers["BIB00001"]
    reader1_borrowed = reader1.books_borrowed
    # print(reader1_borrowed)
    # for book in reader1_borrowed:
    #         print(reader1_borrowed[book][0],reader1_borrowed[book][1])
    # print(reader1.get_overdue())
    # print(lib.get_reader_overdue("BIB00001"))
    lib.borrow_book(1,"BIB00001")
    lib.borrow_book(2,"BIB00001")


    lib.get_all_overdue()
    print(lib.all_books())