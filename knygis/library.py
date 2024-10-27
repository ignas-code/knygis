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

    # def add_book(self,name,author,year,genre,quantity):
    #     if quantity > 0:
    #         new_book = Book(name,author,year,genre,quantity)
    #         for id, existing_book in self.books.items():
    #             if existing_book == new_book:
    #                 current_quantity = existing_book.quantity
    #                 new_quantity = current_quantity + quantity
    #                 existing_book.quantity = new_quantity
    #                 return
            
    #         self.books[self.bookid] = new_book
    #         self.bookid += 1
    def is_book_in_db(self,title,author,published_year,genre,isbn): # does not check for total copies
        """
        Selects a book entry by its attributes (excluding total_copies) and returns the book_id if it exists.
        Returns:
            tuple: A tuple containing the book_id of the matching entry if found, otherwise None.
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT id from books 
        WHERE title = ? AND author = ? AND published_year = ? AND genre =? AND isbn = ? AND is_deleted IS 0
                        ''',(title,author,published_year,genre,isbn))
        result = cursor.fetchone()
        conn.close()

        return result

    def increase_book_total_copies(self,book_id,copies_to_add):
        """
        Increases the `total_copies` of a book in the database.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE books 
        SET total_copies = total_copies + ?
        WHERE id = ?;
                        ''',(copies_to_add,book_id))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    def add_book(self,title,author,published_year,genre,isbn,total_copies):
        book_already_exists = self.is_book_in_db(title,author,published_year,genre,isbn)
        if book_already_exists is None:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            try:
                cursor.execute('''
                INSERT INTO books (title, author, published_year, genre, isbn, total_copies)
                VALUES (?,?,?,?,?,?);
                                ''',(title,author,published_year,genre,isbn,total_copies))
                conn.commit()

            except sqlite3.IntegrityError:
                 return ('ISBN not unique')
            except:
                return
                
            conn.close()
            return 'Book added successfully'

        else:
            book_id = book_already_exists[0]
            result = self.increase_book_total_copies(book_id,total_copies)
            if result == True:
                print(f"Such book (ID: {book_id}') already exists, increased `total_copies` number by {total_copies}")
                return 'Book already exists. Added additional copies.'
            else:
                print(f'Unable to increase `total_copies` number for book (ID: {book_id})')
                return 'Book already exists. Adding additioanl copies failed.'

    def all_books(self):
        """
        Retrieves all book entries from the database.

        Returns:
            list of tuples
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT id,title,author,published_year,genre,isbn,total_copies FROM books WHERE is_deleted IS 0''')
        result = cursor.fetchall()
        conn.close()
        column_names = ['id', 'Pavadinimas', 'Autorius', 'Leidimo metai', 'Žanras', 'ISBN', 'Vienetai']
        df = pd.DataFrame(result, columns=column_names)

        print(df)
        return df

    def all_readers(self):
        """
        Retrieves all readers from the database.

        Returns:
            list of tuples
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM readers''')
        result = cursor.fetchall()
        conn.close()
        return result

    def available_copies(self,book_id):
        """
        Returns:
        int or bool
            The number of available copies of the book if available,
            or False if no copies are available.

        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT total_copies FROM books WHERE id = ?''',(book_id))
        total_copies = cursor.fetchone()
        cursor.execute('''SELECT COUNT(*) FROM loans WHERE book_id = ? AND return_date IS NULL''',(book_id))
        loaned_copies = cursor.fetchone()
        conn.close()
        if total_copies != None and loaned_copies is not None:
            available_copies = total_copies[0] - loaned_copies[0]
            return available_copies
        return None

    def is_book_borrowed_by_reader(self,book_id,reader_id):
        """
        Returns:
            bool: True if the reader has the book currently borrowed, False otherwise.
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM loans WHERE book_id = ? AND reader_id = ? AND return_date IS NULL''',(book_id,reader_id))
        result = cursor.fetchall()
        conn.close()
        if len(result) > 0:
            return True
        else:
            return False

    def get_borrowed_count_by_reader(self,reader_id):
        """
        Retrieves a number of books currently borrowed by the reader.

        Returns:
            int
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT COUNT(*) FROM loans WHERE reader_id = ? AND return_date IS NULL''',(reader_id))
        result = cursor.fetchone()
        conn.close()
        return result[0]

    def borrow_book(self,book_id,reader_id):
        print('function sstart')
        max_borrowed_books = 3
        reader_overdue_books = self.get_reader_overdue(reader_id)
        available_copies_result = self.available_copies(book_id)
        currently_borrowed = self.is_book_borrowed_by_reader(book_id,reader_id)
        borrowed_count = self.get_borrowed_count_by_reader(reader_id)
        if (
            reader_overdue_books is None 
            and available_copies_result > 0 
            and currently_borrowed == False 
            and borrowed_count < max_borrowed_books
            ):
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO loans (book_id, reader_id)
            VALUES (?,?);
                            ''',(book_id, reader_id))
            conn.commit()
            conn.close()
            return True
        else: # possible improvement here could be using if clauses and returning all applicable error messages
            if reader_overdue_books:
                print("Cannot borrow book: Reader has overdue books")
                return "Reader has overdue books"
            elif currently_borrowed:
                print("Cannot borrow book: Reader already has this book borrowed")
                return "Reader already has this book borrowed"
            elif borrowed_count >= max_borrowed_books:
                print(f"Cannot borrow book: Reader already has maximum number of books ({max_borrowed_books}) borrowed")
                return "Reader already has maximum number of books borrowed"
            elif available_copies_result == False:
                print("Cannot borrow book: No available copies")
                return "No available copies"
            return False

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
        
    def return_book(self,book_id,reader_id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''UPDATE loans SET return_date = CURRENT_TIMESTAMP WHERE book_id = ? AND reader_id = ? AND return_date IS NULL''',(book_id,reader_id))
        conn.commit()
        result = cursor.rowcount
        conn.close()
        if result < 1:
            print("No such unreturned book found")
            return "No such unreturned book found"
        if result == 1:
            print("Book returned succesfully")
            return True
        if result > 1:
            print("More than one copy of this book was borrowed, books returned succesfully")
            print(result)
            return result

    def add_reader(self,first_name,last_name): # (id, reader_card_number, first_name, last_name)
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO readers (first_name, last_name)
        VALUES (?,?);
                        ''',(first_name, last_name))
        reader_id = cursor.lastrowid
        lib_card_num = reader_id
        random_num = random.randint(100,999)
        reader_card_number = f'LIB{random_num}{lib_card_num:04}'

        cursor.execute('''
        UPDATE readers 
        SET reader_card_number = ?
        WHERE id = ?;
                        ''',(reader_card_number,reader_id))
        conn.commit()
        conn.close()
        return reader_card_number
    
    def find_books_by_name(self,book_name):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT id,title,author,published_year,genre,isbn,total_copies FROM books WHERE title LIKE '%' || ? || '%' AND is_deleted IS 0''',(book_name,))
        result = cursor.fetchall()
        conn.close()

        return result


    def find_books_by_author(self,book_author):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT id,title,author,published_year,genre,isbn,total_copies FROM books WHERE author LIKE '%' || ? || '%' AND is_deleted IS 0''',(book_author,))
        result = cursor.fetchall()
        conn.close()

        return result
    
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
        
    def get_reader_overdue(self,reader_id):
        """
        Returns overdue book ids (in a list) of a specific reader, otherwise returns none.
        Paramter `loan_period` sets the number of days before a book is considered overdue
        """
        loan_period = 14 #days
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT book_id FROM loans WHERE reader_id = ? AND return_date IS NULL AND DATE('now') > DATE(loan_date, '+' || ? || ' days');''',(reader_id,loan_period))
        overdue_book_ids = cursor.fetchall() # list of tuples containing book_id
        conn.close()
        if overdue_book_ids != None and len(overdue_book_ids) > 0:
            overdue_book_ids = [id[0] for id in overdue_book_ids] 
        else:
            return None
        return overdue_book_ids  
    
    def get_all_overdue(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
                        SELECT books.title, books.author, books.isbn, readers.first_name, readers.last_name, readers.reader_card_number, loans.loan_date
                        FROM loans 
                        JOIN readers ON loans.reader_id = readers.id
                        JOIN books ON loans.book_id = books.id
                        WHERE loans.return_date IS NULL
                        AND DATE('now') > DATE(loan_date, '+' || 14 || ' days');
                       ''')
        overdue_books = cursor.fetchall()
        conn.close()
        return overdue_books
    
    def get_borrowed_by_user(self,reader_id):
        """
        Retrieves all books (title and author) currently and previously borrowed by the reader. Used for borrowed books page.
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT 
                            loans.book_id,
                            loans.loan_date,
                            books.title,
                            books.author,
                            books.published_year,
                            books.genre,
                            books.isbn 
                        FROM 
                            loans 
                        INNER JOIN 
                            books 
                        ON 
                            loans.book_id = books.id 
                        WHERE 
                            loans.reader_id = ?
                        AND
                            return_date IS NULL
                       ''',(reader_id))
        current_books = cursor.fetchall()
        cursor.execute('''SELECT 
                            loans.book_id,
                            loans.loan_date,
                            loans.return_date,
                            books.title,
                            books.author,
                            books.published_year,
                            books.genre,
                            books.isbn 
                        FROM 
                            loans 
                        INNER JOIN 
                            books 
                        ON 
                            loans.book_id = books.id 
                        WHERE 
                            loans.reader_id = ?
                        AND
                            return_date IS NOT NULL
                       ''',(reader_id))
        previous_books = cursor.fetchall()
        conn.close()
        return current_books, previous_books

    def get_currently_borrowed_by_user(self,reader_id):
        """
        Retrieves all books (title and author) currently borrowed by the reader. Used for book return selector.

        Returns:
            list of tuples
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT book_id FROM loans WHERE reader_id = ? AND return_date IS NULL''',(reader_id))
        book_ids = cursor.fetchall()
        book_titles_authors = []
        for book_id in book_ids:
            cursor.execute('''SELECT id, title, author FROM books WHERE id = ?''',(str(book_id[0])))
            result = cursor.fetchone()
            book_titles_authors.append(result)
        conn.close()
        return book_titles_authors

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

    def get_title_author(self,book_id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''SELECT title FROM books WHERE id = ?''',(book_id))
        title = cursor.fetchone()
        cursor.execute('''SELECT author FROM books WHERE id = ?''',(book_id))
        author = cursor.fetchone()
        conn.close()
        if title is not None and author is not None:
            return title[0],author[0]
        else:
            return False,False

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