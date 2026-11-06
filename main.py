
import sys
import json
import os

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QStackedWidget, QMessageBox, QDialog, QFormLayout, QSpinBox,
    QComboBox, QHeaderView, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


# ---------------- DATA STORAGE ----------------

DATA_FILE = "library_data.json"
SETTINGS_FILE = "library_settings.json"


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                stored_data = json.load(file)

                return {
                    "books": stored_data.get("books", []),
                    "loans": stored_data.get("loans", []),
                    "students": stored_data.get("students", [])
                }

        except (json.JSONDecodeError, OSError):
            pass

    return {"books": [], "loans": [], "students": []}


data = load_data()


def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_theme():
    try:
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file).get("theme", "Light")
    except (OSError, json.JSONDecodeError):
        return "Light"


def save_theme(theme):
    with open(SETTINGS_FILE, "w") as file:
        json.dump({"theme": theme}, file, indent=4)


# ---------------- THEMES ----------------

LIGHT_THEME = {
    "window": "#F4F6FA",
    "sidebar": "#172B4D",
    "sidebar_hover": "#344C78",
    "sidebar_active": "#405A98",
    "surface": "#FFFFFF",
    "surface_alt": "#F8FAFD",
    "text": "#263746",
    "muted": "#718096",
    "primary": "#263D73",
    "primary_hover": "#405A98",
    "border": "#DCE2EB",
    "table_header": "#E9EDF5",
    "table_alternate": "#F7F9FC",
    "selection": "#DCE6F7",
    "selection_text": "#172B4D",
    "input": "#FFFFFF",
    "danger": "#C0392B",
    "danger_hover": "#A93226"
}

DARK_THEME = {
    "window": "#151B29",
    "sidebar": "#0D1321",
    "sidebar_hover": "#27344B",
    "sidebar_active": "#344B70",
    "surface": "#202A3B",
    "surface_alt": "#273347",
    "text": "#E7ECF5",
    "muted": "#A0AEC0",
    "primary": "#5276B5",
    "primary_hover": "#698BC9",
    "border": "#39465B",
    "table_header": "#2B3950",
    "table_alternate": "#263246",
    "selection": "#3C5275",
    "selection_text": "#FFFFFF",
    "input": "#263246",
    "danger": "#C64B4B",
    "danger_hover": "#E05B5B"
}


# ---------------- BOOK FORM ----------------

class BookDialog(QDialog):

    def __init__(self, parent=None, book=None):
        super().__init__(parent)

        self.setWindowTitle("Book Information")
        self.setFixedSize(380, 330)

        layout = QFormLayout(self)

        self.title = QLineEdit()
        self.author = QLineEdit()

        self.category = QComboBox()
        self.category.addItems([
            "Fiction", "Science", "Technology",
            "History", "Education", "Other"
        ])

        self.quantity = QSpinBox()
        self.quantity.setRange(1, 1000)

        layout.addRow("Book Title:", self.title)
        layout.addRow("Author:", self.author)
        layout.addRow("Category:", self.category)
        layout.addRow("Quantity:", self.quantity)

        if book:
            self.title.setText(book["title"])
            self.author.setText(book["author"])
            self.category.setCurrentText(book["category"])
            self.quantity.setValue(book["quantity"])

        save_button = QPushButton("Save Book")
        save_button.clicked.connect(self.validate)
        layout.addRow(save_button)

    def validate(self):
        if not self.title.text().strip() or not self.author.text().strip():
            QMessageBox.warning(
                self, "Missing Information",
                "Please enter the book title and author."
            )
            return

        self.accept()

    def get_data(self):
        return {
            "title": self.title.text().strip(),
            "author": self.author.text().strip(),
            "category": self.category.currentText(),
            "quantity": self.quantity.value()
        }


# ---------------- STUDENT FORM ----------------

