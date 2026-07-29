import streamlit as st
import pymongo
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------
# Page Configuration
# ------------------------------------------------
st.set_page_config(
    page_title="My Books",
    page_icon="📖",
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
st.title("📖 My Books")

st.write("View and manage your personal book collection.")

st.divider()

# ------------------------------------------------
# Fetch Books
# ------------------------------------------------
books = list(
    books_collection.find(
        {
            "added_by": st.session_state.user_email
        }
    )
)

# ------------------------------------------------
# No Books
# ------------------------------------------------
if len(books) == 0:

    st.info("No books found.")

    if st.button(
        "➕ Add Your First Book",
        use_container_width=True
    ):
        st.switch_page("pages/4_Add_Book.py")

    st.stop()

# ------------------------------------------------
# Convert to DataFrame
# ------------------------------------------------
df = pd.DataFrame(books)

# Remove MongoDB ObjectId
df = df.drop(columns=["_id"])

# ------------------------------------------------
# Search
# ------------------------------------------------
search = st.text_input(
    "Search by Title or Author"
)

if search:

    df = df[
        df["title"].str.contains(search, case=False) |
        df["author"].str.contains(search, case=False)
    ]

# ------------------------------------------------
# Display Table
# ------------------------------------------------
st.subheader("Book Collection")

st.dataframe(
    df,
    use_container_width=True
)

st.divider()

# ------------------------------------------------
# Genre Chart
# ------------------------------------------------
st.subheader("Books by Genre")

genre_count = df["genre"].value_counts()

fig, ax = plt.subplots()

ax.bar(
    genre_count.index,
    genre_count.values
)

ax.set_xlabel("Genre")
ax.set_ylabel("Number of Books")
ax.set_title("Books by Genre")

plt.xticks(rotation=45)

st.pyplot(fig)

st.divider()

# ------------------------------------------------
# Delete Book
# ------------------------------------------------
st.subheader("Delete a Book")

book_title = st.selectbox(
    "Select Book",
    df["title"]
)

if st.button(
    "Delete Book",
    use_container_width=True
):

    books_collection.delete_one(
        {
            "title": book_title,
            "added_by": st.session_state.user_email
        }
    )

    st.success("Book deleted successfully.")

    st.rerun()

st.divider()

if st.button(
    "⬅ Back to Dashboard",
    use_container_width=True
):
    st.switch_page("pages/3_Dashboard.py")