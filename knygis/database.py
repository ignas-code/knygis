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