class StudentDialog(QDialog):

    def __init__(self, parent=None, student=None):
        super().__init__(parent)

        self.setWindowTitle("Student Information")
        self.setFixedSize(420, 430)

        layout = QFormLayout(self)

        self.student_id = QLineEdit()
        self.student_id.setPlaceholderText("Enter Student ID")

        self.name = QLineEdit()
        self.name.setPlaceholderText("Enter full name")

        self.gender = QComboBox()
        self.gender.addItems(["Male", "Female", "Other"])

        # Class is manually editable
        self.student_class = QLineEdit()
        self.student_class.setPlaceholderText("Enter class ")

        self.section = QComboBox()
        self.section.setEditable(True)
        self.section.addItems(["A", "B", "C", "D"])

        self.contact = QLineEdit()
        self.contact.setPlaceholderText("Enter contact number")

        layout.addRow("Student ID:", self.student_id)
        layout.addRow("Full Name:", self.name)
        layout.addRow("Gender:", self.gender)
        layout.addRow("Class:", self.student_class)
        layout.addRow("Section:", self.section)
        layout.addRow("Contact Number:", self.contact)

        if student:
            self.student_id.setText(student["student_id"])
            self.student_id.setReadOnly(True)
            self.name.setText(student["name"])
            self.gender.setCurrentText(student["gender"])
            self.student_class.setText(student["class"])
            self.section.setCurrentText(student["section"])
            self.contact.setText(student["contact"])

        save_button = QPushButton("Save Student")
        save_button.clicked.connect(self.validate)
        layout.addRow(save_button)

    def validate(self):
        student_id = self.student_id.text().strip()
        name = self.name.text().strip()
        student_class = self.student_class.text().strip()
        section = self.section.currentText().strip()
        contact = self.contact.text().strip()

        if not student_id:
            QMessageBox.warning(
                self, "Missing Information",
                "Please enter the Student ID."
            )
            return

        if not name:
            QMessageBox.warning(
                self, "Missing Information",
                "Please enter the student's full name."
            )
            return

        if not student_class:
            QMessageBox.warning(
                self, "Missing Information",
                "Please enter the student's class."
            )
            return

        if not section:
            QMessageBox.warning(
                self, "Missing Information",
                "Please enter the student's section."
            )
            return

        if not contact:
            QMessageBox.warning(
                self, "Missing Information",
                "Please enter the student's contact number."
            )
            return

        if not self.student_id.isReadOnly():
            if any(
                s["student_id"] == student_id
                for s in data["students"]
            ):
                QMessageBox.warning(
                    self, "Duplicate Student ID",
                    "This Student ID is already registered."
                )
                return

        self.accept()

    def get_data(self):
        return {
            "student_id": self.student_id.text().strip(),
            "name": self.name.text().strip(),
            "gender": self.gender.currentText(),
            "class": self.student_class.text().strip(),
            "section": self.section.currentText().strip(),
            "contact": self.contact.text().strip()
        }


# ---------------- MAIN APPLICATION ----------------

