<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-1.56-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/scikit--learn-1.8-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

<h1 align="center">✦ Movie & Song Recommendation System</h1> 

<p align="center">
  <strong>An elegant, content-based recommendation engine for movies and Bollywood music — powered by TF-IDF, cosine similarity, and audio-feature fingerprinting.</strong>
</p> 

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-how-it-works">How It Works</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-project-structure">Project Structure</a> •
  <a href="#-datasets">Datasets</a> •
  <a href="#-contributing">Contributing</a>
</p>

---

## 📖 Overview

**Recommendation System** is a full-stack web application built with **Streamlit** that delivers intelligent, content-based recommendations for:

| Domain | Catalogue Size | Algorithm |
|--------|---------------|-----------|
| 🎬 **Movies** | 9,742 titles | TF-IDF vectorization on genres + Cosine Similarity |
| 🎵 **Bollywood Songs** | ~2,000 curated tracks | 8-dimensional audio fingerprint + Cosine Similarity |

The app features a premium dark-mode UI with gold accents, smooth hover animations, Google Fonts typography (Inter, DM Serif Display, Plus Jakarta Sans), and a four-page navigation layout.

---

## ✨ Features

### 🎬 Movie Recommender
- Select any movie from a catalogue of **9,742 titles**
- Get the **top 10 most similar movies** ranked by cosine similarity score
- Results display genre tags, match percentage, and animated progress bars

### 🎵 Song Recommender
Three discovery modes for Bollywood music:

| Mode | Description |
|------|-------------|
| **🔍 Search by Song** | Fuzzy-match a song name → find 10 most sonically similar tracks |
| **🎭 By Mood** | Choose from 6 moods (Happy, Sad, Romantic, Party, Energetic, Chill) → get mood-matched songs |
| **🎤 By Artist** | Search by artist name → browse their top tracks by popularity |

### 📊 Analytics Dashboard
- Live dataset metrics: total movies, songs, and unique artists
- Animated metric cards with gold gradient accents

