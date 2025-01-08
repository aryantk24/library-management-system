## Subject project management with GIT

# Library Management System
A collaborative open-source project to manage library functionalities like adding books, searching books, borrowing, and returning them. Built using Flask and SQLite.

## Features
- Add, delete, and update books.
- Search books by title, author, or ISBN.
- Borrow and return books.
- Basic file-based storage using SQLite.

## Project Structure
LibraryManagementSystem/
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   └── utils.py
├── frontend/
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── add_book.html
│   │   ├── search_book.html
│   │   ├── borrow_book.html
│   │   └── return_book.html
│   └── static/
│       ├── styles.css
│       └── script.js
├── README.md
└── requirements.txt

## How to run
1. Clone the directory to your local machine
2. Switch to the repository
3. Run app.py
4. Use the app
