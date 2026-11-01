from mood_config import MOOD_GENRES


def genre_ranker(mood, movies_df):
    wanted = MOOD_GENRES.get(mood, [])

    def score(genre_text):
        movie_genres = [g.strip() for g in genre_text.split(",")]
        return sum(g in wanted for g in movie_genres)

    return movies_df["genre"].apply(score)