### 🎨 Premium UI
- Custom dark theme (`#0d0f14` base) with a gold (`#e8a020`) accent palette
- Glassmorphism-inspired card components with hover lift effects
- Responsive layout with `clamp()` fluid typography
- Hidden Streamlit defaults (menu, footer, toolbar) for a clean look

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | [Streamlit](https://streamlit.io/) | Web framework & UI rendering |
| **ML — Movies** | [scikit-learn](https://scikit-learn.org/) (`TfidfVectorizer`, `cosine_similarity`) | Genre vectorization & similarity |
| **ML — Songs** | [scikit-learn](https://scikit-learn.org/) (`MinMaxScaler`, `cosine_similarity`) | Audio feature normalization & similarity |
| **Data** | [pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/) | Data loading, cleaning, transformation |
| **Fuzzy Search** | [RapidFuzz](https://github.com/maxbachmann/RapidFuzz) | Approximate song title matching |
| **Styling** | Vanilla CSS (injected via `st.markdown`) | Custom dark theme, animations, typography |

---

## 🧠 How It Works

### Movie Recommendation Pipeline

```
movies.csv ──► TF-IDF Vectorizer ──► Genre Vectors ──► Cosine Similarity Matrix
                  (token: "|")                              │
                                                            ▼
               User selects movie ──► Lookup index ──► Sort by similarity ──► Top N results
```

1. **Vectorization**: The `genres` column (pipe-delimited, e.g. `Adventure|Comedy|Fantasy`) is tokenized using `TfidfVectorizer(token_pattern=r"[^|]+")`.
2. **Similarity**: A full pairwise `cosine_similarity` matrix is precomputed at startup.
3. **Ranking**: Given a selected movie, the corresponding row is sorted in descending similarity order, and the top 10 are returned with percentage scores.

### Song Recommendation Pipeline

```
hindi_songs.csv ──► Filter (known artists + alphabetic names) ──► Top 2000 by popularity
                                                                        │
                                                                        ▼
                    8 Audio Features ──► MinMaxScaler ──► Cosine Similarity Matrix
                                                                        │
                                                                        ▼
                  User searches song ──► Fuzzy match ──► Lookup index ──► Top N results
```

1. **Filtering**: From 114K raw tracks, songs are filtered to only known Bollywood artists (Arijit Singh, Shreya Ghoshal, Pritam, Neha Kakkar, Atif Aslam, KK, Sonu Nigam, Sunidhi Chauhan, Amit Trivedi, Sachin, Jubin) and capped at 2,000 by popularity.
2. **Feature Engineering**: 8 Spotify audio features are used:
   - `danceability`, `energy`, `valence`, `tempo`
   - `acousticness`, `instrumentalness`, `speechiness`, `liveness`
3. **Normalization**: All features are scaled to `[0, 1]` via `MinMaxScaler`.
4. **Mood Classification**: Rule-based assignment using `valence`, `energy`, and `danceability` thresholds:

   | Mood | Rule |
   |------|------|
   | Happy | `valence > 0.6` AND `energy > 0.6` |
   | Party | `valence > 0.5` AND `danceability > 0.7` |
   | Sad | `valence < 0.4` AND `energy < 0.5` |
   | Romantic | `valence > 0.5` AND `energy < 0.5` |
   | Energetic | `energy > 0.7` |
   | Chill | Everything else |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **pip** (or any Python package manager)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/dhruv-limbasiya/Movie-and-Song-Recommendation-System.git
cd Movie-and-Song-Recommendation-System

# 2. Create a virtual environment (recommended)
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Dataset Setup

Place the following CSV files inside the `data/` directory:

| File | Description | Source |
|------|-------------|--------|
| `movies.csv` | 9,742 movies with `movieId`, `title`, `genres` | [MovieLens Latest Small](https://grouplens.org/datasets/movielens/) |
| `hindi_songs.csv` | 114K tracks with 21 Spotify audio features | Spotify / Kaggle dataset |

> **Note:** CSV files are excluded from version control via `.gitignore`. You must download them separately.

### Run the App

```bash
streamlit run app.py
```

The app will launch at **http://localhost:8501** by default.

---

## 📁 Project Structure

```
Movie-and-Song-Recommendation-System/
│
├── app.py                   # Streamlit application — UI, routing, styling
├── movie_recommender.py     # Movie recommendation engine (TF-IDF + cosine sim)
├── song_recommender.py      # Song recommendation engine (audio features + cosine sim)
├── requirements.txt         # Pinned Python dependencies
├── .gitignore               # Git ignore rules
│
└── data/
    ├── movies.csv           # MovieLens dataset (9,742 rows × 3 cols)
    └── hindi_songs.csv      # Spotify Hindi songs dataset (114K rows × 21 cols)
```

### Module Breakdown

| File | Lines | Exports |
|------|-------|---------|
| [app.py](app.py) | 746 | Streamlit pages: Home, Movies, Songs, Analytics |
| [movie_recommender.py](movie_recommender.py) | 33 | `get_recommendations()`, `get_all_movie_titles()` |
| [song_recommender.py](song_recommender.py) | 143 | `get_song_recommendations()`, `get_songs_by_mood()`, `get_songs_by_artist()`, `get_top_songs()`, `get_all_song_titles()`, `get_all_artists()`, `get_all_moods()` |

---

## 📊 Datasets

### `movies.csv` — MovieLens

| Column | Type | Description |
|--------|------|-------------|
| `movieId` | int | Unique movie identifier |
| `title` | str | Movie title with release year, e.g. `Toy Story (1995)` |
| `genres` | str | Pipe-delimited genre list, e.g. `Adventure\|Animation\|Children\|Comedy\|Fantasy` |

### `hindi_songs.csv` — Spotify Audio Features

| Column | Type | Description |
|--------|------|-------------|
| `track_id` | str | Spotify track ID |
| `artists` | str | Artist name(s) |
| `album_name` | str | Album name |
| `track_name` | str | Song title |
| `popularity` | int | Spotify popularity score (0–100) |
| `duration_ms` | int | Track duration in milliseconds |
| `danceability` | float | How suitable for dancing (0.0–1.0) |
| `energy` | float | Perceptual intensity and activity (0.0–1.0) |
| `valence` | float | Musical positiveness / happiness (0.0–1.0) |
| `tempo` | float | Estimated BPM |
| `acousticness` | float | Confidence of acoustic sound (0.0–1.0) |
| `instrumentalness` | float | Predicts no vocal content (0.0–1.0) |
| `speechiness` | float | Presence of spoken words (0.0–1.0) |
| `liveness` | float | Detects live audience (0.0–1.0) |
| `key` | int | Musical key (0–11, Pitches C–B) |
| `loudness` | float | Overall loudness in dB |
| `mode` | int | Major (1) or Minor (0) |
| `time_signature` | int | Estimated time signature |
| `track_genre` | str | Genre label |

---

## 🧩 Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | 1.56.0 | Web application framework |
| `pandas` | 3.0.2 | Data manipulation |
| `numpy` | 2.4.4 | Numerical computing |
| `scikit-learn` | 1.8.0 | TF-IDF, cosine similarity, scaling |
| `rapidfuzz` | 3.14.5 | Fuzzy string matching for song search |

<details>
<summary>View full dependency list</summary>

```
altair==6.0.0        attrs==26.1.0         blinker==1.9.0
cachetools==7.0.6    certifi==2026.2.25    charset-normalizer==3.4.7
click==8.3.2         colorama==0.4.6       gitdb==4.0.12
GitPython==3.1.46    idna==3.11            Jinja2==3.1.6
joblib==1.5.3        jsonschema==4.26.0    jsonschema-specifications==2025.9.1
MarkupSafe==3.0.3    narwhals==2.20.0      numpy==2.4.4
packaging==26.1      pandas==3.0.2         pillow==12.2.0
protobuf==7.34.1     pyarrow==23.0.1       pydeck==0.9.2
python-dateutil==2.9.0.post0               RapidFuzz==3.14.5
referencing==0.37.0  requests==2.33.1      rpds-py==0.30.0
scikit-learn==1.8.0  scipy==1.17.1         six==1.17.0
smmap==5.0.3         streamlit==1.56.0     tenacity==9.1.4
threadpoolctl==3.6.0 toml==0.10.2          tornado==6.5.5
typing_extensions==4.15.0                  tzdata==2026.1
urllib3==2.6.3       watchdog==6.0.0
```