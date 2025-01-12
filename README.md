
# Library Management System

A web-based **Library Management System** built using **Flask**. This application allows users to manage books, search for available books, and update book information. The project is fully containerized using Docker for easy deployment and sharing.

---

## **Project Structure**

```
LibraryManagementSystem/
├── static/                   # Static assets
│   ├── styles.css            # Stylesheet
│
├── templates/                # HTML templates
│   ├── add_book.html         # Add new book page
│   ├── base.html             # Base template layout
│   ├── index.html            # Homepage
│   ├── login.html            # Login page
│   ├── register.html         # Registration page
│   ├── search_book.html      # Book search page
│   ├── update_book.html      # Update book details page
│   ├── user_dashboard.html   # User dashboard
│
├── .dockerignore             # Files to exclude during Docker build
├── .gitignore                # Files to ignore in Git
├── app.py                    # Main Flask application
├── database.py               # Database connection logic
├── Dockerfile                # Docker configuration for containerization
├── library.db                # SQLite database file
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
```

---

## **Features**
- User login and registration system.
- Add, update, and delete books.
- Search for books by title or author.
- User dashboard for managing books.
- Fully containerized with Docker.

---

## **Getting Started**

### **Clone the Repository**
To get a local copy of the project, run:
```bash
git clone https://github.com/<your-username>/LibraryManagementSystem.git
cd LibraryManagementSystem
```

### **Install Dependencies**
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### **Run the Application**
1. Run the Flask application:
   ```bash
   python app.py
   ```
2. Access the application in your browser:
   ```
   http://127.0.0.1:5000
   ```

---
## **Using the Docker Image from Docker Hub**

If the Docker image is available on Docker Hub, pull and run the container:

### **Pull the Image**
```bash
docker pull <your-dockerhub-username>/library-management
```

### **Run the Image**
```bash
docker run -p 4000:5000 <your-dockerhub-username>/library-management
```
---

## **Using Docker**

### **Build the Docker Image**
To containerize the application, use the following command:
```bash
docker build -t library-management .
```

### **Run the Docker Container**
Run the container and map port `4000` on your machine to port `5000` in the container:
```bash
docker run -p 4000:5000 library-management
```

Visit the application in your browser:
```
http://localhost:4000
```

---

## **How to Contribute**

### **Fork and Clone**
1. Fork the repository on GitHub.
2. Clone your fork:
   ```bash
   git clone https://github.com/<your-username>/LibraryManagementSystem.git
   ```

### **Create a Branch**
Create a new branch for your feature:
```bash
git checkout -b feature/new-feature
```

### **Commit Changes**
1. Make changes to the project.
2. Commit your changes:
   ```bash
   git add .
   git commit -m "Add new feature"
   ```

### **Push and Submit a Pull Request**
1. Push your branch:
   ```bash
   git push origin feature/new-feature
   ```
2. Submit a pull request to the `main` branch.

---

## **License**
This project is licensed under the [MIT License](LICENSE).

---
