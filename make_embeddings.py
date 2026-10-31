import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

df = pd.read_csv("movies.csv")
df["description"] = df["description"].fillna("")
df = df.drop_duplicates(subset="title").reset_index(drop=True)

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(df["description"].tolist(), show_progress_bar=True)

np.save("embeddings.npy", embeddings)
print("Saved", embeddings.shape)