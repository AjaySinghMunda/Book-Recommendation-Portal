import streamlit as st
import pymongo

# ------------------------------------------------
# Page Configuration
# ------------------------------------------------
st.set_page_config(
    page_title="Dashboard",
    page_icon="📚",
    layout="centered"
)

# ------------------------------------------------
# Security Check
# ------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.switch_page("pages/2_Login.py")

# ------------------------------------------------
# MongoDB Connection
# ------------------------------------------------
conn = pymongo.MongoClient(st.secrets["MONGO_URI"])

db = conn["BookRecommendationSystem"]

users_collection = db["Users"]
books_collection = db["Books"]

# ------------------------------------------------
# Statistics
# ------------------------------------------------
book_count = books_collection.count_documents(
    {
        "added_by": st.session_state.user_email
    }
)

# ------------------------------------------------
# Dashboard
# ------------------------------------------------
st.title("📚 Dashboard")

st.success(
    f"Welcome, {st.session_state.user_name}!"
)

st.divider()

st.metric(
    label="Books Added",
    value=book_count
)

st.info(
    f"Logged in as: {st.session_state.user_email}"
)

st.divider()

st.subheader("Quick Navigation")

if st.button(
    "➕ Add Book",
    use_container_width=True
):
    st.switch_page("pages/4_Add_Book.py")

if st.button(
    "📖 My Books",
    use_container_width=True
):
    st.switch_page("pages/5_My_Books.py")

if st.button(
    "🤖 Recommendations",
    use_container_width=True
):
    st.switch_page("pages/6_Recommendations.py")

if st.button(
    "👤 Profile",
    use_container_width=True
):
    st.switch_page("pages/7_Profile.py")

st.divider()

if st.button(
    "🚪 Logout",
    use_container_width=True
):

    st.session_state.logged_in = False

    st.session_state.pop("user_name", None)
    st.session_state.pop("user_email", None)

    st.success("Logged out successfully.")

    st.switch_page("Home.py")
