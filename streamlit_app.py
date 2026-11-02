# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px
from mood_config import MOOD_GENRES, MOOD_INFO
from mood_ranker import recommend_by_mood
from map_view import build_map
from region_config import REGIONS, LANGUAGE_CAPTIONS
from styles import BASE_CSS

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
    
    st.html("""
    <style>
    [class*="st-key-mood_"] button {
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        border-radius: 14px;
    }
    [class*="st-key-mood_"] button:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(192, 80, 106, 0.35);
    }
    [class*="st-key-mood_"] [data-testid="stBaseButton-primary"] {
        box-shadow: 0 0 18px rgba(212, 175, 55, 0.55);
        border: 1px solid #d4af37;
    }
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    [data-testid="stImage"] {
        animation: fadeUp 0.6s ease both;
    }
    @keyframes twinkle {
        0%, 100% { opacity: 0.25; transform: scale(0.8); }
        50% { opacity: 1; transform: scale(1.15); }
    }
    [class*="st-key-mood_Surprise"] button {
        position: relative;
    }
    [class*="st-key-mood_Surprise"] button::after {
        content: "✦";
        position: absolute;
        top: 4px;
        right: 10px;
        color: #d4af37;
        animation: twinkle 2.4s ease-in-out infinite;
    }
    @media (max-width: 640px) {
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
            flex: 1 1 calc(50% - 1rem) !important;
            min-width: calc(50% - 1rem) !important;
        }
    }
    @media (prefers-reduced-motion: reduce) {
        [class*="st-key-mood_"] button { transition: none; }
        [class*="st-key-mood_"] button:hover { transform: none; }
        [data-testid="stImage"] { animation: none; }
        [class*="st-key-mood_Surprise"] button::after { animation: none; opacity: 1; }
    }
    </style>
    """)

    st.title("🎬 Indian Movie Recommender")
    st.markdown("Find movies similar to your favorites: Bollywood, Tollywood, Marathi and Malayalam!")
    st.caption("Every mood has a movie. Every language has a story.")

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
            st.subheader("If you liked that, try these! 🎯")

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

    moods = list(MOOD_INFO.keys())

    if "selected_mood" not in st.session_state:
        st.session_state.selected_mood = moods[0]

    mood_cols = st.columns(len(moods))
    for col, mood in zip(mood_cols, moods):
        emoji, tagline = MOOD_INFO[mood]
        with col:
            is_selected = st.session_state.selected_mood == mood
            if st.button(
                f"{emoji} {mood}",
                key=f"mood_{mood}",
                type="primary" if is_selected else "secondary",
                use_container_width=True,
            ):
                st.session_state.selected_mood = mood
                st.rerun()
            st.caption(tagline)

    selected_mood = st.session_state.selected_mood

    if st.button("Find My Movie"):
        mood_pool = movies_df
        if industry_choice != "All":
            mood_pool = movies_df[movies_df["industry"] == industry_choice]
        with st.spinner("Finding stories you'll love…"):
            mood_results = recommend_by_mood(selected_mood, mood_pool, num_recs)
        if mood_results.empty:
            st.warning("Couldn't find the right match this time. Try another mood or language.")
        else:
            st.subheader("Picked for your mood. ✨")
            mood_rows = list(mood_results.iterrows())
            mood_cols_per_row = 5
            for start in range(0, len(mood_rows), mood_cols_per_row):
                result_cols = st.columns(mood_cols_per_row)
                for rc, (_, m) in zip(result_cols, mood_rows[start:start + mood_cols_per_row]):
                    with rc:
                        if pd.notna(m["poster"]):
                            st.image("https://image.tmdb.org/t/p/w300" + m["poster"])
                        st.markdown(f"**{m['title']}**")
                        st.caption(f"{m['industry']} · {m['year']} · ⭐ {m['rating']:.1f}")
                        with st.expander("Plot"):
                            st.write(m["description"])

    st.header("India Map of Cinema 🗺️")

    if "selected_region" not in st.session_state:
        st.session_state.selected_region = None
    if "map_version" not in st.session_state:
        st.session_state.map_version = 0

    map_event = st.plotly_chart(
        build_map(st.session_state.selected_region),
        use_container_width=True,
        theme=None,
        on_select="rerun",
        selection_mode="points",
        key=f"india_map_{st.session_state.map_version}",
    )

    points = map_event.selection.points
    if points:
        clicked = points[0]["location"]
        if clicked != st.session_state.selected_region:
            st.session_state.selected_region = clicked
            st.rerun()

    if st.button("Reset selection"):
        st.session_state.selected_region = None
        st.session_state.map_version += 1
        st.rerun()

    chosen_region = st.session_state.selected_region
    if chosen_region:
        region_info = REGIONS[chosen_region]
        st.subheader(chosen_region)
        lang_caption = LANGUAGE_CAPTIONS.get(region_info["language"])
        if lang_caption:
            st.caption(lang_caption)
        if region_info["industry"]:
            region_movies = movies_df[movies_df["industry"] == region_info["industry"]]
            st.write(f"**Cinema:** {region_info['cinema']}")
            st.write(f"**Language:** {region_info['language']}")
            st.write(f"**Movies in our collection:** {len(region_movies)}")
            st.caption("A little gem worth discovering. 💎")

            region_top = list(region_movies.nlargest(5, "rating").iterrows())
            region_cols = st.columns(5)
            for rcol, (_, rm) in zip(region_cols, region_top):
                with rcol:
                    if pd.notna(rm["poster"]):
                        st.image("https://image.tmdb.org/t/p/w300" + rm["poster"])
                    st.markdown(f"**{rm['title']}**")
                    st.caption(f"{rm['year']} · ⭐ {rm['rating']:.1f}")
        elif region_info["cinema"]:
            st.write(f"**Cinema:** {region_info['cinema']}")
            st.write(f"**Language:** {region_info['language']}")
            st.info("Movies from this region are coming soon.")
        else:
            st.info("No cinema data for this region yet.")

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

