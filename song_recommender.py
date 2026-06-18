import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import os

BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, 'data', 'hindi_songs.csv')

songs = pd.read_csv(file_path)

# --- STANDARDIZE COLUMN NAMES ---
songs = songs.rename(columns={
    'Name': 'track_name',
    'Artists': 'artists',
    'Popularity': 'popularity'
})

# --- BASIC CLEANING ---
songs = songs.dropna(subset=['track_name', 'artists']).reset_index(drop=True)

songs = songs[songs['artists'].str.contains(
    'Arijit|Shreya|Pritam|Neha|Atif|KK|Sonu Nigam|Sunidhi|Amit Trivedi|Sachin|Jubin',
    case=False, na=False
)]

# ALSO filter by track name (important)
songs = songs[songs['track_name'].str.contains(
    '[a-zA-Z]', regex=True
)]

# 🔴 LIMIT AFTER FILTERING
if len(songs) > 2000:
    songs = songs.sort_values('popularity', ascending=False).head(2000)

# 🔴 RESET INDEX AGAIN (VERY IMPORTANT)
songs = songs.reset_index(drop=True)

# ================= FEATURE SET =================
audio_features = [
    'danceability', 'energy', 'valence', 'tempo',
    'acousticness', 'instrumentalness',
    'speechiness', 'liveness'
]

available_features = [f for f in audio_features if f in songs.columns]

# 🔴 HARD FAIL if no features (prevents fake AI)
if len(available_features) == 0:
    raise ValueError(
        "Dataset has NO audio features. Use a proper Spotify dataset."
    )

# ================= NORMALIZATION =================
scaler = MinMaxScaler()
songs_features = songs[available_features].fillna(0)
songs_features_scaled = scaler.fit_transform(songs_features)

# ================= SIMILARITY =================
audio_similarity = cosine_similarity(songs_features_scaled)

# ================= INDEX MAPPING =================
songs['unique_key'] = songs['track_name'] + " - " + songs['artists']
song_indices = pd.Series(songs.index, index=songs['unique_key']).drop_duplicates()

# ================= MOOD LOGIC =================
def assign_mood(row):
    valence = row.get('valence', 0.5)
    energy = row.get('energy', 0.5)
    danceability = row.get('danceability', 0.5)

    if valence > 0.6 and energy > 0.6:
        return 'Happy'
    elif valence > 0.5 and danceability > 0.7:
        return 'Party'
    elif valence < 0.4 and energy < 0.5:
        return 'Sad'
    elif valence > 0.5 and energy < 0.5:
        return 'Romantic'
    elif energy > 0.7:
        return 'Energetic'
    else:
        return 'Chill'

# Apply mood
songs['mood'] = songs.apply(assign_mood, axis=1)

# ================= RECOMMENDER =================
def get_song_recommendations(title, n=10):
    try:
        if title not in song_indices:
            return pd.DataFrame()

        idx = song_indices[title]
        if isinstance(idx, pd.Series):
            idx = idx.iloc[0]

        sim_scores = list(enumerate(audio_similarity[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:n+1]

        song_idx_list = [i[0] for i in sim_scores]
        scores = [round(i[1] * 100, 2) for i in sim_scores]

        result = songs.iloc[song_idx_list][['track_name', 'artists']].copy()
        result['match_score'] = scores
        return result

    except KeyError:
        return pd.DataFrame()

# ================= FILTER FUNCTIONS =================
def get_songs_by_mood(mood, n=10):
    mood_songs = songs[songs['mood'] == mood]
    if 'popularity' in mood_songs.columns:
        mood_songs = mood_songs.sort_values('popularity', ascending=False)
    return mood_songs[['track_name', 'artists', 'mood']].head(n)


def get_songs_by_artist(artist_name, n=10):
    matches = songs[songs['artists'].str.contains(artist_name, case=False, na=False)]
    if 'popularity' in matches.columns:
        matches = matches.sort_values('popularity', ascending=False)
    return matches[['track_name', 'artists']].head(n)


def get_top_songs(n=20):
    if 'popularity' in songs.columns:
        return songs.nlargest(n, 'popularity')[['track_name', 'artists', 'popularity']]
    return songs.head(n)[['track_name', 'artists']]


def get_all_song_titles():
    return sorted(songs['unique_key'].tolist())


def get_all_artists():
    all_artists = []
    for artist_str in songs['artists'].dropna():
        all_artists.extend([a.strip() for a in str(artist_str).split(',')])
    return sorted(list(set(all_artists)))


def get_all_moods():
    return sorted(songs['mood'].unique().tolist())