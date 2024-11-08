import streamlit as st
import pickle
import numpy as np

# Load data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Function to recommend books
def recommend(user_input):
    try:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(item)

        return data
    except IndexError:
        return None  # Return None if book title is not found

# Streamlit App
st.set_page_config(page_title="Book Recommender System", page_icon="📚", layout="wide")

# Create tabs
tabs = st.tabs(["Home", "Top 50 Books", "Get Recommendations"])

# Custom CSS for styling
st.markdown(
    """
    <style>
    .book-card {
        margin: 10px;
        background-color: #1e1e1e;
        border-radius: 5px;
        padding: 10px;
        color: white;
        width: 150px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
    }
    .book-title {
        font-size: 14px;
        text-align: center;
        margin-top: 5px;
    }
    .book-author {
        font-size: 12px;
        text-align: center;
        margin-bottom: 5px;
    }
    .home-title {
        text-align: center;
        color: #FFD700;
        font-size: 36px;
        margin: 20px 0;
    }
    .home-description {
        text-align: center;
        color: #ffffff;
        font-size: 18px;
        margin: 10px 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Home Tab
with tabs[0]:
    st.markdown('<h1 class="home-title">Welcome to the Book Recommender System!</h1>', unsafe_allow_html=True)
    st.markdown('<p class="home-description">Discover your next favorite book based on popular titles or get personalized recommendations!</p>', unsafe_allow_html=True)
    st.image("book.jpg", caption="Explore the World of Books!", use_column_width=True)  # Replace with your image URL
    st.markdown('<p class="home-description">Navigate to the "Top 50 Books" to see popular choices or use the "Get Recommendations" tab for tailored suggestions.</p>', unsafe_allow_html=True)

# Tab for Top 50 Books
with tabs[1]:
    st.title('📚 My Book Recommender')
    st.header('Top 50 Books')

    # Display popular books in a grid format
    cols = st.columns(4)  # Four columns
    for i in range(len(popular_df)):
        with cols[i % 4]:
            # Each book displayed in a card format
            st.markdown('<div class="book-card">', unsafe_allow_html=True)
            st.image(popular_df['Image-URL-M'].values[i], width=120)  # Set a consistent image width
            st.markdown(f"<div class='book-title'>{popular_df['Book-Title'].values[i]}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='book-author'>Author: {popular_df['Book-Author'].values[i]}</div>", unsafe_allow_html=True)
            st.write(f"**Votes:** {popular_df['num_ratings'].values[i]}")
            st.write(f"**Rating:** {popular_df['avg_rating'].values[i]:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)

# Tab for Recommendations
with tabs[2]:
    st.header('Get Book Recommendations')
    user_input = st.text_input('Enter a book title:', '')

    if st.button('Recommend'):
        if user_input:
            recommendations = recommend(user_input)
            if recommendations:
                st.subheader('Recommended Books:')
                # Display recommended books in the same card format
                cols = st.columns(4)  # Four columns
                for i, rec in enumerate(recommendations):
                    with cols[i % 4]:  # Ensure proper alignment
                        st.markdown('<div class="book-card">', unsafe_allow_html=True)
                        st.image(rec[2], width=120)  # Set a consistent image width
                        st.markdown(f"<div class='book-title'>{rec[0]}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='book-author'>{rec[1]}</div>", unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning('Book not found. Please try another title.')
        else:
            st.warning('Please enter a book title to get recommendations.')
