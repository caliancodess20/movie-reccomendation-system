import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("movies.csv")
df["genre"] = df["genre"].fillna("")
df["description"] = df["description"].fillna("")
df = df.drop_duplicates(subset="title").reset_index(drop=True)

text = df["description"]
matrix = TfidfVectorizer(stop_words="english").fit_transform(text)
sim = cosine_similarity(matrix)

# turn "Action, Drama" into a set of genre names
genre_sets = [set(g.split(", ")) - {""} for g in df["genre"]]

scores = []
for i in range(len(df)):
    if not genre_sets[i]:
        continue
    top5 = sim[i].argsort()[::-1][1:6]  # best 5, skipping the movie itself
    hits = sum(1 for j in top5 if genre_sets[i] & genre_sets[j])
    scores.append(hits / 5)

print("Movies tested:", len(scores))
print("Genre match score:", round(sum(scores) / len(scores), 3))