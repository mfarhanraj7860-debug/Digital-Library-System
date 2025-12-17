import streamlit as st

class Book:
    def __init__(self, title, author, book_id, total_copies):
        self.title = title
        self.author = author
        self.book_id = book_id
        self.total_copies = total_copies
        self.available_copies = total_copies

    def borrow(self):
        if self.available_copies > 0:
            self.available_copies -= 1
            return True
        return False

    def return_book(self):
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            return True
        return False

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book_id):
        self.borrowed_books.append(book_id)

    def return_book(self, book_id):
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def search_by_author(self, author):
        return [b for b in self.books if author.lower() in b.author.lower()]

    def get_book_by_id(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None



if "library" not in st.session_state:
    st.session_state.library = Library()
    # Sample books
    st.session_state.library.add_book(Book("Python Basics", "John Doe", "101", 3))
    st.session_state.library.add_book(Book("AI Fundamentals", "Andrew Ng", "102", 2))
    st.session_state.library.add_book(Book("Data Science", "Jane Smith", "103", 1))

if "user" not in st.session_state:
    st.session_state.user = User(1, "Guest User")

# ______________________
# STREAMLIT UI
# ______________________

st.title("📚 Digital Library System")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Search Book by Author",
        "Borrow Book",
        "Return Book",
        "Check Book Availability"
    ]
)

if menu == "Search Book by Author":
    st.subheader("🔍 Search Book by Author")
    author = st.text_input("Enter author name")
    if st.button("Search"):
        results = st.session_state.library.search_by_author(author)
        if results:
            for book in results:
                st.write(f"{book.title} by {book.author} (ID: {book.book_id})")
        else:
            st.warning("No book found")

elif menu == "Borrow Book":
    st.subheader("📕 Borrow Book")
    book_id = st.text_input("Enter Book ID")
    if st.button("Borrow"):
        book = st.session_state.library.get_book_by_id(book_id)
        if book and book.borrow():
            st.session_state.user.borrow_book(book_id)
            st.success(f"Book '{book.title}' borrowed successfully!")
        else:
            st.error("Book not available or invalid ID")

elif menu == "Return Book":
    st.subheader("📗 Return Book")
    book_id = st.text_input("Enter Book ID")
    if st.button("Return"):
        book = st.session_state.library.get_book_by_id(book_id)
        if book and book.return_book():
            st.session_state.user.return_book(book_id)
            st.success(f"Book '{book.title}' returned successfully!")
        else:
            st.error("Invalid return request")

elif menu == "Check Book Availability":
    st.subheader("✅ Check Book Availability")
    book_id = st.text_input("Enter Book ID")
    if st.button("Check"):
        book = st.session_state.library.get_book_by_id(book_id)
        if book:
            st.info(f"Available Copies: {book.available_copies} / {book.total_copies}")
        else:
            st.error("Book not found")
