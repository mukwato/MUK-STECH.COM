"""
====================================================================
        LIBRARY ANALYTICS & DATA MANAGEMENT SYSTEM
                    PYTHON PROGRAMMING 2026
====================================================================

SYSTEM FEATURES
--------------------------------------------------------------------
1. User Authentication
2. SHA-256 Password Hashing
3. Role-Based Access Control
4. Admin and Member Roles
5. Library Book Management
6. CRUD Operations:
      - Create
      - Read
      - Update
      - Delete
7. Automatic 500+ Record Dataset
8. CSV Data Storage
9. Linear Search Algorithm
10. Priority Ranking Algorithm
11. Content-Based Similarity Recommendation Algorithm
12. Abstraction
13. Inheritance
14. Polymorphism
15. Encapsulation
16. Composition
17. Data Validation
18. Exception Handling
19. System Activity Logging
20. Matplotlib Data Visualization
21. PDF Report Generation
22. Tkinter Graphical User Interface
23. Dashboard Statistics
24. Search by ID, Title, Author and Category
25. Professional User Interface
====================================================================
"""

# ================================================================
# IMPORT LIBRARIES
# ================================================================

import os
import csv
import json
import random
import logging
import hashlib
import tkinter as tk

from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
from datetime import datetime

import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# ================================================================
# LOGGING CONFIGURATION
# ================================================================

