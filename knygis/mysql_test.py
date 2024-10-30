import mysql.connector
from mysql.connector import Error

hostname = ""
database = ""
port = ""
username = ""
password = ""

def example():
    try:
        connection = mysql.connector.connect(host=hostname, database=database, user=username, password=password, port=port)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def create_database():
    conn = mysql.connector.connect(host=hostname, database=database, user=username, password=password, port=port)
    if conn.is_connected():
        cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            author VARCHAR(255),
            published_year INT,
            genre VARCHAR(100),
            isbn VARCHAR(20) UNIQUE,
            total_copies INT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_deleted BOOLEAN DEFAULT 0
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            reader_card_number VARCHAR(50) UNIQUE,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS librarians (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255),
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loans (
            id INT AUTO_INCREMENT PRIMARY KEY,
            book_id INT,
            reader_id INT,
            loan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            return_date TIMESTAMP,
            FOREIGN KEY (reader_id) REFERENCES readers(id) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
        );
    ''')
    conn.commit()
    conn.close()

def add_book(title,author,published_year,genre,isbn,total_copies):
    conn = mysql.connector.connect(host=hostname, database=database, user=username, password=password, port=port)
    if conn.is_connected():
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO books (title, author, published_year, genre, isbn, total_copies)
        VALUES (%s,%s,%s,%s,%s,%s);
                        ''',(title,author,published_year,genre,isbn,total_copies))
        conn.commit()
            
        conn.close()
        print('Book added successfully')



#create_database()
add_book("Chip War","Chris",'2024','Nonfiction','1234567890','5')