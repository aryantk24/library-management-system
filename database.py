import sqlite3

class Database:
    def __init__(self, db_name='library.db'):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)

    def initialize_tables(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            # Create books table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    isbn TEXT NOT NULL UNIQUE,
                    available INTEGER DEFAULT 1,
                    borrowed_by TEXT
                )
            ''')
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                )
            ''')
            conn.commit()

    def add_book(self, title, author, isbn):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO books (title, author, isbn)
                VALUES (?, ?, ?)
            ''', (title, author, isbn))
            conn.commit()

    def get_all_books(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM books')
            return cursor.fetchall()

    def delete_book(self, book_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
            conn.commit()

    def search_books(self, query):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM books
                WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
            ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
            return cursor.fetchall()

    def borrow_book(self, book_id, user_name):
        with self.connect() as conn:
            cursor = conn.cursor()
            # Check if the book is available
            cursor.execute('SELECT available FROM books WHERE id = ?', (book_id,))
            book = cursor.fetchone()
            if book and book[0] == 1:
                # Add user if not exists
                cursor.execute('INSERT OR IGNORE INTO users (name) VALUES (?)', (user_name,))
                # Update the book's availability and borrower
                cursor.execute('''
                    UPDATE books
                    SET available = 0, borrowed_by = ?
                    WHERE id = ?
                ''', (user_name, book_id))
                conn.commit()
                return True
            return False

    def return_book(self, book_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            # Check if the book is borrowed
            cursor.execute('SELECT available FROM books WHERE id = ?', (book_id,))
            book = cursor.fetchone()
            if book and book[0] == 0:
                # Update the book's availability and clear the borrower
                cursor.execute('''
                    UPDATE books
                    SET available = 1, borrowed_by = NULL
                    WHERE id = ?
                ''', (book_id,))
                conn.commit()
                return True
            return False
