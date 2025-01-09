import sqlite3
from datetime import datetime, timedelta

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
                    borrowed_by TEXT,
                    due_date TEXT
                )
            ''')
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            ''')
            conn.commit()

    def register_user(self, name, password):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (name, password) VALUES (?, ?)', (name, password))
            conn.commit()

    def send_notification(self, book_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            book = cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
        if book:
            return f"Notification sent to {book[5]} about overdue book: {book[1]}"
        return "Book not found."
        

    def generate_issue_alert(self, book_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            book = cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
            if book:
                return f"Issue generated for {book[5]} regarding overdue book: {book[1]}"
        return "Book not found."

    def authenticate_user(self, name, password):
        with self.connect() as conn:
            cursor = conn.cursor()
            user = cursor.execute('SELECT * FROM users WHERE name = ? AND password = ?', (name, password)).fetchone()
            return user

    def borrow_book(self, book_id, user_name):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT available FROM books WHERE id = ?', (book_id,))
            book = cursor.fetchone()
            if book and book[0] == 1:
                due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
                cursor.execute('''
                    UPDATE books
                    SET available = 0, borrowed_by = ?, due_date = ?
                    WHERE id = ?
                ''', (user_name, due_date, book_id))
                conn.commit()
                return True
            return False

    def return_book(self, book_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT available FROM books WHERE id = ?', (book_id,))
            book = cursor.fetchone()
            if book and book[0] == 0:
                cursor.execute('''
                    UPDATE books
                    SET available = 1, borrowed_by = NULL, due_date = NULL
                    WHERE id = ?
                ''', (book_id,))
                conn.commit()
                return True
            return False
        


    def get_all_users(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            users = cursor.execute('SELECT * FROM users').fetchall()
            result = []
            for user in users:
                borrowed_books = cursor.execute('SELECT * FROM books WHERE borrowed_by = ?', (user[1],)).fetchall()
                result.append({'id': user[0], 'name': user[1], 'borrowed_books': borrowed_books})
            return result
  

    def add_book(self, title, author, isbn):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO books (title, author, isbn)
                VALUES (?, ?, ?)
            ''', (title, author, isbn))
            conn.commit()

    def update_book(self, book_id, title, author, isbn):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE books SET title = ?, author = ?, isbn = ?
                WHERE id = ?
            ''', (title, author, isbn, book_id))
            conn.commit()

    def get_all_books(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            return cursor.execute('SELECT * FROM books').fetchall()

    def delete_book(self, book_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
            conn.commit()

    
    def send_notification(self, book_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            book = cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
            if book:
                return f"Notification sent to {book[5]} for overdue book '{book[1]}' (Due Date: {book[6]})."
            return "Book not found."


    def get_user_books(self, user_name):
        with self.connect() as conn:
            cursor = conn.cursor()
            return cursor.execute('SELECT * FROM books WHERE borrowed_by = ?', (user_name,)).fetchall()
    from datetime import datetime

    def get_overdue_books(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            today = datetime.now().strftime('%Y-%m-%d')
         # Fetch books that are not available and have a due_date earlier than today
            overdue_books = cursor.execute('''
            SELECT id, title, author, isbn, available, borrowed_by, due_date
            FROM books
            WHERE due_date < ? AND available = 0
            ''', (today,)).fetchall()
            return overdue_books

    def get_overdue_books_for_user(self, user_name):
        with self.connect() as conn:
            cursor = conn.cursor()
            today = datetime.now().strftime('%Y-%m-%d')
            return cursor.execute('SELECT * FROM books WHERE borrowed_by = ? AND due_date < ?', (user_name, today)).fetchall()
