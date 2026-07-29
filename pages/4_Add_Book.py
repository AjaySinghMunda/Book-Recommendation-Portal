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

# ------------------------------------------------
# Title
# ------------------------------------------------
st.title("➕ Add a New Book")

st.write("Fill in the details below to add a book to your personal library.")

st.divider()

# ------------------------------------------------
# Book Details
# ------------------------------------------------
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
        "Adventure"
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

# ------------------------------------------------
# Add Book
# ------------------------------------------------
if st.button(
    "Add Book",
    use_container_width=True
):

    if not title or not author or not description:

        st.error("Please fill all the fields.")

    else:

        books_collection.insert_one({

            "title": title,
            "author": author,
            "genre": genre,
            "publication_year": publication_year,
            "description": description,
            "added_by": st.session_state.user_email

        })

        st.success("Book added successfully!")

        st.balloons()

st.divider()

if st.button(
    "⬅ Back to Dashboard",
    use_container_width=True
):
    st.switch_page("pages/3_Dashboard.py")