# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px
from mood_config import MOOD_GENRES
from mood_ranker import recommend_by_mood

st.set_page_config(
    page_title="Indian Movie Recommender",
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
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    return df

@st.cache_resource
def build_similarity():
    embeddings = np.load("embeddings.npy")
    return cosine_similarity(embeddings)

def get_recommendations(movie_title, movies_df, num_recommendations=5):
    cosine_sim = build_similarity()

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
    st.title("🎬 Indian Movie Recommender")
    st.markdown("Find movies similar to your favorites: Bollywood, Tollywood, Marathi and Malayalam!")

    movies_df = load_data()

    st.sidebar.title("Options")

    selected_movie = st.selectbox(
        "Choose a movie you like:",
        movies_df["title"].tolist()
    )

    num_recs = st.sidebar.slider("Number of recommendations:", 1, 10, 5)

    industry_choice = st.sidebar.selectbox(
        "Show recommendations from:",
        ["All"] + sorted(movies_df["industry"].unique())
    )

    selected_info = movies_df[movies_df["title"] == selected_movie].iloc[0]

    st.subheader(f"Selected Movie: {selected_movie}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Genre:** {selected_info['genre']}")
    with col2:
        st.write(f"**Year:** {selected_info['year']}")
    with col3:
        st.write(f"**Rating:** ⭐ {selected_info['rating']}")

    st.write(f"**Plot:** {selected_info['description']}")

    if st.button("Get Recommendations", type="primary"):
        recommendations = get_recommendations(selected_movie, movies_df, 1000)
        if industry_choice != "All":
            recommendations = recommendations[recommendations["industry"] == industry_choice]
        recommendations = recommendations.head(num_recs)

        if not recommendations.empty:
            st.subheader("🎯 Recommended Movies:")

            cols_per_row = 5
            rows = list(recommendations.iterrows())
            for start in range(0, len(rows), cols_per_row):
                cols = st.columns(cols_per_row)
                for col, (idx, movie) in zip(cols, rows[start:start + cols_per_row]):
                    with col:
                        if pd.notna(movie["poster"]):
                            st.image("https://image.tmdb.org/t/p/w300" + movie["poster"])
                        st.markdown(f"**{movie['title']}**")
                        st.caption(f"{movie['industry']} · {movie['year']} · ⭐ {movie['rating']:.1f}")
                        st.caption(f"Match: {movie['similarity']:.0%}")
                        with st.expander("Plot"):
                            st.write(movie["description"])
        else:
            st.error("No recommendations found!")

    st.header("What's your mood today? ✨")
    st.caption("Every mood deserves its own movie.")

    moods = list(MOOD_GENRES.keys()) + ["Surprise Me"]
    selected_mood = st.radio("Pick a mood:", moods, horizontal=True)

    if st.button("Find My Movie"):
        mood_results = recommend_by_mood(selected_mood, movies_df, num_recs)
        if mood_results.empty:
            st.warning("No mood match found.")
        else:
            for _, m in mood_results.iterrows():
                st.write(f"🎬 {m['title']} ({m['industry']}, {m['year']})")

    if st.sidebar.checkbox("Show all movies"):
        st.subheader("📚 Movie Database")
        st.dataframe(movies_df[["title", "industry", "genre", "year", "rating"]],
                     use_container_width=True)

    if st.sidebar.checkbox("Show analytics"):
        st.subheader("📊 Movie Analytics")

        industry_counts = movies_df["industry"].value_counts()
        fig = px.pie(values=industry_counts.values, names=industry_counts.index,
                     title="Movies by Industry")
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.scatter(movies_df, x="year", y="rating", color="industry",
                          title="Movie Ratings Over Time", hover_data=["title"])
        st.plotly_chart(fig2, use_container_width=True)

    st.caption("This product uses the TMDB API but is not endorsed or certified by TMDB.")

if __name__ == "__main__":
    main()