class LibraryManagementSystem(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Library Management System")
        self.setMinimumSize(1050, 650)

        self.current_theme = load_theme()

        self.setup_ui()
        self.apply_theme()
        self.refresh_all()
        self.show_dashboard()

    # ---------------- THEME MANAGEMENT ----------------

    def apply_theme(self):

        theme = (
            DARK_THEME
            if self.current_theme == "Dark"
            else LIGHT_THEME
        )

        self.setStyleSheet(f"""
            QWidget {{
                font-family: Segoe UI;
                font-size: 13px;
                color: {theme["text"]};
            }}

            QMainWindow {{
                background-color: {theme["window"]};
            }}

            QWidget#centralWidget,
            QStackedWidget {{
                background-color: {theme["window"]};
            }}

            QFrame#sidebar {{
                background-color: {theme["sidebar"]};
                border: none;
            }}

            QLabel#logo {{
                color: #FFFFFF;
                font-size: 19px;
                font-weight: bold;
            }}

            QLabel#footer {{
                color: #AAB8D0;
                padding: 15px;
            }}

            QLabel#subtitle {{
                color: {theme["muted"]};
            }}

            QFrame#card,
            QFrame#formFrame {{
                background-color: {theme["surface"]};
                border: 1px solid {theme["border"]};
                border-radius: 12px;
            }}

            QLabel#cardName {{
                color: {theme["muted"]};
                font-size: 12px;
            }}

            QLabel#cardNumber {{
                color: {theme["primary"]};
                font-size: 27px;
                font-weight: bold;
            }}

            QPushButton {{
                background-color: {theme["primary"]};
                color: #FFFFFF;
                border: none;
                padding: 11px 15px;
                border-radius: 6px;
                font-weight: 600;
            }}

            QPushButton:hover {{
                background-color: {theme["primary_hover"]};
            }}

            QPushButton#navButton {{
                background-color: transparent;
                color: #FFFFFF;
                text-align: left;
                padding: 14px;
                border-radius: 6px;
                font-weight: normal;
            }}

            QPushButton#navButton:hover {{
                background-color: {theme["sidebar_hover"]};
            }}

            QPushButton#themeButton {{
                background-color: {theme["sidebar_hover"]};
                color: #FFFFFF;
                padding: 12px;
            }}

            QPushButton#themeButton:hover {{
                background-color: {theme["sidebar_active"]};
            }}

            QLineEdit,
            QComboBox,
            QSpinBox {{
                background-color: {theme["input"]};
                color: {theme["text"]};
                border: 1px solid {theme["border"]};
                padding: 9px;
                border-radius: 6px;
                selection-background-color: {theme["selection"]};
            }}

            QLineEdit:focus,
            QComboBox:focus,
            QSpinBox:focus {{
                border: 1px solid {theme["primary"]};
            }}

            QComboBox QAbstractItemView {{
                background-color: {theme["surface"]};
                color: {theme["text"]};
                selection-background-color: {theme["selection"]};
                selection-color: {theme["selection_text"]};
                border: 1px solid {theme["border"]};
            }}

            QTableWidget {{
                background-color: {theme["surface"]};
                alternate-background-color: {theme["table_alternate"]};
                color: {theme["text"]};
                border: 1px solid {theme["border"]};
                gridline-color: {theme["border"]};
                selection-background-color: {theme["selection"]};
                selection-color: {theme["selection_text"]};
                border-radius: 8px;
            }}

            QHeaderView::section {{
                background-color: {theme["table_header"]};
                color: {theme["text"]};
                padding: 11px;
                border: none;
                border-bottom: 1px solid {theme["border"]};
                font-weight: bold;
            }}

            QTableCornerButton::section {{
                background-color: {theme["table_header"]};
                border: none;
            }}

            QScrollBar:vertical {{
                background-color: {theme["window"]};
                width: 10px;
                margin: 0;
            }}

            QScrollBar::handle:vertical {{
                background-color: {theme["muted"]};
                border-radius: 4px;
                min-height: 25px;
            }}

            QScrollBar:horizontal {{
                background-color: {theme["window"]};
                height: 10px;
            }}

            QScrollBar::handle:horizontal {{
                background-color: {theme["muted"]};
                border-radius: 4px;
                min-width: 25px;
            }}

            QDialog {{
                background-color: {theme["window"]};
            }}

            QMessageBox {{
                background-color: {theme["surface"]};
            }}

            QToolTip {{
                background-color: {theme["sidebar"]};
                color: white;
                border: none;
                padding: 5px;
            }}
        """)

        self.theme_button.setText(
            "☀  Switch to Light Mode"
            if self.current_theme == "Dark"
            else "☾  Switch to Dark Mode"
        )

        self.theme_button.setToolTip(
            "Change the application appearance"
        )

    def toggle_theme(self):

        self.current_theme = (
            "Dark" if self.current_theme == "Light"
            else "Light"
        )

        save_theme(self.current_theme)
        self.apply_theme()

    # ---------------- MAIN UI ----------------

    def setup_ui(self):

        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(230)

        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(15, 25, 15, 20)
        side_layout.setSpacing(8)

        logo = QLabel("LIBRARY SYSTEM")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        side_layout.addWidget(logo)
        side_layout.addSpacing(30)

        self.stack = QStackedWidget()

        menu_items = [
            ("▦   Dashboard", self.show_dashboard),
            ("▤   Books", self.show_books),
            ("＋   Issue Book", self.show_issue_page),
            ("↩   Return Book", self.show_issued),
            ("♙   Borrower's Information", self.show_borrowers)
        ]

        for name, function in menu_items:

            button = QPushButton(name)
            button.setObjectName("navButton")
            button.setMinimumHeight(45)
            button.clicked.connect(function)
            side_layout.addWidget(button)

        side_layout.addStretch()

        self.theme_button = QPushButton()
        self.theme_button.setObjectName("themeButton")
        self.theme_button.clicked.connect(self.toggle_theme)

        side_layout.addWidget(self.theme_button)

        footer = QLabel("Library Management\nSystem v1.0")
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        side_layout.addWidget(footer)

        # Pages

        self.dashboard_page = QWidget()
        self.books_page = QWidget()
        self.issue_page = QWidget()
        self.issued_page = QWidget()
        self.borrowers_page = QWidget()

        self.create_dashboard()
        self.create_books_page()
        self.create_issue_page()
        self.create_issued_page()
        self.create_borrowers_page()

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.books_page)
        self.stack.addWidget(self.issue_page)
        self.stack.addWidget(self.issued_page)
        self.stack.addWidget(self.borrowers_page)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)

    # ---------------- COMMON LABEL ----------------

    def create_heading(self, title, subtitle):

        heading = QLabel(title)
        heading.setFont(QFont("Segoe UI", 23, QFont.Weight.Bold))

        description = QLabel(subtitle)
        description.setObjectName("subtitle")

        return heading, description

    # ---------------- DASHBOARD ----------------

    def create_dashboard(self):

        layout = QVBoxLayout(self.dashboard_page)
        layout.setContentsMargins(30, 25, 30, 25)

        heading, subtitle = self.create_heading(
            "Library Dashboard",
            "Overview of your library records"
        )

        layout.addWidget(heading)
        layout.addWidget(subtitle)
        layout.addSpacing(25)

        cards = QHBoxLayout()
        cards.setSpacing(15)

        self.total_books = self.create_card(
            "Total Book Copies", "0"
        )

        self.available_books = self.create_card(
            "Available Copies", "0"
        )

        self.issued_books = self.create_card(
            "Issued Books", "0"
        )

        self.total_students = self.create_card(
            "Registered Students", "0"
        )

        cards.addWidget(self.total_books)
        cards.addWidget(self.available_books)
        cards.addWidget(self.issued_books)
        cards.addWidget(self.total_students)

        layout.addLayout(cards)
        layout.addSpacing(30)

        recent_label = QLabel("Recently Added Books")
        recent_label.setFont(
            QFont("Segoe UI", 16, QFont.Weight.Bold)
        )

        layout.addWidget(recent_label)

        self.recent_table = QTableWidget()
        self.recent_table.setColumnCount(3)
        self.recent_table.setHorizontalHeaderLabels([
            "Book Title", "Author", "Category"
        ])

        self.style_table(self.recent_table)
        layout.addWidget(self.recent_table)
        layout.addStretch()

    def create_card(self, title, value):

        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 20, 18, 20)
        layout.setSpacing(12)

        name = QLabel(title)
        name.setObjectName("cardName")

        number = QLabel(value)
        number.setObjectName("cardNumber")
        number.setFont(
            QFont("Segoe UI", 25, QFont.Weight.Bold)
        )

        layout.addWidget(name)
        layout.addWidget(number)

        card.number_label = number

        return card

    # ---------------- BOOKS PAGE ----------------

    def create_books_page(self):

        layout = QVBoxLayout(self.books_page)
        layout.setContentsMargins(30, 25, 30, 25)

        heading, subtitle = self.create_heading(
            "Books",
            "Add, search, edit and delete library books."
        )

        layout.addWidget(heading)
        layout.addWidget(subtitle)
        layout.addSpacing(20)

        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search by title or author..."
        )
        self.search_input.textChanged.connect(self.search_books)

        search_layout.addWidget(self.search_input)

        add_button = QPushButton("+ Add Book")
        add_button.clicked.connect(self.add_book)
        search_layout.addWidget(add_button)

        layout.addLayout(search_layout)

        self.books_table = QTableWidget()
        self.books_table.setColumnCount(6)
        self.books_table.setHorizontalHeaderLabels([
            "ID", "Title", "Author", "Category",
            "Total Copies", "Available"
        ])

        self.style_table(self.books_table)
        layout.addWidget(self.books_table)

        buttons = QHBoxLayout()

        edit_button = QPushButton("Edit Selected")
        edit_button.clicked.connect(self.edit_book)

        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_book)

        buttons.addWidget(edit_button)
        buttons.addWidget(delete_button)

        layout.addLayout(buttons)

    # ---------------- ISSUE BOOK PAGE ----------------

    def create_issue_page(self):

        layout = QVBoxLayout(self.issue_page)
        layout.setContentsMargins(30, 25, 30, 25)

        heading, subtitle = self.create_heading(
            "Issue Book",
            "Select a registered student and an available book."
        )

        layout.addWidget(heading)
        layout.addWidget(subtitle)
        layout.addSpacing(25)

        form_frame = QFrame()
        form_frame.setObjectName("formFrame")

        form_layout = QFormLayout(form_frame)
        form_layout.setContentsMargins(25, 25, 25, 25)
        form_layout.setSpacing(18)

        self.issue_book_combo = QComboBox()
        self.issue_student_combo = QComboBox()

        form_layout.addRow(
            "Select Available Book:",
            self.issue_book_combo
        )

        form_layout.addRow(
            "Select Student:",
            self.issue_student_combo
        )

        issue_button = QPushButton("Confirm Issue")
        issue_button.clicked.connect(self.process_issue)
        form_layout.addRow(issue_button)

        layout.addWidget(form_frame)
        layout.addStretch()

    # ---------------- RETURN BOOK PAGE ----------------

    def create_issued_page(self):

        layout = QVBoxLayout(self.issued_page)
        layout.setContentsMargins(30, 25, 30, 25)

        heading, subtitle = self.create_heading(
            "Return Book",
            "View currently borrowed books and process returns."
        )

        layout.addWidget(heading)
        layout.addWidget(subtitle)
        layout.addSpacing(20)

        self.issued_table = QTableWidget()
        self.issued_table.setColumnCount(5)
        self.issued_table.setHorizontalHeaderLabels([
            "Book ID", "Book Title", "Student ID",
            "Borrower", "Status"
        ])

        self.style_table(self.issued_table)
        layout.addWidget(self.issued_table)

        return_button = QPushButton("Return Selected Book")
        return_button.clicked.connect(self.return_book)
        layout.addWidget(return_button)

    # ---------------- BORROWER INFORMATION PAGE ----------------

    def create_borrowers_page(self):

        layout = QVBoxLayout(self.borrowers_page)
        layout.setContentsMargins(30, 25, 30, 25)

        heading, subtitle = self.create_heading(
            "Borrower's Information",
            "Register and manage student information."
        )

        layout.addWidget(heading)
        layout.addWidget(subtitle)
        layout.addSpacing(20)

        search_layout = QHBoxLayout()

        self.borrower_search = QLineEdit()
        self.borrower_search.setPlaceholderText(
            "Search by Student ID or name..."
        )
        self.borrower_search.textChanged.connect(
            self.refresh_borrowers_table
        )

        search_layout.addWidget(self.borrower_search)

        add_student_button = QPushButton("+ Add Student")
        add_student_button.clicked.connect(self.add_student)
        search_layout.addWidget(add_student_button)

        layout.addLayout(search_layout)

        self.borrowers_table = QTableWidget()
        self.borrowers_table.setColumnCount(6)
        self.borrowers_table.setHorizontalHeaderLabels([
            "Student ID", "Full Name", "Gender",
            "Class", "Section", "Contact Number"
        ])

        self.style_table(self.borrowers_table)
        layout.addWidget(self.borrowers_table)

        buttons = QHBoxLayout()

        edit_button = QPushButton("Edit Student")
        edit_button.clicked.connect(self.edit_student)

        delete_button = QPushButton("Delete Student")
        delete_button.clicked.connect(self.delete_student)

        history_button = QPushButton("Borrowing History")
        history_button.clicked.connect(self.view_borrowing_history)

        buttons.addWidget(edit_button)
        buttons.addWidget(delete_button)
        buttons.addWidget(history_button)

        layout.addLayout(buttons)

    # ---------------- TABLE STYLE ----------------

    def style_table(self, table):

        table.setAlternatingRowColors(True)

        table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        table.verticalHeader().setVisible(False)

    # ---------------- NAVIGATION ----------------

    def show_dashboard(self):
        self.refresh_all()
        self.stack.setCurrentWidget(self.dashboard_page)

    def show_books(self):
        self.refresh_all()
        self.stack.setCurrentWidget(self.books_page)

    def show_issue_page(self):

        self.refresh_all()

        self.issue_book_combo.clear()
        self.issue_student_combo.clear()

        for book in data["books"]:
            if book["available"] > 0:
                self.issue_book_combo.addItem(
                    f"{book['title']} (Available: {book['available']})",
                    book["id"]
                )

        for student in data["students"]:
            self.issue_student_combo.addItem(
                f"{student['student_id']} - {student['name']} "
                f"({student['class']}-{student['section']})",
                student["student_id"]
            )

        self.stack.setCurrentWidget(self.issue_page)

    def show_issued(self):
        self.refresh_all()
        self.stack.setCurrentWidget(self.issued_page)

    def show_borrowers(self):
        self.refresh_all()
        self.stack.setCurrentWidget(self.borrowers_page)

    # ---------------- REFRESH DATA ----------------

    def refresh_all(self):

        books = data["books"]
        loans = data["loans"]

        total = sum(book["quantity"] for book in books)
        available = sum(book["available"] for book in books)

        issued = sum(
            1 for loan in loans
            if loan["status"] == "Issued"
        )

        self.total_books.number_label.setText(str(total))
        self.available_books.number_label.setText(str(available))
        self.issued_books.number_label.setText(str(issued))
        self.total_students.number_label.setText(
            str(len(data["students"]))
        )

        # Recently added books

        self.recent_table.setRowCount(0)

        for book in books[-5:][::-1]:

            row = self.recent_table.rowCount()
            self.recent_table.insertRow(row)

            values = [
                book["title"],
                book["author"],
                book["category"]
            ]

            for column, value in enumerate(values):
                self.recent_table.setItem(
                    row, column, QTableWidgetItem(str(value))
                )

        self.search_books(self.search_input.text())

        # Currently issued books

        self.issued_table.setRowCount(0)

        for loan_index, loan in enumerate(loans):

            if loan["status"] != "Issued":
                continue

            row = self.issued_table.rowCount()
            self.issued_table.insertRow(row)

            book = self.find_book(loan["book_id"])
            title = book["title"] if book else "Deleted Book"

            values = [
                str(loan["book_id"]),
                title,
                loan.get("student_id", ""),
                loan.get("borrower", ""),
                loan["status"]
            ]

            for column, value in enumerate(values):

                item = QTableWidgetItem(str(value))

                if column == 0:
                    item.setData(
                        Qt.ItemDataRole.UserRole,
                        loan_index
                    )

                self.issued_table.setItem(row, column, item)

        self.refresh_borrowers_table(
            self.borrower_search.text()
        )

    # ---------------- STUDENT MANAGEMENT ----------------

    def selected_student(self):

        row = self.borrowers_table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self, "Selection Required",
                "Please select a student first."
            )
            return None

        student_id = self.borrowers_table.item(row, 0).text()
        return self.find_student(student_id)

    def find_student(self, student_id):

        for student in data["students"]:
            if student["student_id"] == student_id:
                return student

        return None

    def add_student(self):

        dialog = StudentDialog(self)

        if dialog.exec():

            details = dialog.get_data()
            data["students"].append(details)

            save_data()
            self.refresh_all()

            QMessageBox.information(
                self, "Success",
                "Student registered successfully!"
            )

    def edit_student(self):

        student = self.selected_student()

        if not student:
            return

        dialog = StudentDialog(self, student)

        if dialog.exec():

            details = dialog.get_data()
            student.update(details)

            save_data()
            self.refresh_all()

            QMessageBox.information(
                self, "Updated",
                "Student information updated successfully!"
            )

    def delete_student(self):

        student = self.selected_student()

        if not student:
            return

        student_id = student["student_id"]

        active_loans = [
            loan for loan in data["loans"]
            if loan.get("student_id") == student_id
            and loan["status"] == "Issued"
        ]

        if active_loans:
            QMessageBox.warning(
                self, "Cannot Delete",
                "This student currently has borrowed books. "
                "Please process the returns before deleting "
                "the student."
            )
            return

        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete {student['name']}?"
        )

        if confirm == QMessageBox.StandardButton.Yes:

            data["students"].remove(student)

            save_data()
            self.refresh_all()

            QMessageBox.information(
                self, "Deleted",
                "Student record deleted successfully!"
            )

    def refresh_borrowers_table(self, search_text=""):

        if not hasattr(self, "borrowers_table"):
            return

        search_text = search_text.lower().strip()
        self.borrowers_table.setRowCount(0)

        for student in data["students"]:

            searchable = (
                student["student_id"] + " " +
                student["name"]
            ).lower()

            if search_text not in searchable:
                continue

            row = self.borrowers_table.rowCount()
            self.borrowers_table.insertRow(row)

            values = [
                student["student_id"],
                student["name"],
                student["gender"],
                student["class"],
                student["section"],
                student["contact"]
            ]

            for column, value in enumerate(values):
                self.borrowers_table.setItem(
                    row, column, QTableWidgetItem(str(value))
                )

    # ---------------- BORROWING HISTORY ----------------

    def view_borrowing_history(self):

        student = self.selected_student()

        if not student:
            return

        history = []

        for loan in data["loans"]:

            if loan.get("student_id") == student["student_id"]:

                book = self.find_book(loan["book_id"])
                title = book["title"] if book else "Deleted Book"

                history.append(
                    f"Book: {title}\nStatus: {loan['status']}"
                )

        message = (
            "\n\n".join(history)
            if history
            else "This student has no borrowing history."
        )

        QMessageBox.information(
            self,
            f"Borrowing History - {student['name']}",
            message
        )

    # ---------------- SEARCH BOOKS ----------------

    def search_books(self, text):

        if not hasattr(self, "books_table"):
            return

        self.books_table.setRowCount(0)

        for book in data["books"]:

            searchable = (
                book["title"] + " " + book["author"]
            ).lower()

            if text.lower() not in searchable:
                continue

            row = self.books_table.rowCount()
            self.books_table.insertRow(row)

            values = [
                str(book["id"]),
                book["title"],
                book["author"],
                book["category"],
                str(book["quantity"]),
                str(book["available"])
            ]

            for column, value in enumerate(values):
                self.books_table.setItem(
                    row, column, QTableWidgetItem(value)
                )

    # ---------------- FIND BOOK ----------------

    def find_book(self, book_id):

        for book in data["books"]:
            if book["id"] == book_id:
                return book

        return None

    def selected_book(self):

        row = self.books_table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self, "Selection Required",
                "Please select a book first."
            )
            return None

        book_id = int(self.books_table.item(row, 0).text())
        return self.find_book(book_id)

    # ---------------- ADD BOOK ----------------

    def add_book(self):

        dialog = BookDialog(self)

        if dialog.exec():

            details = dialog.get_data()

            new_id = max(
                (book["id"] for book in data["books"]),
                default=0
            ) + 1

            book = {
                "id": new_id,
                **details,
                "available": details["quantity"]
            }

            data["books"].append(book)

            save_data()
            self.refresh_all()

            QMessageBox.information(
                self, "Success",
                "Book added successfully!"
            )

    # ---------------- EDIT BOOK ----------------

    def edit_book(self):

        book = self.selected_book()

        if not book:
            return

        dialog = BookDialog(self, book)

        if dialog.exec():

            details = dialog.get_data()

            already_issued = (
                book["quantity"] - book["available"]
            )

            if details["quantity"] < already_issued:
                QMessageBox.warning(
                    self, "Invalid Quantity",
                    "Total quantity cannot be less than the "
                    "number of currently issued copies."
                )
                return

            book.update(details)

            book["available"] = (
                details["quantity"] - already_issued
            )

            save_data()
            self.refresh_all()

            QMessageBox.information(
                self, "Updated",
                "Book updated successfully!"
            )

    # ---------------- DELETE BOOK ----------------

    def delete_book(self):

        book = self.selected_book()

        if not book:
            return

        if book["available"] != book["quantity"]:
            QMessageBox.warning(
                self, "Cannot Delete",
                "This book has issued copies. "
                "Return all copies before deleting it."
            )
            return

        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{book['title']}'?"
        )

        if confirm == QMessageBox.StandardButton.Yes:

            data["books"].remove(book)

            save_data()
            self.refresh_all()

            QMessageBox.information(
                self, "Deleted",
                "Book deleted successfully!"
            )

    # ---------------- PROCESS ISSUE ----------------

    def process_issue(self):

        book_id = self.issue_book_combo.currentData()
        student_id = self.issue_student_combo.currentData()

        if book_id is None:
            QMessageBox.warning(
                self, "No Books Available",
                "There are no available books to issue."
            )
            return

        if student_id is None:
            QMessageBox.warning(
                self, "No Students Registered",
                "Please register a student before issuing a book."
            )
            return

        book = self.find_book(book_id)
        student = self.find_student(student_id)

        if not book or book["available"] <= 0:
            QMessageBox.warning(
                self, "Unavailable",
                "This book is no longer available."
            )
            self.show_issue_page()
            return

        if not student:
            QMessageBox.warning(
                self, "Student Not Found",
                "Please select a registered student."
            )
            return

        confirm = QMessageBox.question(
            self, "Confirm Issue",
            f"Issue '{book['title']}' to "
            f"{student['name']} ({student['student_id']})?"
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        book["available"] -= 1

        data["loans"].append({
            "book_id": book_id,
            "student_id": student_id,
            "borrower": student["name"],
            "status": "Issued"
        })

        save_data()
        self.refresh_all()
        self.show_issue_page()

        QMessageBox.information(
            self, "Success",
            "Book issued successfully!"
        )

    # ---------------- PROCESS RETURN ----------------

    def return_book(self):

        row = self.issued_table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self, "Selection Required",
                "Please select an issued book."
            )
            return

        loan_index = self.issued_table.item(
            row, 0
        ).data(Qt.ItemDataRole.UserRole)

        if loan_index is None or loan_index >= len(data["loans"]):
            QMessageBox.warning(
                self, "Error",
                "The selected borrowing record could not be found."
            )
            self.refresh_all()
            return

        loan = data["loans"][loan_index]

        if loan["status"] != "Issued":
            QMessageBox.warning(
                self, "Already Returned",
                "This book has already been returned."
            )
            self.refresh_all()
            return

        borrower = loan.get("borrower", "Unknown")

        confirm = QMessageBox.question(
            self, "Confirm Return",
            f"Confirm return of the book borrowed by {borrower}?"
        )

        if confirm == QMessageBox.StandardButton.Yes:

            loan["status"] = "Returned"

            book = self.find_book(loan["book_id"])

            if book:
                book["available"] += 1

            save_data()
            self.refresh_all()

            QMessageBox.information(
                self, "Success",
                "Book returned successfully!"
            )


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = LibraryManagementSystem()
    window.show()

    sys.exit(app.exec())
