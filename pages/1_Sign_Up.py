import streamlit as st
import pymongo
import smtplib
import random
import re

from email.mime.text import MIMEText

# ------------------------------------------------
# Page Configuration
# ------------------------------------------------
st.set_page_config(
    page_title="Sign Up",
    page_icon="📝",
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
if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False

# ------------------------------------------------
# Title
# ------------------------------------------------
st.title("📝 Create an Account")

st.write(
    "Create your account to manage books and receive AI-powered recommendations."
)

st.divider()

# ------------------------------------------------
# Registration Form
# ------------------------------------------------
name = st.text_input(
    "Full Name",
    placeholder="Enter your full name"
)

email = st.text_input(
    "Email Address",
    placeholder="Enter your email"
)

password = st.text_input(
    "Password",
    type="password"
)

confirm_password = st.text_input(
    "Confirm Password",
    type="password"
)

# ------------------------------------------------
# Register Button
# ------------------------------------------------
if st.button("Register", use_container_width=True):

    if not name or not email or not password or not confirm_password:
        st.error("Please fill all the fields.")

    elif password != confirm_password:
        st.error("Passwords do not match.")

    elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        st.error("Please enter a valid email address.")

    elif users_collection.find_one({"email": email}):
        st.error("Email already registered.")

    else:

        otp = random.randint(100000, 999999)

        st.session_state.otp = otp
        st.session_state.name = name
        st.session_state.email = email
        st.session_state.password = password
        st.session_state.otp_sent = True

        try:

            message = MIMEText(
                f"""
Hello {name},

Your OTP for Book Recommendation System is:

{otp}

This OTP is valid for this registration only.

Thank you.
"""
            )

            message["Subject"] = "Email Verification OTP"
            message["From"] = st.secrets["EMAIL"]
            message["To"] = email

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()

            server.login(
                st.secrets["EMAIL"],
                st.secrets["EMAIL_PASSWORD"]
            )

            server.send_message(message)

            server.quit()

            st.success("OTP sent successfully.")

        except Exception as e:

            st.error(f"Unable to send OTP.\n{e}")

# ------------------------------------------------
# OTP Verification
# ------------------------------------------------
if st.session_state.otp_sent:

    st.divider()

    st.subheader("Email Verification")

    otp_input = st.text_input(
        "Enter OTP"
    )

    if st.button(
        "Verify OTP",
        use_container_width=True
    ):

        if otp_input == str(st.session_state.otp):

            users_collection.insert_one({

                "name": st.session_state.name,
                "email": st.session_state.email,
                "password": st.session_state.password

            })

            st.success("Registration Successful!")

            st.session_state.otp_sent = False

            st.switch_page("pages/2_Login.py")

        else:

            st.error("Invalid OTP.")

# ------------------------------------------------
# Login Button
# ------------------------------------------------
st.write("")

st.caption("Already have an account?")

if st.button(
    "Go to Login",
    use_container_width=True
):
    st.switch_page("pages/2_Login.py")
    
