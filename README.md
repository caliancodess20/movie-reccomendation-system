# 🎬 Indian Movie Recommender

Find movies similar to your favourites across **Bollywood, Tollywood (Telugu), Marathi and Malayalam** cinema.

**[Live demo →](https://movie-reccomendation-system-djg9yfhyxezca4jmurghau.streamlit.app/)**

## What it does
Pick a movie and the app suggests similar ones, with posters, genre, year, rating and a similarity score.

## How it works
1. **Data:** about 1,900 movies collected from the TMDB API (`collect_movies.py`).
2. **ML:** each movie's plot is turned into an **embedding** (numbers that capture meaning) using `sentence-transformers` (`all-MiniLM-L6-v2`).
3. **Matching:** **cosine similarity** finds the movies whose embeddings are closest.
4. **App:** built with Streamlit. Embeddings are computed once (`make_embeddings.py`) and loaded from `embeddings.npy`, so the website stays fast.

## Results
I compared three methods on the same test: how often the top 5 recommendations share a genre with the chosen movie (plot text only, no genre given to the model).

| Method | Genre match score |
|---|---|
| TF-IDF (single words) | 0.687 |
| TF-IDF (word pairs) | 0.692 |
| **Sentence embeddings** | **0.711** |

*Limitation:* this test only checks genre overlap, so it understates recommendations that are good for other reasons. Marathi has fewer movies than the other three industries because TMDB has less data for it.

## Run locally
```bash
git clone https://github.com/caliancodess20/movie-reccomendation-system.git
cd movie-reccomendation-system
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Tech stack
Python, Streamlit, pandas, NumPy, scikit-learn, sentence-transformers, Plotly.

*This product uses the TMDB API but is not endorsed or certified by TMDB.*