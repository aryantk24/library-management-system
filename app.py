from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import Database


app = Flask(__name__)
app.secret_key = 'library_secret_key'
db = Database()


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

@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    db.delete_book(book_id)
    flash('Book deleted successfully!')
    return redirect(url_for('index'))
@app.route('/send_notification/<int:book_id>')
def send_notification(book_id):
    # Logic to send notification to the user
    message = db.send_notification(book_id)
    flash(message)
    return redirect(url_for('index'))

@app.route('/generate_issue/<int:book_id>')
def generate_issue(book_id):
    # Logic to generate an issue alert
    message = db.generate_issue_alert(book_id)
    flash(message)
    return redirect(url_for('index'))

@app.route('/update_book/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        db.update_book(book_id, title, author, isbn)
        flash('Book updated successfully!')
        return redirect(url_for('index'))
    book = next((b for b in db.get_all_books() if b[0] == book_id), None)
    return render_template('update_book.html', book=book)



@app.route('/')
def index():
    books = db.get_all_books()
    users = db.get_all_users()  # Fetch registered users
    overdue_books = db.get_overdue_books()  # Fetch overdue books
    return render_template('index.html', books=books, users=users, overdue_books=overdue_books)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        try:
            db.register_user(name, password)
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except:
            flash('Username already exists.')
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user = db.authenticate_user(name, password)
        if user:
            session['user'] = name
            flash('Login successful!')
            return redirect(url_for('user_dashboard'))
        flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.')
    return redirect(url_for('login'))

@app.route('/user_dashboard')
def user_dashboard():
    if 'user' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    books = db.get_all_books()
    user_books = db.get_user_books(session['user'])
    overdue_books = db.get_overdue_books_for_user(session['user'])
    return render_template('user_dashboard.html', books=books, user_books=user_books, overdue_books=overdue_books)

@app.route('/borrow_book/<int:book_id>')
def borrow_book(book_id):
    if 'user' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    if db.borrow_book(book_id, session['user']):
        flash('Book borrowed successfully!')
    else:
        flash('Book is not available.')
    return redirect(url_for('user_dashboard'))

@app.route('/return_book/<int:book_id>')
def return_book(book_id):
    if 'user' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))
    if db.return_book(book_id):
        flash('Book returned successfully!')
    else:
        flash('Error returning the book.')
    return redirect(url_for('user_dashboard'))

# Entry point of the application
if __name__ == '__main__':
    db.initialize_tables()  # Initialize the database tables if not already created
    app.run(debug=True)  # Run the application in debug mode
