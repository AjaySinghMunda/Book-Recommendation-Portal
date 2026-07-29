import streamlit as st
import pymongo
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ------------------------------------------------
# Page Configuration
# ------------------------------------------------
st.set_page_config(
    page_title="Recommendations",
    page_icon="🤖",
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
st.title("🤖 Book Recommendations")

st.write("Get AI-powered recommendations based on your library.")

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

if len(books) < 2:
    st.info("Add at least two books to generate recommendations.")
    st.stop()

# ------------------------------------------------
# DataFrame
# ------------------------------------------------
df = pd.DataFrame(books)

# Combine text columns
df["content"] = (
    df["title"] + " " +
    df["author"] + " " +
    df["genre"] + " " +
    df["description"]
)

# ------------------------------------------------
# TF-IDF
# ------------------------------------------------
vectorizer = TfidfVectorizer(stop_words="english")

matrix = vectorizer.fit_transform(df["content"])

similarity = cosine_similarity(matrix)

# ------------------------------------------------
# Select Book
# ------------------------------------------------
selected_book = st.selectbox(
    "Choose a Book",
    df["title"]
)

index = df[df["title"] == selected_book].index[0]

scores = list(enumerate(similarity[index]))

scores = sorted(
    scores,
    key=lambda x: x[1],
    reverse=True
)

st.divider()

st.subheader("Recommended Books")

count = 0

for i, score in scores:

    if i == index:
        continue

    st.success(df.iloc[i]["title"])

    st.write(f"**Author:** {df.iloc[i]['author']}")
    st.write(f"**Genre:** {df.iloc[i]['genre']}")
    st.write(f"**Similarity Score:** {score:.2f}")

    st.write("---")

    count += 1

    if count == 5:
        break

st.divider()

if st.button(
    "⬅ Back to Dashboard",
    use_container_width=True
):
    st.switch_page("pages/3_Dashboard.py")