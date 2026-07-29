import streamlit as st
import pymongo
from bson import ObjectId

# ------------------------------------------------
# Page Configuration
# ------------------------------------------------
st.set_page_config(
    page_title="Edit Book",
    page_icon="✏",
    layout="centered"
)

# ------------------------------------------------
# Login Check
# ------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.switch_page("pages/2_Login.py")

# ------------------------------------------------
# Check Selected Book
# ------------------------------------------------
if "edit_book" not in st.session_state:
    st.error("No book selected.")
    st.switch_page("pages/5_My_Books.py")

# ------------------------------------------------
# MongoDB
# ------------------------------------------------
conn = pymongo.MongoClient(st.secrets["MONGO_URI"])

db = conn["BookRecommendationSystem"]

books_collection = db["Books"]


book = books_collection.find_one(
    {
        "_id": ObjectId(st.session_state.edit_book),
        "added_by": st.session_state.user_email
    }
)

if not book:
    st.error("Book not found.")
    st.switch_page("pages/5_My_Books.py")
    
st.title("✏ Edit Book")

st.write("Update the details of your book.")

st.divider()


genres = [
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

title = st.text_input(
    "Title",
    value=book["title"]
)

author = st.text_input(
    "Author",
    value=book["author"]
)

genre = st.selectbox(
    "Genre",
    genres,
    index=genres.index(book["genre"])
)

publication_year = st.number_input(
    "Publication Year",
    min_value=1000,
    max_value=2100,
    value=int(book["publication_year"])
)

description = st.text_area(
    "Description",
    value=book["description"],
    height=180
)

if st.button(
    "💾 Save Changes",
    use_container_width=True
):

    if (
        not title.strip()
        or not author.strip()
        or not description.strip()
    ):
        st.error("Please fill all fields.")

    else:

        books_collection.update_one(
            {
                "_id": ObjectId(st.session_state.edit_book)
            },
            {
                "$set": {
                    "title": title.strip(),
                    "author": author.strip(),
                    "genre": genre,
                    "publication_year": int(publication_year),
                    "description": description.strip()
                }
            }
        )

        st.success("Book updated successfully!")

        st.switch_page("pages/5_My_Books.py")
        
        
if st.button(
    "⬅ Back",
    use_container_width=True
):
    st.switch_page("pages/5_My_Books.py")