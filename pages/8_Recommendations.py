import streamlit as st
import pymongo

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

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
conn = pymongo.MongoClient(
    st.secrets["MONGO_URI"]
)

db = conn["BookRecommendationSystem"]

books_collection = db["Books"]

catalog_collection = db["Catalog"]

# ------------------------------------------------
# Title
# ------------------------------------------------
st.title("🤖 Book Recommendation Engine")

st.write(
    "Discover books you'll enjoy using AI-powered recommendations."
)

st.divider()

# ------------------------------------------------
# Fetch Data
# ------------------------------------------------
user_books = list(
    books_collection.find(
        {
            "added_by": st.session_state.user_email
        }
    )
)

catalog_books = list(
    catalog_collection.find()
)

# ------------------------------------------------
# Recommendation Mode
# ------------------------------------------------
st.subheader("Choose Recommendation Mode")

mode = st.radio(
    "How would you like to receive recommendations?",
    [
        "📚 Recommend Similar Books",
        "✍️ Describe What You Want"
    ]
)

st.divider()

# ------------------------------------------------
# Mode 1
# ------------------------------------------------
if mode == "📚 Recommend Similar Books":

    st.subheader("📚 Recommend Similar Books")

    st.info(
        "Select one of your books to receive similar recommendations."
    )

    if len(user_books) == 0:
    
        st.warning(
            "You haven't added any books yet."
        )
    
    else:
    
        selected_title = st.selectbox(
            "Choose a Book",
            [
                book["title"]
                for book in user_books
            ]
        )
    
        if st.button(
            "🔍 Get Recommendations",
            use_container_width=True
        ):
                # ----------------------------
                # Find Selected Book
                # ----------------------------
                selected_book = next(
                    (
                        book
                        for book in user_books
                        if book["title"] == selected_title
                    ),
                    None
                )
            
                if selected_book is None:
                    st.error("Book not found.")
            
                else:
            
                    # Combine selected book with catalog
                    books_for_ai = [selected_book] + catalog_books
            
                    df = pd.DataFrame(books_for_ai)
            
                    # Fill missing values
                    df["description"] = df["description"].fillna("")
                    df["genre"] = df["genre"].fillna("")
            
                    # Create text for AI
                    df["content"] = (
                        df["title"]
                        + " "
                        + df["author"]
                        + " "
                        + df["genre"]
                        + " "
                        + df["description"]
                    )
            
                    # TF-IDF
                    vectorizer = TfidfVectorizer(
                        stop_words="english"
                    )
            
                    tfidf_matrix = vectorizer.fit_transform(
                        df["content"]
                    )
            
                    similarity = cosine_similarity(
                        tfidf_matrix
                    )
            
                    scores = list(
                        enumerate(similarity[0])
                    )
            
                    scores = sorted(
                        scores,
                        key=lambda x: x[1],
                        reverse=True
                    )
                    owned_titles = {
                        book["title"]
                        for book in user_books
                    }
            
                    recommendations = []
            
                    for index, score in scores[1:]:
            
                        candidate = df.iloc[index]
            
                        if candidate["title"] in owned_titles:
                            continue
            
                        recommendations.append(
                            {
                                "title": candidate["title"],
                                "author": candidate["author"],
                                "genre": candidate["genre"],
                                "publication_year": candidate["publication_year"],
                                "description": candidate["description"],
                                "score": score
                            }
                        )
            
                        if len(recommendations) == 5:
                            break  
                        
                st.divider()

                st.subheader("📖 Recommended Books")
        
                if len(recommendations) == 0:
        
                    st.warning(
                        "No recommendations found."
                    )
        
                else:
        
                    for book in recommendations:
        
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
        
                            st.write(
                                f"**⭐ Match Score:** {book['score']*100:.1f}%"
                            )
        
                            st.write(book["description"])       

# ------------------------------------------------
# Mode 2
# ------------------------------------------------
else:

    st.subheader("✍️ Describe What You Want")

    st.info(
        "Describe the type of book you are looking for."
    )

    user_prompt = st.text_area(
        "Describe the book you want",
        placeholder="Example:\nA fast-paced thriller with unexpected twists.",
        height=180
    )
    
    st.button(
        "🤖 Find Books",
        use_container_width=True
    )

st.divider()

# ------------------------------------------------
# Recommendation Area
# ------------------------------------------------
st.subheader("📖 Recommendations")

st.info(
    f"""
Catalog Books : {len(catalog_books)}

Your Library : {len(user_books)}

Recommendations will appear here.
"""
)

st.divider()

# ------------------------------------------------
# Back Button
# ------------------------------------------------
if st.button(
    "⬅ Back to Dashboard",
    use_container_width=True
):
    st.switch_page("pages/3_Dashboard.py")
    
