import tomllib
import time
import requests
import pandas as pd

with open(".streamlit/secrets.toml", "rb") as f:
    key = tomllib.load(f)["TMDB_API_KEY"]

def get_json(url, params):
    """Ask TMDB. If the connection drops, wait and try again."""
    for attempt in range(5):
        try:
            return requests.get(url, params=params, timeout=15).json()
        except requests.exceptions.RequestException:
            print("  connection problem, retrying...", attempt + 1)
            time.sleep(3)
    return {}  # give up on this page, but don't crash

languages = {"hi": "Bollywood", "te": "Tollywood", "mr": "Marathi", "ml": "Malayalam"}

g = get_json("https://api.themoviedb.org/3/genre/movie/list", {"api_key": key})
genre_names = {x["id"]: x["name"] for x in g.get("genres", [])}

rows = []
for code, industry in languages.items():
    for page in range(1, 26):
        params = {
            "api_key": key,
            "with_original_language": code,
            "sort_by": "vote_count.desc",
            "vote_count.gte": 10,
            "page": page,
        }
        data = get_json("https://api.themoviedb.org/3/discover/movie", params)
        for m in data.get("results", []):
            if not m["overview"]:
                continue
            rows.append({
                "title": m["title"],
                "industry": industry,
                "genre": ", ".join(genre_names.get(i, "") for i in m["genre_ids"]),
                "year": m["release_date"][:4],
                "rating": m["vote_average"],
                "description": m["overview"],
                "poster": m["poster_path"],
            })
        time.sleep(0.5)
    print(industry, "done")

df = pd.DataFrame(rows)
df.to_csv("movies.csv", index=False)
print("Saved", len(df), "movies")
