import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("movies.csv")
df["genre"] = df["genre"].fillna("")
df["description"] = df["description"].fillna("")
df = df.drop_duplicates(subset="title").reset_index(drop=True)

# the model turns each story into 384 numbers that capture its meaning
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(df["description"].tolist(), show_progress_bar=True)
sim = cosine_similarity(embeddings)

genre_sets = [set(g.split(", ")) - {""} for g in df["genre"]]

scores = []
for i in range(len(df)):
    if not genre_sets[i]:
        continue
    top5 = sim[i].argsort()[::-1][1:6]
    hits = sum(1 for j in top5 if genre_sets[i] & genre_sets[j])
    scores.append(hits / 5)

print("Movies tested:", len(scores))
print("Genre match score:", round(sum(scores) / len(scores), 3))