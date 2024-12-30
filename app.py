from flask import Flask, render_template, request, redirect, url_for, flash
from database import Database

app = Flask(__name__)
app.secret_key = 'library_secret_key'
db = Database()

@app.route('/')
def index():
    books = db.get_all_books()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        db.add_book(title, author, isbn)
        flash('Book added successfully!')
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/search', methods=['GET', 'POST'])
def search_book():
    if request.method == 'POST':
        query = request.form['query']
        results = db.search_books(query)
        return render_template('search_book.html', books=results, query=query)
    return render_template('search_book.html', books=[])

@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    db.delete_book(book_id)
    flash('Book deleted successfully!')
    return redirect(url_for('index'))

@app.route('/borrow_book/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    user_name = request.form['user']
    if db.borrow_book(book_id, user_name):
        flash('Book borrowed successfully!')
    else:
        flash('Book is already borrowed!')
    return redirect(url_for('index'))

@app.route('/return_book/<int:book_id>', methods=['POST'])
def return_book(book_id):
    if db.return_book(book_id):
        flash('Book returned successfully!')
    else:
        flash('Book is not borrowed!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.initialize_tables()  # Ensure tables are created when app starts
    app.run(debug=True)
