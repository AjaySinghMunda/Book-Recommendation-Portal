import streamlit as st
import pymongo
import numpy as np

# ------------------------------------------------
# Page Configuration
# ------------------------------------------------
st.set_page_config(
    page_title="Profile",
    page_icon="👤",
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

users_collection = db["Users"]
books_collection = db["Books"]

# ------------------------------------------------
# Fetch User
# ------------------------------------------------
user = users_collection.find_one(
    {
        "email": st.session_state.user_email
    }
)

books = list(
    books_collection.find(
        {
            "added_by": st.session_state.user_email
        }
    )
)

# ------------------------------------------------
# Statistics
# ------------------------------------------------
book_count = len(books)

title_lengths = [len(book["title"]) for book in books]

if title_lengths:
    average_title_length = np.mean(title_lengths)
    longest_title = np.max(title_lengths)
    shortest_title = np.min(title_lengths)
else:
    average_title_length = 0
    longest_title = 0
    shortest_title = 0

# ------------------------------------------------
# Title
# ------------------------------------------------
st.title("👤 My Profile")

st.divider()

# ------------------------------------------------
# Account Information
# ------------------------------------------------
st.subheader("Account Information")

st.write(f"**Name:** {user['name']}")
st.write(f"**Email:** {user['email']}")

st.divider()

# ------------------------------------------------
# Change Password
# ------------------------------------------------
st.subheader("🔒 Change Password")

current_password = st.text_input(
    "Current Password",
    type="password"
)

new_password = st.text_input(
    "New Password",
    type="password"
)

confirm_password = st.text_input(
    "Confirm New Password",
    type="password"
)

if st.button(
    "Change Password",
    use_container_width=True
):

    if not current_password or not new_password or not confirm_password:
        st.error("Please fill all the fields.")

    elif current_password != user["password"]:
        st.error("Current password is incorrect.")

    elif new_password != confirm_password:
        st.error("New passwords do not match.")

    elif current_password == new_password:
        st.error("New password must be different from the current password.")

    elif len(new_password) < 6:
        st.error("Password must contain at least 6 characters.")

    else:

        users_collection.update_one(
            {
                "email": st.session_state.user_email
            },
            {
                "$set": {
                    "password": new_password
                }
            }
        )

        st.success("Password changed successfully.")

        # Refresh user information
        user = users_collection.find_one(
            {
                "email": st.session_state.user_email
            }
        )

st.divider()

# ------------------------------------------------
# Library Statistics
# ------------------------------------------------
st.subheader("Library Statistics")

st.metric(
    "Total Books",
    book_count
)

st.metric(
    "Average Title Length",
    f"{average_title_length:.2f}"
)

st.metric(
    "Longest Title",
    longest_title
)

st.metric(
    "Shortest Title",
    shortest_title
)

st.divider()

# ------------------------------------------------
# NumPy Demonstration
# ------------------------------------------------
st.subheader("NumPy Analysis")

if title_lengths:

    st.write("Title Lengths")

    st.write(title_lengths)

    st.write(f"Mean : {np.mean(title_lengths):.2f}")
    st.write(f"Median : {np.median(title_lengths):.2f}")
    st.write(f"Maximum : {np.max(title_lengths)}")
    st.write(f"Minimum : {np.min(title_lengths)}")
    st.write(f"Standard Deviation : {np.std(title_lengths):.2f}")

else:

    st.info("No books available for analysis.")

st.divider()

if st.button(
    "⬅ Back to Dashboard",
    use_container_width=True
):
    st.switch_page("pages/3_Dashboard.py")