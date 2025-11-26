class Book:
    def __init__(self, title, author, year):
        self.__title = title
        self.__author = author
        self.__year = year
        self.__available = True

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_year(self):
        return self.__year

    def is_available(self):
        return self.__available

    def mark_as_taken(self):
        self.__available = False

    def mark_as_returned(self):
        self.__available = True

    def __str__(self):
        return f"{self.__title} by {self.__author} ({self.__year})"

class PrintedBook(Book):
    def __init__(self, title, author, year, pages, condition):
        super().__init__(title, author, year)
        self.pages = pages
        self.condition = condition  # "новая", "хорошая", "плохая"

    def repair(self):
        if self.condition == "плохая":
            self.condition = "хорошая"
        elif self.condition == "хорошая":
            self.condition = "новая"
        # If condition is already "новая", do nothing

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}, {self.pages} pages, condition: {self.condition}"

class EBook(Book):
    def __init__(self, title, author, year, file_size, format_):
        super().__init__(title, author, year)
        self.file_size = file_size  # in MB
        self.format = format_

    def download(self):
        print(f"Downloading {self.get_title()} in {self.format} format...")

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}, {self.file_size}MB, format: {self.format}"

class User:
    def __init__(self, name):
        self.name = name
        self.__borrowed_books = []

    def borrow(self, book):
        if book.is_available():
            book.mark_as_taken()
            self.__borrowed_books.append(book)
            print(f"{self.name} borrowed {book.get_title()}.")
        else:
            print(f"Sorry, {book.get_title()} is currently unavailable.")

    def return_book(self, book):
        if book in self.__borrowed_books:
            book.mark_as_returned()
            self.__borrowed_books.remove(book)
            print(f"{self.name} returned {book.get_title()}.")
        else:
            print(f"{self.name} doesn't have {book.get_title()}.")

    def show_books(self):
        if self.__borrowed_books:
            print(f"{self.name} has borrowed these books:")
            for book in self.__borrowed_books:
                print(f" - {book}")
        else:
            print(f"{self.name} has not borrowed any books.")

    def get_borrowed_books(self):
        return self.__borrowed_books

class Librarian(User):
    def add_book(self, library, book):
        library.add_book(book)
        print(f"Librarian {self.name} added {book.get_title()}.")

    def remove_book(self, library, title):
        library.remove_book(title)
        print(f"Librarian {self.name} removed {title}.")

    def register_user(self, library, user):
        library.add_user(user)
        print(f"Librarian {self.name} registered user {user.name}.")

class Library:
    def __init__(self):
        self.__books = []
        self.__users = []

    def add_book(self, book):
        self.__books.append(book)

    def remove_book(self, title):
        for book in self.__books:
            if book.get_title() == title:
                self.__books.remove(book)
                return
        print(f"Book titled '{title}' not found.")

    def add_user(self, user):
        self.__users.append(user)

    def find_book(self, title):
        for book in self.__books:
            if book.get_title() == title:
                return book
        return None

    def show_all_books(self):
        if not self.__books:
            print("No books available in the library.")
        else:
            for book in self.__books:
                print(book)

    def show_available_books(self):
        available_books = [book for book in self.__books if book.is_available()]
        if not available_books:
            print("No available books found.")
        else:
            for book in available_books:
                print(book)

    def lend_book(self, title, user_name):
        book = self.find_book(title)
        if not book:
            print(f"Book '{title}' not found in the library.")
            return

        if not book.is_available():
            print(f"Book '{title}' is currently not available.")
            return

        for user in self.__users:
            if user.name == user_name:
                user.borrow(book)
                return

        print(f"User '{user_name}' not found.")

    def return_book(self, title, user_name):
        for user in self.__users:
            if user.name == user_name:
                book = self.find_book(title)
                if book and book in user.get_borrowed_books():
                    user.return_book(book)
                    return
                print(f"{user_name} does not have the book '{title}'.")
                return
        print(f"User '{user_name}' not found.")


if __name__ == '__main__':
    lib = Library()

    # --- создаём книги ---
    b1 = PrintedBook("Война и мир", "Толстой", 1869, 1225, "хорошая")
    b2 = EBook("Мастер и Маргарита", "Булгаков", 1966, 5, "epub")
    b3 = PrintedBook("Преступление и наказание", "Достоевский", 1866, 480, "плохая")

    # --- создаём пользователей ---
    user1 = User("Анна")
    librarian = Librarian("Мария")

    # --- библиотекарь добавляет книги ---
    librarian.add_book(lib, b1)
    librarian.add_book(lib, b2)
    librarian.add_book(lib, b3)

    # --- библиотекарь регистрирует пользователя ---
    librarian.register_user(lib, user1)

    # --- пользователь берёт книгу ---
    lib.lend_book("Война и мир", "Анна")

    # --- пользователь смотрит свои книги ---
    user1.show_books()

    # --- пользователь возвращает книгу ---
    lib.return_book("Война и мир", "Анна")

    # --- электронная книга ---
    b2.download()

    # --- ремонт книги ---
    b3.repair()
    print(b3)
