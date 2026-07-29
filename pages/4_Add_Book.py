import streamlit as st
import pymongo

# ------------------------------------------------
# Page Configuration
# ------------------------------------------------
st.set_page_config(
    page_title="Add Book",
    page_icon="➕",
    layout="centered"
)

# ------------------------------------------------
# Login Check
# ------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.switch_page("pages/2_Login.py")

# ------------------------------------------------
# MongoDB Connection
# ------------------------------------------------
conn = pymongo.MongoClient(st.secrets["MONGO_URI"])

db = conn["BookRecommendationSystem"]

books_collection = db["Books"]
catalog_collection = db["Catalog"]

# ------------------------------------------------
# Title
# ------------------------------------------------
st.title("➕ Add a New Book")

st.write("Choose a book from the catalog or add one manually.")

st.divider()

# ------------------------------------------------
# Add Mode
# ------------------------------------------------
mode = st.radio(
    "How would you like to add a book?",
    [
        "📚 Add from Catalog",
        "✍️ Add Manually"
    ]
)

# ==========================================================
# CATALOG MODE
# ==========================================================
if mode == "📚 Add from Catalog":

    catalog_books = list(
        catalog_collection.find().sort("title", 1)
    )

    if len(catalog_books) == 0:

        st.warning("No books found in the catalog.")

    else:

        title_list = [
            book["title"]
            for book in catalog_books
        ]

        selected_title = st.selectbox(
            "Search or Select a Book",
            title_list,
            index=None,
            placeholder="Choose a book..."
        )

        if selected_title:

            selected_book = next(
                book
                for book in catalog_books
                if book["title"] == selected_title
            )

            st.divider()

            st.subheader(selected_book["title"])

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Author**")
                st.write(selected_book["author"])

                st.write("**Genre**")
                st.write(selected_book["genre"])

            with col2:
                st.write("**Publication Year**")
                st.write(selected_book["publication_year"])

            st.write("**Description**")
            st.info(selected_book["description"])

            st.divider()

            if st.button(
                "📚 Add to My Library",
                use_container_width=True
            ):

                existing_book = books_collection.find_one(
                    {
                        "title": selected_book["title"],
                        "added_by": st.session_state.user_email
                    }
                )

                if existing_book:

                    st.warning(
                        "This book is already in your library."
                    )

                else:

                    new_book = {

                        "title": selected_book["title"],
                        "author": selected_book["author"],
                        "genre": selected_book["genre"],
                        "publication_year": selected_book["publication_year"],
                        "description": selected_book["description"],
                        "added_by": st.session_state.user_email

                    }

                    books_collection.insert_one(new_book)

                    st.success(
                        f"✅ '{selected_book['title']}' has been added to your library."
                    )

                    st.balloons()

# ==========================================================
# PART 2 STARTS HERE
# ==========================================================


# ==========================================================
# MANUAL MODE
# ==========================================================
elif mode == "✍️ Add Manually":

    title = st.text_input(
        "Book Title",
        placeholder="Enter book title"
    )

    author = st.text_input(
        "Author",
        placeholder="Enter author's name"
    )

    genre = st.selectbox(
        "Genre",
        [
            "Fiction",
            "Non-Fiction",
            "Fantasy",
            "Science Fiction",
            "Mystery",
            "Thriller",
            "Romance",
            "Biography",
            "History",
            "Horror",
            "Self Help",
            "Poetry",
            "Adventure",
            "Young Adult",
            "Crime",
            "Political Satire",
            "Memoir",
            "Productivity",
            "Dystopian",
            "Other"
        ]
    )

    publication_year = st.number_input(
        "Publication Year",
        min_value=1000,
        max_value=2100,
        step=1
    )

    description = st.text_area(
        "Description",
        placeholder="Write a short description of the book..."
    )

    st.divider()

    if st.button(
        "➕ Add Book",
        use_container_width=True
    ):

        if (
            not title.strip()
            or not author.strip()
            or not description.strip()
        ):

            st.error("Please fill in all the fields.")

        else:

            existing_book = books_collection.find_one(
                {
                    "title": title.strip(),
                    "added_by": st.session_state.user_email
                }
            )

            if existing_book:

                st.warning(
                    "This book already exists in your library."
                )

            else:

                books_collection.insert_one(
                    {
                        "title": title.strip(),
                        "author": author.strip(),
                        "genre": genre,
                        "publication_year": publication_year,
                        "description": description.strip(),
                        "added_by": st.session_state.user_email
                    }
                )

                st.success(
                    f"✅ '{title}' has been added to your library."
                )

                st.balloons()

# ==========================================================
# Footer
# ==========================================================

st.divider()

if st.button(
    "⬅ Back to Dashboard",
    use_container_width=True
):
    st.switch_page("pages/3_Dashboard.py")