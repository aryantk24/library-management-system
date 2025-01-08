from flask import Flask, render_template, request, redirect, url_for, flash
from database import Database

# Initialize the Flask application
app = Flask(__name__)

# Secret key for session management and flash messages
app.secret_key = 'library_secret_key'

# Create an instance of the Database class for database operations
db = Database()

# Route for the home page
@app.route('/')
def index():
    """
    Display the home page with a list of all books.
    """
    books = db.get_all_books()  # Fetch all books from the database
    return render_template('index.html', books=books)

# Route for adding a new book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Add a new book to the library. 
    Handles both GET and POST requests:
    - GET: Display the form to add a book.
    - POST: Save the book details to the database.
    """
    if request.method == 'POST':
        # Get book details from the submitted form
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        
        # Add the book to the database
        db.add_book(title, author, isbn)
        
        # Flash success message
        flash('Book added successfully!')
        
        # Redirect to the home page
        return redirect(url_for('index'))
    
    # Render the form to add a book
    return render_template('add_book.html')

# Route for searching books
@app.route('/search', methods=['GET', 'POST'])
def search_book():
    """
    Search for books by title, author, or ISBN.
    Handles both GET and POST requests:
    - GET: Display the search form.
    - POST: Perform the search and display results.
    """
    if request.method == 'POST':
        # Get the search query from the form
        query = request.form['query']
        
        # Search for books matching the query in the database
        results = db.search_books(query)
        
        # Render the search results page
        return render_template('search_book.html', books=results, query=query)
    
    # Render an empty search page for GET requests
    return render_template('search_book.html', books=[])

# Route for deleting a book
@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    """
    Delete a book from the library by its ID.
    """
    db.delete_book(book_id)  # Remove the book from the database
    
    # Flash success message
    flash('Book deleted successfully!')
    
    # Redirect to the home page
    return redirect(url_for('index'))

# Route for borrowing a book
@app.route('/borrow_book/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    """
    Borrow a book from the library by its ID.
    - POST request: Requires the user's name.
    """
    user_name = request.form['user']  # Get the user's name from the form
    
    if db.borrow_book(book_id, user_name):  # Attempt to borrow the book
        flash('Book borrowed successfully!')  # Success message
    else:
        flash('Book is already borrowed!')  # Error message if book is unavailable
    
    # Redirect to the home page
    return redirect(url_for('index'))

# Route for returning a borrowed book
@app.route('/return_book/<int:book_id>', methods=['POST'])
def return_book(book_id):
    """
    Return a borrowed book to the library by its ID.
    """
    if db.return_book(book_id):  # Attempt to return the book
        flash('Book returned successfully!')  # Success message
    else:
        flash('Book is not borrowed!')  # Error message if the book wasn't borrowed
    
    # Redirect to the home page
    return redirect(url_for('index'))

# Entry point of the application
if __name__ == '__main__':
    db.initialize_tables()  # Initialize the database tables if not already created
    app.run(debug=True)  # Run the application in debug mode
