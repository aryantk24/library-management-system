from database import get_db

def add_book(title, author, isbn):
    db = get_db()
    db.execute('''
        INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)
    ''', (title, author, isbn))
    db.commit()

def get_all_books():
    db = get_db()
    return db.execute('SELECT * FROM books').fetchall()

def search_books(query):
    db = get_db()
    return db.execute('''
        SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
    ''', ('%' + query + '%', '%' + query + '%', '%' + query + '%')).fetchall()

def borrow_book(book_id):
    db = get_db()
    db.execute('''
        UPDATE books SET available = 0 WHERE id = ?
    ''', (book_id,))
    db.commit()

def return_book(book_id):
    db = get_db()
    db.execute('''
        UPDATE books SET available = 1 WHERE id = ?
    ''', (book_id,))
    db.commit()
