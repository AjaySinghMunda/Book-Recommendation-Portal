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
# Library Statistics
# ------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📚 Books",
        len(df)
    )

with col2:
    st.metric(
        "🏷 Genres",
        df["genre"].nunique()
    )

with col3:
    st.metric(
        "📅 Oldest",
        int(df["publication_year"].min())
    )

with col4:
    st.metric(
        "🆕 Newest",
        int(df["publication_year"].max())
    )

st.divider()

# ------------------------------------------------
# Search & Filter
# ------------------------------------------------
left, right = st.columns([2,1])

with left:

    search = st.text_input(
        "🔍 Search Books",
        placeholder="Search by title or author..."
    )

with right:

    genres = ["All"] + sorted(df["genre"].unique().tolist())

    selected_genre = st.selectbox(
        "Genre",
        genres
    )

# ------------------------------------------------
# Apply Search
# ------------------------------------------------
if search:

    df = df[
        df["title"].str.contains(search, case=False, na=False)
        |
        df["author"].str.contains(search, case=False, na=False)
    ]

# ------------------------------------------------
# Apply Genre Filter
# ------------------------------------------------
if selected_genre != "All":

    df = df[
        df["genre"] == selected_genre
    ]

st.divider()

# ------------------------------------------------
# Sorting
# ------------------------------------------------
sort_option = st.selectbox(
    "Sort By",
    [
        "Title (A-Z)",
        "Publication Year (Newest)",
        "Publication Year (Oldest)"
    ]
)

if sort_option == "Title (A-Z)":
    df = df.sort_values(
        by="title"
    )

elif sort_option == "Publication Year (Newest)":
    df = df.sort_values(
        by="publication_year",
        ascending=False
    )

elif sort_option == "Publication Year (Oldest)":
    df = df.sort_values(
        by="publication_year"
    )

# ------------------------------------------------
# Display Table
# ------------------------------------------------
st.subheader("📚 My Collection")

for _, book in df.iterrows():

    with st.container(border=True):

        st.markdown(
            f"### 📖 {book['title']}"
        )

        st.write(
            f"**👤 Author:** {book['author']}"
        )

        st.write(
            f"**🏷 Genre:** {book['genre']}"
        )

        st.write(
            f"**📅 Publication Year:** {book['publication_year']}"
        )

        st.write(book["description"])

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "✏ Edit",
                key=f"edit_{book['_id']}",
                use_container_width=True
            ):

                st.session_state.edit_book = str(book["_id"])

                st.switch_page("pages/6_Edit_Book.py")

        with col2:

            if st.button(
                "🗑 Delete",
                key=f"delete_{book['_id']}",
                use_container_width=True
            ):

                books_collection.delete_one(
                    {
                        "_id": book["_id"]
                    }
                )

                st.success("Book deleted successfully.")

                st.rerun()

        st.divider()

# ------------------------------------------------
# Genre Chart
# ------------------------------------------------

st.header("📊 Library Analytics")
genre_count = (
    df["genre"]
    .value_counts()
)

fig, ax = plt.subplots(figsize=(8,4))

ax.barh(
    genre_count.index,
    genre_count.values
)

ax.set_title("Books by Genre")

ax.set_xlabel("Number of Books")

st.pyplot(fig)

year_count = (
    df["publication_year"]
    .value_counts()
    .sort_index()
)

fig, ax = plt.subplots(figsize=(8,4))

ax.plot(
    year_count.index,
    year_count.values,
    marker="o"
)

ax.set_title("Publication Year Distribution")

ax.set_xlabel("Publication Year")

ax.set_ylabel("Books")

st.pyplot(fig)

st.divider()



st.divider()

if st.button(
    "⬅ Back to Dashboard",
    use_container_width=True
):
    st.switch_page("pages/3_Dashboard.py")