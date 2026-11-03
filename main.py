import streamlit as st
import json
import random
import string
from pathlib import Path
from datetime import datetime


# =========================
# LIBRARY CLASS
# =========================

class Library:

    database = "library.json"
    data = {"Books": [], "Members": []}

    # Load existing data
    if Path(database).exists():
        try:
            with open(database, "r") as fs:
                content = fs.read().strip()

                if content:
                    data = json.loads(content)
        except json.JSONDecodeError:
            data = {"Books": [], "Members": []}

    else:
        with open(database, "w") as fs:
            json.dump(data, fs, indent=4)

    @staticmethod
    def gen_id(prefix="B"):
        random_id = ""

        for i in range(5):
            random_id += random.choice(
                string.ascii_uppercase + string.digits
            )

        return prefix + "-" + random_id

    @classmethod
    def save_data(cls):
        with open(cls.database, "w") as fs:
            json.dump(cls.data, fs, indent=4, default=str)

    # =========================
    # ADD BOOK
    # =========================

    @classmethod
    def add_book(cls, title, author, copies):

        book = {
            "id": cls.gen_id(),
            "title": title,
            "author": author,
            "total_copy": copies,
            "avalabe_copies": copies,
            "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        cls.data["Books"].append(book)
        cls.save_data()

    # =========================
    # ADD MEMBER
    # =========================

    @classmethod
    def add_member(cls, name, email):

        member = {
            "id": cls.gen_id("M"),
            "name": name,
            "email": email,
            "borowed": []
        }

        cls.data["Members"].append(member)
        cls.save_data()

    # =========================
    # BORROW BOOK
    # =========================

    @classmethod
    def borrow_book(cls, member_id, book_id):

        members = [
            m for m in cls.data["Members"]
            if m["id"] == member_id
        ]

        if not members:
            return False, "Member ID does not exist."

        books = [
            b for b in cls.data["Books"]
            if b["id"] == book_id
        ]

        if not books:
            return False, "Book ID does not exist."

        member = members[0]
        book = books[0]

        if book["avalabe_copies"] <= 0:
            return False, "No available copies."

        borrow_entry = {
            "book_id": book["id"],
            "title": book["title"],
            "borrow_on": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        member["borowed"].append(borrow_entry)

        book["avalabe_copies"] -= 1

        cls.save_data()

        return True, "Book borrowed successfully."

    # =========================
    # RETURN BOOK
    # =========================

    @classmethod
    def return_book(cls, member_id, book_id):

        members = [
            m for m in cls.data["Members"]
            if m["id"] == member_id
        ]

        if not members:
            return False, "Member ID does not exist."

        member = members[0]

        borrowed = [
            b for b in member["borowed"]
            if b["book_id"] == book_id
        ]

        if not borrowed:
            return False, "This book is not borrowed by this member."

        member["borowed"].remove(borrowed[0])

        books = [
            b for b in cls.data["Books"]
            if b["id"] == book_id
        ]

        if books:
            books[0]["avalabe_copies"] += 1

        cls.save_data()

        return True, "Book returned successfully."


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)


# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.title {
    font-size: 38px;
    font-weight: 700;
    color: #1f2937;
}

