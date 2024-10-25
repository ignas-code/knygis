import sqlite3

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

if __name__ == "__main__":
    create_database(db_file)
    print(is_book_in_db("abc","d James",'2024','-','-',db_file))