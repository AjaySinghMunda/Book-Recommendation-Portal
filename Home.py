import streamlit as st

st.set_page_config(
    page_title="Book Recommendation Portal",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Book Recommendation Portal")

st.divider()

st.subheader("Welcome!")

st.write(
    """
    Discover books, manage your personal library,
    and receive AI-powered book recommendations.
    """
)

st.write("")

col1, col2 = st.columns(2)

with col1:
    if st.button("📝 Sign Up", use_container_width=True):
        st.switch_page("pages/1_Sign_Up.py")

with col2:
    if st.button("🔑 Login", use_container_width=True):
        st.switch_page("pages/2_Login.py")

st.write("")
st.write("")

st.info("Create an account to add books and receive recommendations.")