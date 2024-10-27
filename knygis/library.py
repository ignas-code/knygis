from books import Book
from user import Reader, Librarian
from datetime import datetime as dt
from datetime import timedelta
import random
import settings
import pandas as pd
import sqlite3
import random


class Library:
    def __init__(self):
        self.bookid = 0
        self.books = {}
        self.readers = {} # readers - key:lib_card, value: Reader object
        self.lib_card_num = 0
        self.librarian = Librarian(settings.librarian_username,settings.librarian_password)
        self.initialized_data = False
        self.db_file = 'knygis/data/library.db'

    def add_book(self,name,author,year,genre,quantity):
        if quantity > 0:
            new_book = Book(name,author,year,genre,quantity)
            for id, existing_book in self.books.items():
                if existing_book == new_book:
                    current_quantity = existing_book.quantity
                    new_quantity = current_quantity + quantity
                    existing_book.quantity = new_quantity
                    return
            
            self.books[self.bookid] = new_book
            self.bookid += 1

    def all_books(self):
        """
        Retrieves all book entries from the database.

        Returns:
            list of tuples
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT id,title,author,published_year,genre,isbn,total_copies FROM books''')
        result = cursor.fetchall()
        conn.close()
        column_names = ['id', 'Pavadinimas', 'Autorius', 'Leidimo metai', 'Žanras', 'ISBN', 'Vienetai']
        df = pd.DataFrame(result, columns=column_names)

        print(df)
        return df

    def all_readers(self):
        all_readers = []
        for value in self.readers.values():
            all_readers.append(f'{value.lib_card}, {value.username}')
            print(value.lib_card, value.username)
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
    
    def borrow_late_book(self,book_id,lib_card):
        "Dev use only. Changes the borrowing date to -15 days"
        current_date = dt.now().date()
        current_date = current_date - timedelta(days=15)
        current_date = current_date.strftime("%Y-%m-%d")
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
        random_num = random.randint(100,999)
        lib_card = f'BIB{random_num}{self.lib_card_num:04}'
        books_borrowed = {} # dictionary where key is book ID, and value is borrowing date
        reader = Reader(username,lib_card,books_borrowed)
        self.readers[lib_card] = reader
        return lib_card
    
    def find_books_by_name(self,book_name):
        found_books = []
        found_books_dict = {}
        for book_id in self.books:
            name = self.books[book_id].name
            if book_name.lower() in name.lower():
                found_books.append(self.books[book_id])
                found_books_dict[book_id] = self.books[book_id]
        
        if found_books:
            for book in found_books:
                print(book)
        else:
            print(f'Knygų su pavadinimu "{book_name}" nerasta')
            return f'Knygų su pavadinimu "{book_name}" nerasta'
        return found_books_dict

    def find_books_by_author(self,book_author):
        found_books = []
        found_books_dict = {}
        for book_id in self.books:
            author = self.books[book_id].author
            if book_author.lower() in author.lower():
                found_books.append(self.books[book_id])
                found_books_dict[book_id] = self.books[book_id]
        
        if found_books:
            for book in found_books:
                print(book)
        else:
            print(f'Knygų su autoriumi "{book_author}" nerasta')
            return f'Knygų su autoriumi "{book_author}" nerasta'
        return found_books_dict
    
    def remove_book(self,bookid): #be careful, no safety checks at all
        try:
            removed_book = self.books.pop(bookid)
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
                                              # add self.deleted_books = {} and put "popped" books there in the future
        removed_books = []
        book_ids = list(self.books.keys()) # Cannot iterate over a dictionary, which changes its size
        for book_id in book_ids:
            book_year = self.books[book_id].year
            book_borrowed = self.books[book_id].borrowed_cur
            try:
                book_year = int(book_year)
            except:
                print("Klaida `rem_ob_1`")
                return False
            if book_year < criteria and book_borrowed == 0:
                removed_book = self.remove_book(book_id)
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
                    try:
                        late_book = self.books[overdue_book_id]
                    except:
                        late_book = Book("ištrinta","ištrinta","ištrinta","ištrinta","ištrinta")
                    late_reader = self.readers[lib_card].username
                    all_overdue.append(overdue_book_id)
                    late_readers.append(lib_card)
                    print(f'Skaitytojas: {late_reader}, knyga: {late_book}')
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

# methods migrated to sql
    def get_reader(self,first_name,last_name,reader_card_number):
        """
        Retrieves the ID of a registered reader from the database based on the provided details.

        Returns:
            int: The unique ID of the reader if found.
            bool: False if no reader is found matching the provided details.

        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT id FROM readers WHERE first_name = ? AND last_name = ? AND reader_card_number = ?''',(first_name,last_name,reader_card_number))
        result = cursor.fetchall()
        conn.close()
        if len(result) == 0:
            print("Reader not found")
            return False
        if len(result) == 1:
            print("Reader found")
            return result[0][0]
        if len(result) > 1:
            print('Error, duplicate users found. Please contact admin')
            return False

        return result

if __name__ == "__main__":
    # for testing purposes only
    lib = Library()
    for i in range(9):
        lib.add_book("Lustu karas","Chris Miller",2024,"publicistika",2)
    lib.add_book("Atominiai iprociai","Hanes Clear",2019,"dalykine",-1)
    lib.add_book("Atominiai iprociai","Hanes Clear",2019,"dalykine",10)
    lib.add_book("Fear no evil","Natan",1988,"zanras",2)
    lib._remove_book(4)
    lib.all_books()
    for i in range (3):
        lib.add_reader("Jonas Jonauskas")
    lib.add_reader("Tomas")
    lib.find_books_by_name("ato")
    lib.all_readers()
    reader1 = lib.readers["BIB00001"]
    reader1_borrowed = reader1.books_borrowed
    lib.borrow_book(1,"BIB00001")
    lib.borrow_book(2,"BIB00001")
    lib.get_all_overdue()
    print(lib.all_books())