.subtitle {
    color: #6b7280;
    font-size: 17px;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

.metric-title {
    color: #6b7280;
    font-size: 15px;
}

.metric-value {
    font-size: 30px;
    font-weight: 700;
    color: #111827;
}

.sidebar-title {
    font-size: 25px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# =========================
# SIDEBAR
# =========================

st.sidebar.markdown(
    '<div class="sidebar-title">📚 My Library</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "➕ Add Book",
        "📚 Books",
        "👤 Add Member",
        "👥 Members",
        "📖 Borrow Book",
        "↩️ Return Book"
    ]
)


# =========================
# DATA
# =========================

books = Library.data["Books"]
members = Library.data["Members"]

total_books = len(books)
total_members = len(members)

total_copies = sum(
    book["total_copy"] for book in books
)

available_copies = sum(
    book["avalabe_copies"] for book in books
)

borrowed_copies = total_copies - available_copies


# =========================
# DASHBOARD
# =========================

if menu == "🏠 Dashboard":

    st.markdown(
        '<div class="title">Library Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Manage your books and members easily.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📚 Total Books",
            total_books
        )

    with col2:
        st.metric(
            "📦 Total Copies",
            total_copies
        )

    with col3:
        st.metric(
            "👥 Members",
            total_members
        )

    with col4:
        st.metric(
            "📖 Borrowed",
            borrowed_copies
        )

    st.write("")

    st.subheader("📊 Library Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.write("Available Copies")

        st.progress(
            available_copies / total_copies
            if total_copies > 0
            else 0
        )

        st.write(
            f"{available_copies} copies available"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.write("Borrowed Copies")

        st.progress(
            borrowed_copies / total_copies
            if total_copies > 0
            else 0
        )

        st.write(
            f"{borrowed_copies} copies borrowed"
        )

        st.markdown("</div>", unsafe_allow_html=True)


# =========================
# ADD BOOK
# =========================

elif menu == "➕ Add Book":

    st.title("➕ Add New Book")

    with st.form("add_book_form"):

        title = st.text_input(
            "Book Title"
        )

        author = st.text_input(
            "Author Name"
        )

        copies = st.number_input(
            "Number of Copies",
            min_value=1,
            value=1,
            step=1
        )

        submit = st.form_submit_button(
            "Add Book"
        )

        if submit:

            if not title or not author:
                st.error(
                    "Please enter title and author."
                )

            else:

                Library.add_book(
                    title,
                    author,
                    copies
                )

                st.success(
                    "Book added successfully!"
                )

                st.rerun()


# =========================
# BOOK LIST
# =========================

elif menu == "📚 Books":

    st.title("📚 All Books")

    if not books:

        st.info("No books found.")

    else:

        for book in books:

            with st.container(border=True):

                col1, col2, col3, col4 = st.columns(
                    [2, 4, 3, 2]
                )

                with col1:
                    st.write(
                        f"**{book['id']}**"
                    )

                with col2:
                    st.write(
                        f"**{book['title']}**"
                    )
                    st.caption(
                        book["author"]
                    )

                with col3:
                    st.write(
                        f"Total: {book['total_copy']}"
                    )

                    st.write(
                        f"Available: {book['avalabe_copies']}"
                    )

                with col4:

                    if book["avalabe_copies"] > 0:
                        st.success("Available")
                    else:
                        st.error("Unavailable")


# =========================
# ADD MEMBER
# =========================

elif menu == "👤 Add Member":

    st.title("👤 Add New Member")

    with st.form("member_form"):

        name = st.text_input(
            "Member Name"
        )

        email = st.text_input(
            "Email Address"
        )

        submit = st.form_submit_button(
            "Add Member"
        )

        if submit:

            if not name or not email:

                st.error(
                    "Please enter all details."
                )

            else:

                Library.add_member(
                    name,
                    email
                )

                st.success(
                    "Member added successfully!"
                )

                st.rerun()


# =========================
# MEMBER LIST
# =========================

elif menu == "👥 Members":

    st.title("👥 Library Members")

    if not members:

        st.info("No members found.")

    else:

        for member in members:

            with st.container(border=True):

                col1, col2, col3, col4 = st.columns(
                    [2, 3, 4, 2]
                )

                with col1:
                    st.write(
                        f"**{member['id']}**"
                    )

                with col2:
                    st.write(
                        f"**{member['name']}**"
                    )

                with col3:
                    st.write(
                        member["email"]
                    )

                with col4:
                    st.write(
                        f"Borrowed: {len(member['borowed'])}"
                    )


# =========================
# BORROW BOOK
# =========================

elif menu == "📖 Borrow Book":

    st.title("📖 Borrow Book")

    if not members:

        st.warning(
            "Please add a member first."
        )

    elif not books:

        st.warning(
            "Please add a book first."
        )

    else:

        member_options = {
            f"{m['name']} ({m['id']})": m["id"]
            for m in members
        }

        book_options = {
            f"{b['title']} ({b['id']})": b["id"]
            for b in books
            if b["avalabe_copies"] > 0
        }

        if not book_options:

            st.warning(
                "No books are currently available."
            )

        else:

            selected_member = st.selectbox(
                "Select Member",
                list(member_options.keys())
            )

            selected_book = st.selectbox(
                "Select Book",
                list(book_options.keys())
            )

            if st.button(
                "📖 Borrow Book",
                type="primary"
            ):

                success, message = Library.borrow_book(
                    member_options[selected_member],
                    book_options[selected_book]
                )

                if success:
                    st.success(message)
                    st.rerun()

                else:
                    st.error(message)


# =========================
# RETURN BOOK
# =========================

elif menu == "↩️ Return Book":

    st.title("↩️ Return Book")

    member_options = {
        f"{m['name']} ({m['id']})": m["id"]
        for m in members
        if m["borowed"]
    }

    if not member_options:

        st.info(
            "No member currently has borrowed books."
        )

    else:

        selected_member = st.selectbox(
            "Select Member",
            list(member_options.keys())
        )

        member_id = member_options[
            selected_member
        ]

        member = next(
            m for m in members
            if m["id"] == member_id
        )

        borrowed_books = {
            f"{b['title']} ({b['book_id']})":
            b["book_id"]
            for b in member["borowed"]
        }

        selected_book = st.selectbox(
            "Select Book",
            list(borrowed_books.keys())
        )

        if st.button(
            "↩️ Return Book",
            type="primary"
        ):

            success, message = Library.return_book(
                member_id,
                borrowed_books[selected_book]
            )

            if success:
                st.success(message)
                st.rerun()

            else:
                st.error(message)