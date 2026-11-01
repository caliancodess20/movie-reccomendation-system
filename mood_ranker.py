import pandas as pd
from mood_config import MOOD_GENRES


def genre_ranker(mood, movies_df):
    wanted = MOOD_GENRES.get(mood, [])

    def score(genre_text):
        if not isinstance(genre_text, str):
            return 0
        movie_genres = [g.strip() for g in genre_text.split(",")]
        return sum(g in wanted for g in movie_genres)

    return movies_df["genre"].apply(score)


def recommend_by_mood(mood, movies_df, num=5):
    if mood == "Surprise Me":
        return movies_df.sample(num)

    scores = genre_ranker(mood, movies_df)
    matches = movies_df[scores > 0]

    if matches.empty:
        return pd.DataFrame()

    return matches.nlargest(num, "rating")