def home_page():
    main()

def mood_page():
    st.title("Mood Discovery")
    st.caption("Every mood deserves its own movie.")

    movies_df = load_data()

    filter_col, count_col = st.columns(2)
    with filter_col:
        industry_choice = st.selectbox(
            "Show movies from:",
            ["All"] + sorted(movies_df["industry"].unique()),
        )
    with count_col:
        num_recs = st.slider("How many movies?", 1, 10, 5)

    moods = list(MOOD_INFO.keys())

    if "selected_mood" not in st.session_state:
        st.session_state.selected_mood = moods[0]

    mood_cols = st.columns(len(moods))
    for col, mood in zip(mood_cols, moods):
        emoji, tagline = MOOD_INFO[mood]
        with col:
            is_selected = st.session_state.selected_mood == mood
            if st.button(
                f"{emoji} {mood}",
                key=f"mood_{mood}",
                type="primary" if is_selected else "secondary",
                use_container_width=True,
            ):
                st.session_state.selected_mood = mood
                st.rerun()
            st.caption(tagline)

    if st.button("Find My Movie", type="primary"):
        mood_pool = movies_df
        if industry_choice != "All":
            mood_pool = movies_df[movies_df["industry"] == industry_choice]
        with st.spinner("Finding stories you'll love…"):
            mood_results = recommend_by_mood(
                st.session_state.selected_mood, mood_pool, num_recs
            )
        if mood_results.empty:
            st.warning("Couldn't find the right match this time. Try another mood or language.")
        else:
            st.subheader("Picked for your mood. ✨")
            mood_rows = list(mood_results.iterrows())
            for start in range(0, len(mood_rows), 5):
                result_cols = st.columns(5)
                for rc, (_, m) in zip(result_cols, mood_rows[start:start + 5]):
                    with rc:
                        if pd.notna(m["poster"]):
                            st.image("https://image.tmdb.org/t/p/w300" + m["poster"])
                        st.markdown(f"**{m['title']}**")
                        st.caption(f"{m['industry']} · {m['year']} · ⭐ {m['rating']:.1f}")
                        with st.expander("Plot"):
                            st.write(m["description"])

def recommendations_page():
    st.title("Recommendations")
    st.info("This page is coming in the next step.")

def languages_page():
    st.title("Explore Languages")
    st.info("This page is coming in the next step.")

def details_page():
    st.title("Movie Details")
    st.info("This page is coming in the next step.")

pages = [
    st.Page(home_page, title="Home", icon="🎬", url_path="home", default=True),
    st.Page(mood_page, title="Mood Discovery", icon="🎭", url_path="moods"),
    st.Page(recommendations_page, title="Recommendations", icon="🍿", url_path="recommendations"),
    st.Page(languages_page, title="Explore Languages", icon="🗺️", url_path="languages"),
    st.Page(details_page, title="Movie Details", icon="🎞️", url_path="details"),
]
st.html(BASE_CSS)
navigation = st.navigation(pages, position="top")
navigation.run()