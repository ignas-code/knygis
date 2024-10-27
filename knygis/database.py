import sqlite3
import random

db_file = 'knygis/data/library.db'

def create_database(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255),
    author VARCHAR(255),
    published_year INTEGER,
    genre VARCHAR(100),
    isbn VARCHAR(20) UNIQUE,
    total_copies INTEGER,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT 0
    );
                   ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS readers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reader_card_number VARCHAR(50) UNIQUE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
                   ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS librarians (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255),
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
                   ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    reader_id INTEGER,
    loan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    return_date TIMESTAMP,
    FOREIGN KEY (reader_id) REFERENCES readers (id),
    FOREIGN KEY (book_id) REFERENCES books (id)
    );
                ''')
    conn.commit()
    conn.close()

def is_book_in_db(title,author,published_year,genre,isbn,db_file): # does not check for total copies
    """
    Selects a book entry by its attributes (excluding total_copies) and returns the book_id if it exists.
    Returns:
        tuple: A tuple containing the book_id of the matching entry if found, otherwise None.
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id from books 
    WHERE title = ? AND author = ? AND published_year = ? AND genre =? AND isbn = ?
                    ''',(title,author,published_year,genre,isbn))
    result = cursor.fetchone()
    conn.close()

    return result

def increase_book_total_copies(book_id,copies_to_add,db_file):
    """
    Increases the `total_copies` of a book in the database.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    conn = sqlite3.connect(db_file)
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

def add_book_to_db(title,author,published_year,genre,isbn,total_copies, db_file): # no safety checks
    book_already_exists = is_book_in_db(title,author,published_year,genre,isbn,db_file)
    if book_already_exists is None:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO books (title, author, published_year, genre, isbn, total_copies)
            VALUES (?,?,?,?,?,?);
                            ''',(title,author,published_year,genre,isbn,total_copies))
            conn.commit()

        except:
            print('ISBN not unique')
            
        conn.close()

    else:
        book_id = book_already_exists[0]
        result = increase_book_total_copies(book_id,total_copies,db_file)
        if result == True:
            print(f"Such book (ID: {book_id}') already exists, increased `total_copies` number by {total_copies}")
        else:
            print(f'Unable to increase `total_copies` number for book (ID: {book_id})')

def all_books():
    """
    Retrieves all book entries from the database.

    Returns:
        list of tuples
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM books''')
    result = cursor.fetchall()
    conn.close()
    return result

def add_reader(first_name,last_name): # (id, reader_card_number, first_name, last_name)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO readers (first_name, last_name)
    VALUES (?,?);
                    ''',(first_name, last_name))
    reader_id = cursor.lastrowid
    lib_card_num = reader_id
    random_num = random.randint(100,999)
    lib_card = f'LIB{random_num}{lib_card_num:04}'

    cursor.execute('''
    UPDATE readers 
    SET reader_card_number = ?
    WHERE id = ?;
                    ''',(lib_card,reader_id))
    conn.commit()
    conn.close()
    return lib_card

def all_readers():
    """
    Retrieves all readers from the database.

    Returns:
        list of tuples
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM readers''')
    result = cursor.fetchall()
    conn.close()
    return result

def get_reader_overdue(reader_id,db_file):
    """
    Returns overdue book ids (in a list) of a specific reader, otherwise returns none.
    Paramter `loan_period` sets the number of days before a book is considered overdue
    """
    loan_period = 14 #days
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''SELECT id FROM loans WHERE reader_id = ? AND return_date IS NULL AND DATE('now') > DATE(loan_date, '+' || ? || ' days');''',(reader_id,loan_period))
    overdue_book_ids = cursor.fetchall() # list of tuples containing book_id
    conn.close()
    if overdue_book_ids != None and len(overdue_book_ids) > 0:
         overdue_book_ids = [id[0] for id in overdue_book_ids] 
    else:
        return None
    return overdue_book_ids

def get_borrowed_count_by_reader(reader_id,db_file):
    """
    Retrieves a number of books currently borrowed by the reader.

    Returns:
        int
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''SELECT COUNT(*) FROM loans WHERE reader_id = ? AND return_date IS NULL''',(reader_id))
    result = cursor.fetchone()
    conn.close()
    return result[0]

def available_copies(book_id,db_file):
    """
    Returns:
    int or bool
        The number of available copies of the book if available,
        or False if no copies are available.

    """
    conn = sqlite3.connect(db_file)
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

def is_book_borrowed_by_reader(book_id,reader_id,db_file):
    """
    Returns:
        bool: True if the reader has the book currently borrowed, False otherwise.
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM loans WHERE book_id = ? AND reader_id = ? AND return_date IS NULL''',(book_id,reader_id))
    result = cursor.fetchall()
    conn.close()
    if len(result) > 0:
        return True
    else:
        return False

def borrow_book(book_id,reader_id,db_file):
    max_borrowed_books = 3
    reader_overdue_books = get_reader_overdue(reader_id,db_file)
    available_copies_result = available_copies(book_id,db_file)
    currently_borrowed = is_book_borrowed_by_reader(book_id,reader_id,db_file)
    borrowed_count = get_borrowed_count_by_reader(reader_id,db_file)
    if (
        reader_overdue_books is None 
        and available_copies_result > 0 
        and currently_borrowed == False 
        and borrowed_count < max_borrowed_books
        ):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO loans (book_id, reader_id)
        VALUES (?,?);
                        ''',(book_id, reader_id))
        conn.commit()
        conn.close()
        return True
    else:
        if reader_overdue_books:
            print("Cannot borrow book: Reader has overdue books")
        if available_copies_result == False:
            print("Cannot borrow book: No available copies")
        if currently_borrowed:
            print("Cannot borrow book: Reader already has this book borrowed")
        if borrowed_count >= max_borrowed_books:
            print(f"Cannot borrow book: Reader already has maximum number of books ({max_borrowed_books}) borrowed")
        return False

def return_book(book_id,reader_id,db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''UPDATE loans SET return_date = CURRENT_TIMESTAMP WHERE book_id = ? AND reader_id = ? AND return_date IS NULL''',(book_id,reader_id))
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    if len(result) < 1:
        print("No such unreturned book found")
        return False
    if len(result) == 1:
        print("Book returned succesfully")
        return True
    if len(result) > 1:
        print("More than one copy of this book was borrowed, books returned succesfully")
    print(result)
    return result

def get_reader(first_name,last_name,reader_card_number,db_file):
    """
    Docstring.

    Returns:
        list of tuples
    """
    conn = sqlite3.connect(db_file)
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
    create_database(db_file)
    add_book_to_db("Chip War","Chris Miller",'2024','Nonfiction','3322111982172002','12',db_file)
    add_book_to_db('Think Python','Allen B. Downey','2015','Nonfiction','1491939362',4,db_file)
    print(is_book_in_db("abc","d James",'2024','-','-',db_file))
    print(is_book_in_db("Chip War","Chris Miller",'2024','Nonfiction','3322111982172002',db_file))
    print(increase_book_total_copies(1,1,db_file))
    print(all_books())
    print(add_reader('Skaitmantas','Knyginis'))
    print(all_readers())
    print(get_reader_overdue('8',db_file))
    borrow_book(3,1,db_file)
    #print(available_copies('2',db_file))
    print(is_book_borrowed_by_reader('1','2',db_file))
    print(get_borrowed_count_by_reader('4',db_file))
    return_book('4','4',db_file)
    print(get_borrowed_count_by_reader('4',db_file))
    print(get_reader('Skaitmantas','Knyginis','LIB8080001',db_file))
    print(get_reader('Raidvardas','Puslapiauskas','LIB5410004',db_file))