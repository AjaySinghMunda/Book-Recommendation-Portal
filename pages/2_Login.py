import streamlit as st
import pymongo

# ------------------------------------------------
# Page Configuration
# ------------------------------------------------
st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)

# ------------------------------------------------
# MongoDB Connection
# ------------------------------------------------
conn = pymongo.MongoClient(st.secrets["MONGO_URI"])

db = conn["BookRecommendationSystem"]

users_collection = db["Users"]

# ------------------------------------------------
# Session State
# ------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ------------------------------------------------
# Title
# ------------------------------------------------
st.title("🔐 Login")

st.write(
    "Login to access your personal library and recommendations."
)

st.divider()

# ------------------------------------------------
# Login Form
# ------------------------------------------------
email = st.text_input(
    "Email Address",
    placeholder="Enter your registered email"
)

password = st.text_input(
    "Password",
    type="password"
)

# ------------------------------------------------
# Login Button
# ------------------------------------------------
if st.button(
    "Login",
    use_container_width=True
):

    if not email or not password:

        st.error("Please fill all the fields.")

    else:

        user = users_collection.find_one(
            {
                "email": email
            }
        )

        if user is None:

            st.error("No account found with this email.")

        elif user["password"] != password:

            st.error("Incorrect password.")

        else:

            st.session_state.logged_in = True
            st.session_state.user_name = user["name"]
            st.session_state.user_email = user["email"]

            st.success("Login Successful!")

            st.switch_page("pages/3_Dashboard.py")

# ------------------------------------------------
# Sign Up
# ------------------------------------------------
st.write("")

st.caption("Don't have an account?")

if st.button(
    "Create Account",
    use_container_width=True
):
    st.switch_page("pages/1_Sign_Up.py")