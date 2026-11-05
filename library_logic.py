import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("books.json")


class LibraryManager:

    def __init__(self):
        self.books = self.load_books()

    def load_books(self):
        if not DATA_FILE.exists():
            DATA_FILE.write_text("[]", encoding="utf-8")

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

    def save_books(self):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.books, file, indent=4)

    def get_book(self, book_id):
        for book in self.books:
            if book["book_id"].lower() == book_id.lower():
                return book
        return None

    def add_book(self, book_id, title, author, category, quantity):
        if self.get_book(book_id):
            return False, "A book with this ID already exists."

        book = {
            "book_id": book_id,
            "title": title,
            "author": author,
            "category": category,
            "quantity": quantity,
            "issued": []
        }

        self.books.append(book)
        self.save_books()
        return True, "Book added successfully!"

    def update_book(self, book_id, title, author, category, quantity):
        book = self.get_book(book_id)

        if not book:
            return False, "Book not found."

        if quantity < len(book["issued"]):
            return False, "Quantity cannot be less than issued copies."

        book["title"] = title
        book["author"] = author
        book["category"] = category
        book["quantity"] = quantity

        self.save_books()
        return True, "Book updated successfully!"

    def delete_book(self, book_id):
        book = self.get_book(book_id)

        if not book:
            return False, "Book not found."

        if book["issued"]:
            return False, "Return all issued copies before deleting."

        self.books.remove(book)
        self.save_books()
        return True, "Book deleted successfully!"

    def issue_book(self, book_id, borrower, due_date):
        book = self.get_book(book_id)

        if not book:
            return False, "Book not found."

        if not borrower.strip():
            return False, "Enter the borrower's name."

        available = book["quantity"] - len(book["issued"])

        if available <= 0:
            return False, "No copies available."

        book["issued"].append({
            "borrower": borrower.strip(),
            "due_date": due_date
        })

        self.save_books()
        return True, "Book issued successfully!"

    def return_book(self, book_id, borrower):
        book = self.get_book(book_id)

        if not book:
            return False, "Book not found."

        if not borrower.strip():
            return False, "Enter the borrower's name."

        for record in book["issued"]:
            if record["borrower"].lower() == borrower.strip().lower():
                book["issued"].remove(record)
                self.save_books()
                return True, "Book returned successfully!"

        return False, "No issued record found for this borrower."

    def search_books(self, keyword):
        keyword = keyword.lower().strip()

        if not keyword:
            return self.books

        return [
            book for book in self.books
            if keyword in book["book_id"].lower()
            or keyword in book["title"].lower()
            or keyword in book["author"].lower()
            or keyword in book["category"].lower()
        ]