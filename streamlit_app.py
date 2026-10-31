
# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

@st.cache_data
def load_data():
    """Read movies from the CSV file we collected"""
    df = pd.read_csv("movies.csv")
    df["genre"] = df["genre"].fillna("")
    df["description"] = df["description"].fillna("")
    df = df.drop_duplicates(subset="title").reset_index(drop=True)
    return df


@st.cache_resource
def build_similarity(texts):
    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(texts)
    return cosine_similarity(matrix)

def get_recommendations(movie_title, movies_df, num_recommendations=5):
    texts = (movies_df["genre"] + " " + movies_df["description"]).tolist()
    cosine_sim = build_similarity(texts)

    matches = movies_df[movies_df["title"] == movie_title]
    if matches.empty:
        return pd.DataFrame()
    idx = matches.index[0]

    sim_scores = sorted(enumerate(cosine_sim[idx]), key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations + 1]

    recommendations = movies_df.iloc[[i for i, _ in sim_scores]].copy()
    recommendations["similarity"] = [s for _, s in sim_scores]
    return recommendations

def main():
    st.title("🎬 Simple Movie Recommender")
    st.markdown("Find movies similar to your favorites!")

    # Load data
    movies_df = load_data()

    # Sidebar
    st.sidebar.title("Options")

    # Movie selection
    selected_movie = st.selectbox(
        "Choose a movie you like:",
        movies_df['title'].tolist()
    )

    num_recs = st.sidebar.slider("Number of recommendations:", 1, 10, 5)

    # Show selected movie info
    selected_info = movies_df[movies_df['title'] == selected_movie].iloc[0]

    st.subheader(f"Selected Movie: {selected_movie}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Genre:** {selected_info['genre']}")
    with col2:
        st.write(f"**Year:** {selected_info['year']}")
    with col3:
        st.write(f"**Rating:** ⭐ {selected_info['rating']}")

    st.write(f"**Plot:** {selected_info['description']}")

    # Get recommendations
    if st.button("Get Recommendations", type="primary"):
        recommendations = get_recommendations(selected_movie, movies_df, num_recs)

        if not recommendations.empty:
            st.subheader("🎯 Recommended Movies:")

            for idx, movie in recommendations.iterrows():
                with st.expander(f"🎬 {movie['title']} (Similarity: {movie['similarity']:.2f})"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**Genre:** {movie['genre']}")
                        st.write(f"**Year:** {movie['year']}")
                        st.write(f"**Rating:** ⭐ {movie['rating']}")
                        st.write(f"**Plot:** {movie['description']}")
                    with col2:
                        st.metric("Similarity Score", f"{movie['similarity']:.2f}")
        else:
            st.error("No recommendations found!")

    # Show all movies
    if st.sidebar.checkbox("Show all movies"):
        st.subheader("📚 Movie Database")
        st.dataframe(movies_df[['title', 'genre', 'year', 'rating']], use_container_width=True)

    # Simple analytics
    if st.sidebar.checkbox("Show analytics"):
        st.subheader("📊 Movie Analytics")

        # Genre distribution
        genre_counts = movies_df['genre'].value_counts()
        fig = px.pie(values=genre_counts.values, names=genre_counts.index, title="Movies by Genre")
        st.plotly_chart(fig, use_container_width=True)

        # Ratings over time
        fig2 = px.scatter(movies_df, x='year', y='rating', color='genre', 
                         title="Movie Ratings Over Time", hover_data=['title'])
        st.plotly_chart(fig2, use_container_width=True)

if __name__ == "__main__":
    main()
