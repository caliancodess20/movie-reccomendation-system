# 🎬 FilmyDost: Indian Movie Recommender

> Every mood has a movie. Every language has a story.

FilmyDost is an Indian cinema discovery app. Pick a movie you love, choose a mood, or explore regional cinema on a map of India.

---

## ✨ Features

🎯 **Smart Recommendations** - Content-based filtering using sentence embeddings and cosine similarity  
🎭 **Mood-Based Discovery** - Pick a mood (Romantic, Need a Laugh, Need Excitement and more) and get matching movies  
🗺️ **India Map of Cinema** - Click a state or Union Territory to explore its regional cinema, language and movies  
🎬 **Industry Filter** - Bollywood, Tollywood, Marathi and Malayalam  
🌏 **Language-Aware Captions** - Short regional captions, shown only where the language is known  
🌙 **Cinematic Dark Theme** - Mobile-friendly layout with reduced-motion support  
📊 **Analytics** - Movies by industry and ratings over time  

---

## 🎭 How the mood feature works

The mood feature is a separate, optional layer. It does not change the original recommender.

1. Each mood maps to a list of genres (`mood_config.py`).
2. `mood_ranker.py` scores every movie by how many of its genres match the mood.
3. The top-rated matches are shown. **Surprise Me** picks random movies.
4. If nothing matches, the app shows a friendly message.

New rankers (for example, an embedding-based one) can be added as functions with the same shape: `ranker(mood, movies_df)` returns one score per movie.

## 🗺️ How the India map works

- All 28 states and 8 Union Territories are on the map.
- Regions with movies in our collection show real titles: Maharashtra (Marathi), Telangana and Andhra Pradesh (Tollywood), Kerala (Malayalam) and Uttar Pradesh and Madhya Pradesh (Bollywood).
- Other regions show their cinema and language with a "coming soon" note. Nothing is invented.
- This is a discovery guide by language and industry. It is not a claim that every movie belongs to a state's film industry.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web framework and UI |
| **Pandas / NumPy** | Data handling |
| **Scikit-learn** | Cosine similarity |
| **Sentence embeddings** | Movie plot vectors (`embeddings.npy`) |
| **Plotly** | Charts and the India map |
| **TMDB API** | Movie data and posters |

---

## 📁 Project structure

| File | Purpose |
|------|---------|
| `streamlit_app.py` | The app: data loading, recommendations and UI |
| `movies.csv` | Movie data: title, industry, genre, year, rating, description, poster |
| `embeddings.npy` | One embedding per movie, in the same row order as `movies.csv` |
| `mood_config.py` | Mood to genre mapping, plus emoji and taglines |
| `mood_ranker.py` | Mood scoring and mood recommendations |
| `region_config.py` | Region data for the map, plus language captions |
| `map_view.py` | Draws the India map |
| `india_states_merged.geojson` | State and Union Territory boundaries |
| `make_states_map.py` | One-time script that builds the merged map file |
| `.streamlit/config.toml` | Dark theme |

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/caliancodess20/movie-reccomendation-system.git
cd movie-reccomendation-system

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run streamlit_app.py
```

Note: `embeddings.npy` must stay in the same row order as `movies.csv`. If you change the CSV, regenerate the embeddings.

---

## 🔭 Future ideas

- A second mood ranker using the existing embeddings
- Mood vectors (for example, light to dark, calm to high energy)
- More industries (Tamil, Kannada, Bengali and others), so more map regions have movies

---

## 🙏 Credits

This product uses the TMDB API but is not endorsed or certified by TMDB.