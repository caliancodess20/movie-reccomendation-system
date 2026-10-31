import tomllib
import requests

# read the key from the secrets file
with open(".streamlit/secrets.toml", "rb") as f:
    key = tomllib.load(f)["TMDB_API_KEY"]

# ask TMDB for Marathi movies
url = "https://api.themoviedb.org/3/discover/movie"
params = {"api_key": key, "with_original_language": "mr"}
data = requests.get(url, params=params).json()

# print the first 5 titles
for movie in data["results"][:5]:
    print(movie["title"])