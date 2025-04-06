import os
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser  # Open PDFs in the default browser

db_file = "bookstore.db"
books_folder = "books"
os.makedirs(books_folder, exist_ok=True)

# Database setup
def init_db():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            genre TEXT,
            file_path TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def upload_book(title, author, genre, file_path):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    new_path = os.path.join(books_folder, os.path.basename(file_path))

    # Prevent overwriting existing files
    if os.path.exists(new_path):
        base, ext = os.path.splitext(os.path.basename(file_path))
        new_path = os.path.join(books_folder, f"{base}_copy{ext}")

    try:
        os.replace(file_path, new_path)  # Move file safely
        cursor.execute("INSERT INTO books (title, author, genre, file_path) VALUES (?, ?, ?, ?)",
                       (title, author, genre, new_path))
        conn.commit()
        print("Book uploaded successfully and saved in the database!")
    except sqlite3.IntegrityError:
        print("Error: This book already exists in the database!")
    except Exception as e:
        print(f"Error uploading book: {e}")
    finally:
        conn.close()

def list_books():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, file_path FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

def open_pdf(file_path):
    if not os.path.exists(file_path):
        print("Error: File not found!")
        return
   
    print(f"Opening {file_path} in the browser...")
    webbrowser.open_new(rf"file://{os.path.abspath(file_path)}")

def download_book(book_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT file_path FROM books WHERE id=?", (book_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        file_path = result[0]
        root = tk.Tk()
        root.withdraw()
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        root.destroy()

        if save_path:
            try:
                with open(file_path, "rb") as src, open(save_path, "wb") as dst:
                    dst.write(src.read())
                print("Book downloaded successfully!")
            except Exception as e:
                print(f"Download error: {e}")

def main_menu():
    while True:
        print("\n1. Read a Book")
        print("2. Upload a Book")
        print("3. Download a Book")
        print("4. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            books = list_books()
            if not books:
                print("No books available! Please upload a book first.")
                continue

            print("\nAvailable Books:")
            for b in books:
                print(f"{b[0]}. {b[1]} by {b[2]}")

            try:
                book_id = int(input("Enter book ID to read: "))
                book = next((b for b in books if b[0] == book_id), None)
                if book:
                    open_pdf(book[3])  # Open the PDF in the browser
                else:
                    print("Invalid book ID! Please enter a valid number.")
            except ValueError:
                print("Invalid input! Please enter a number.")

        elif choice == "2":
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            genre = input("Enter genre: ")

            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF files", "*.pdf")])
            root.destroy()

            if not file_path:
                print("No file selected! Please try again.")
                continue

            upload_book(title, author, genre, file_path)

        elif choice == "3":
            books = list_books()
            if not books:
                print("No books available for download!")
                continue

            print("\nAvailable Books:")
            for b in books:
                print(f"{b[0]}. {b[1]} by {b[2]}")

            try:
                book_id = int(input("Enter book ID to download: "))
                if any(b[0] == book_id for b in books):
                    download_book(book_id)
                else:
                    print("Invalid book ID! Please enter a valid number.")
            except ValueError:
                print("Invalid input! Please enter a number.")

        elif choice == "4":
            print("Exiting program...")
            break
        else:
            print("Invalid choice! Try again.")

def login_screen():
    username = input("Enter username: ")
    password = input("Enter password: ")
    if login_user(username, password):
        print("Login successful!")
        main_menu()
    else:
        print("Invalid credentials!")

def register_screen():
    username = input("Enter new username: ")
    password = input("Enter new password: ")
    if register_user(username, password):
        print("Registration successful! Proceed to login.")
    else:
        print("Username already exists!")

def start():
    init_db()
    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Select an option: ")
        if choice == "1":
            login_screen()
        elif choice == "2":
            register_screen()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option! Try again.")

if __name__ == "__main__":
    start()