logging.basicConfig(
    filename="system_activity.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ================================================================
# 1. ABSTRACTION
# ================================================================

class LibraryItem(ABC):
    """
    Abstract Base Class.

    This class demonstrates ABSTRACTION.

    It represents the general concept of an item in a library.
    Subclasses must implement the abstract methods.
    """

    def __init__(self, item_id, title, category):

        self._item_id = item_id
        self._title = title
        self._category = category

    # ------------------------------------------------------------
    # ENCAPSULATION USING PROPERTIES
    # ------------------------------------------------------------

    @property
    def item_id(self):
        return self._item_id

    @property
    def title(self):
        return self._title

    @property
    def category(self):
        return self._category

    @abstractmethod
    def get_item_type(self):
        """
        Abstract method.

        Every child class must implement this method.
        """
        pass

    @abstractmethod
    def get_details(self):
        """
        Abstract method for displaying item information.
        """
        pass
# ================================================================
# 2. INHERITANCE & POLYMORPHISM
# ================================================================

class Book(LibraryItem):
    """
    Book inherits from LibraryItem.

    Demonstrates:
    - INHERITANCE
    - POLYMORPHISM
    - ENCAPSULATION
    """

    def __init__(
        self,
        item_id,
        title,
        category,
        author,
        borrow_count,
        rating,
        date_added
    ):

        # Call parent constructor
        super().__init__(
            item_id,
            title,
            category
        )

        self.author = author
        self.borrow_count = int(borrow_count)
        self.rating = float(rating)
        self.date_added = date_added

    # ------------------------------------------------------------
    # POLYMORPHISM
    # ------------------------------------------------------------

    def get_item_type(self):

        return "Book"

    def get_details(self):

        return (
            f"ID: {self.item_id}\n"
            f"Title: {self.title}\n"
            f"Category: {self.category}\n"
            f"Author: {self.author}\n"
            f"Borrow Count: {self.borrow_count}\n"
            f"Rating: {self.rating:.1f}/5.0\n"
            f"Date Added: {self.date_added}"
        )


# ================================================================
# 3. USER CLASS
# ================================================================

class User:
    """
    Represents a system user.
    """

    def __init__(
        self,
        username,
        password_hash,
        role
    ):

        self.username = username
        self.password_hash = password_hash
        self.role = role


# ================================================================
# 4. AUTHENTICATION MANAGER
# ================================================================

class AuthManager:
    """
    Manages:
    - User registration
    - Login
    - Password hashing
    - User storage
    """

    def __init__(
        self,
        user_file="users.json"
    ):

        self.user_file = user_file
        self.users = {}

        self.load_users()

    # ------------------------------------------------------------
    # SHA-256 PASSWORD HASHING
    # ------------------------------------------------------------

    def _hash_password(self, password):

        return hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

    # ------------------------------------------------------------
    # LOAD USERS
    # ------------------------------------------------------------

    def load_users(self):

        try:

            if not os.path.exists(
                self.user_file
            ):

                # Create default administrator
                self.users["admin"] = User(
                    "admin",
                    self._hash_password(
                        "admin123"
                    ),
                    "Admin"
                )

                self.save_users()

                logging.info(
                    "Default administrator account created."
                )

                return

            with open(
                self.user_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            for username, user_data in data.items():

                self.users[username] = User(
                    username,
                    user_data["hash"],
                    user_data["role"]
                )

            # Make sure an admin account always exists
            if "admin" not in self.users:

                self.users["admin"] = User(
                    "admin",
                    self._hash_password(
                        "admin123"
                    ),
                    "Admin"
                )

                self.save_users()

        except (
            json.JSONDecodeError,
            KeyError,
            OSError
        ) as error:

            logging.error(
                f"Error loading users: {error}"
            )

            self.users = {}

            self.users["admin"] = User(
                "admin",
                self._hash_password(
                    "admin123"
                ),
                "Admin"
            )

            self.save_users()

    # ------------------------------------------------------------
    # SAVE USERS
    # ------------------------------------------------------------

    def save_users(self):

        try:

            data = {}

            for user in self.users.values():

                data[user.username] = {
                    "hash": user.password_hash,
                    "role": user.role
                }

            with open(
                self.user_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
                )

        except OSError as error:

            logging.error(
                f"Error saving users: {error}"
            )

    # ------------------------------------------------------------
    # REGISTER USER
    # ------------------------------------------------------------

    def register_user(
        self,
        username,
        password,
        role="Member"
    ):

        username = username.strip()

        if not username:

            return False, "Username is required."

        if not password:

            return False, "Password is required."

        if username in self.users:

            logging.warning(
                f"Registration failed: "
                f"{username} already exists."
            )

            return (
                False,
                "Username already exists."
            )

        if role not in [
            "Admin",
            "Member"
        ]:

            role = "Member"

        password_hash = (
            self._hash_password(password)
        )

        self.users[username] = User(
            username,
            password_hash,
            role
        )

        self.save_users()

        logging.info(
            f"New user registered: "
            f"{username} ({role})"
        )

        return (
            True,
            "User registered successfully."
        )

    # ------------------------------------------------------------
    # LOGIN
    # ------------------------------------------------------------

    def login(
        self,
        username,
        password
    ):

        username = username.strip()

        password_hash = (
            self._hash_password(password)
        )

        if (
            username in self.users
            and
            self.users[username].password_hash
            == password_hash
        ):

            logging.info(
                f"Successful login: {username}"
            )

            return (
                True,
                self.users[username]
            )

        logging.warning(
            f"Failed login attempt: {username}"
        )

        return False, None

# ================================================================
# 5. LIBRARY DATA ENGINE
# ================================================================

class LibraryDataEngine:
    """
    Main library data management class.

    Demonstrates COMPOSITION because this class manages
    a collection of Book objects.

    Responsibilities:
    - Generate dataset
    - Load dataset
    - Save dataset
    - Add books
    - Update books
    - Delete books
    - Search books
    - Ranking
    - Recommendations
    """

    def __init__(
        self,
        csv_file="library_dataset.csv"
    ):

        self.csv_file = csv_file

        # Composition:
        # LibraryDataEngine contains Book objects
        self.dataset = []

        self.ensure_dataset_exists()
        self.load_data()

    # ============================================================
    # CREATE 500 RECORD DATASET
    # ============================================================

    def ensure_dataset_exists(self):

        if os.path.exists(
            self.csv_file
        ):

            return

        categories = [
            "Fiction",
            "Technology",
            "Science",
            "History",
            "Biography",
            "Education",
            "Business",
            "Programming"
        ]

        authors = [
            "Alice Smith",
            "Bob Jones",
            "Charlie Brown",
            "Diana Prince",
            "Evan Wright",
            "Grace Miller",
            "James Wilson",
            "Linda Taylor",
            "Michael Johnson",
            "Sarah Williams"
        ]

        try:

            with open(
                self.csv_file,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "ID",
                    "Title",
                    "Category",
                    "Author",
                    "BorrowCount",
                    "Rating",
                    "DateAdded"
                ])

                for i in range(
                    1,
                    501
                ):

                    book_id = (
                        f"B{i:04d}"
                    )

                    title = (
                        f"Book Title Volume {i}"
                    )

                    category = random.choice(
                        categories
                    )

                    author = random.choice(
                        authors
                    )

                    borrow_count = random.randint(
                        0,
                        300
                    )

                    rating = round(
                        random.uniform(
                            1.0,
                            5.0
                        ),
                        1
                    )

                    date_added = (
                        f"2025-"
                        f"{random.randint(1,12):02d}-"
                        f"{random.randint(1,28):02d}"
                    )

                    writer.writerow([
                        book_id,
                        title,
                        category,
                        author,
                        borrow_count,
                        rating,
                        date_added
                    ])

            logging.info(
                "500 library records generated."
            )

        except OSError as error:

            logging.error(
                f"Dataset creation failed: {error}"
            )

    # ============================================================
    # LOAD DATA
    # ============================================================

    def load_data(self):

        self.dataset = []

        try:

            with open(
                self.csv_file,
                "r",
                encoding="utf-8"
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:

                    try:

                        book = Book(
                            row["ID"],
                            row["Title"],
                            row["Category"],
                            row["Author"],
                            row["BorrowCount"],
                            row["Rating"],
                            row["DateAdded"]
                        )

                        self.dataset.append(
                            book
                        )

                    except (
                        ValueError,
                        KeyError
                    ) as error:

                        logging.warning(
                            f"Skipped invalid record: "
                            f"{error}"
                        )

            logging.info(
                f"{len(self.dataset)} "
                f"library records loaded."
            )

        except (
            OSError,
            csv.Error
        ) as error:

            logging.error(
                f"Error loading dataset: {error}"
            )

    # ============================================================
    # SAVE DATA
    # ============================================================

    def save_data(self):

        try:

            with open(
                self.csv_file,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "ID",
                    "Title",
                    "Category",
                    "Author",
                    "BorrowCount",
                    "Rating",
                    "DateAdded"
                ])

                for book in self.dataset:

                    writer.writerow([
                        book.item_id,
                        book.title,
                        book.category,
                        book.author,
                        book.borrow_count,
                        book.rating,
                        book.date_added
                    ])

            logging.info(
                "Library dataset saved."
            )

            return True

        except OSError as error:

            logging.error(
                f"Error saving dataset: {error}"
            )

            return False

    # ============================================================
    # FIND BOOK BY ID
    # ============================================================

    def find_by_id(
        self,
        item_id
    ):

        item_id = item_id.strip().lower()

        for book in self.dataset:

            if (
                book.item_id.lower()
                == item_id
            ):

                return book

        return None

    # ============================================================
    # ADD BOOK
    # ============================================================

    def add_book(
        self,
        item_id,
        title,
        category,
        author,
        borrow_count,
        rating,
        date_added
    ):

        item_id = item_id.strip()
        title = title.strip()
        category = category.strip()
        author = author.strip()

        # --------------------------------------------------------
        # VALIDATION
        # --------------------------------------------------------

        if not item_id:

            return (
                False,
                "Book ID is required."
            )

        if not title:

            return (
                False,
                "Book title is required."
            )

        if not category:

            return (
                False,
                "Book category is required."
            )

        if not author:

            return (
                False,
                "Book author is required."
            )

        # Duplicate check
        if self.find_by_id(item_id):

            return (
                False,
                "A book with this ID already exists."
            )

        # Numerical validation
        try:

            borrow_count = int(
                borrow_count
            )

            rating = float(
                rating
            )

        except ValueError:

            return (
                False,
                "Borrow Count must be an integer "
                "and Rating must be a number."
            )

        if borrow_count < 0:

            return (
                False,
                "Borrow Count cannot be negative."
            )

        if not (
            0 <= rating <= 5
        ):

            return (
                False,
                "Rating must be between 0 and 5."
            )

        # --------------------------------------------------------
        # CREATE BOOK OBJECT
        # --------------------------------------------------------

        new_book = Book(
            item_id,
            title,
            category,
            author,
            borrow_count,
            rating,
            date_added
        )

        # Add to memory
        self.dataset.append(
            new_book
        )

        # Save to CSV
        if not self.save_data():

            # Roll back if saving failed
            self.dataset.remove(
                new_book
            )

            return (
                False,
                "Unable to save the book to the database."
            )

        logging.info(
            f"Book added successfully: {item_id}")
     
