import streamlit as st
from movie_recommender import get_recommendations, get_all_movie_titles
from song_recommender import (
    get_song_recommendations, get_songs_by_mood, get_songs_by_artist,
    get_all_song_titles, get_all_moods
)
from rapidfuzz import process

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Recommendation System",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── FONTS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400&family=DM+Serif+Display:ital@0;1&display=swap');
</style>
""", unsafe_allow_html=True)

# ── DARK MODE CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
:root {
    --bg:           #0d0f14;
    --bg2:          #12151c;
    --surface:      #181b24;
    --surface2:     #1e2130;
    --surface3:     #242840;
    --gold:         #e8a020;
    --gold-light:   #f5bc4a;
    --gold-pale:    #2a2010;
    --gold-deep:    #f0c060;
    --text:         #e8eaf0;
    --text2:        #9ea3b5;
    --text3:        #5c6180;
    --border:       #252a3a;
    --border-light: #1e2230;
}

/* ── BASE ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stMain"],
.main {
    background-color: var(--bg) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text) !important;
}

#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
/* Keep header so sidebar toggle button remains accessible */
[data-testid="stHeader"] { background: var(--bg) !important; border-bottom: 1px solid var(--border) !important; }
[data-testid="stToolbar"] { visibility: hidden !important; }

.block-container {
    padding: 2.5rem 3rem 3rem !important;
    max-width: 980px !important;
}

/* ── DISABLE SIDEBAR COLLAPSE BUTTON ── */
[data-testid="stSidebarCollapseButton"] {
    display: none !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div { padding: 2rem 1.4rem !important; }

/* ── SIDEBAR NAV RADIO ── */
.stRadio > label { display: none !important; }
.stRadio > div {
    gap: 2px !important;
    flex-direction: column !important;
}
.stRadio > div > label {
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    padding: 10px 14px !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    color: var(--text2) !important;
    cursor: pointer !important;
    border: 1px solid transparent !important;
    transition: all 0.2s ease !important;
    font-family: 'Inter', sans-serif !important;
}
.stRadio > div > label:hover {
    background: var(--surface2) !important;
    color: var(--gold-light) !important;
    border-color: var(--border) !important;
}

/* Force nav text visible across all Streamlit versions */
[data-testid="stSidebar"] .stRadio label p,
[data-testid="stSidebar"] .stRadio label span,
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #9ea3b5 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    visibility: visible !important;
    opacity: 1 !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover p,
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover span {
    color: #f5bc4a !important;
}
[data-testid="stSidebar"] input[type="radio"] { display: none !important; }

/* ── EYEBROW ── */
.eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 3px;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 14px;
}
.eyebrow::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border), transparent);
}

/* ── PAGE TITLE ── */
.page-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(34px, 4vw, 52px);
    font-weight: 400;
    line-height: 1.1;
    color: var(--text);
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}

.page-sub {
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    color: var(--text2);
    line-height: 1.7;
    font-weight: 300;
    margin-bottom: 2rem;
}

/* ── STATS STRIP ── */
.stats-strip {
    display: flex;
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    background: var(--surface);
    margin-bottom: 2.5rem;
}
.stat-cell {
    flex: 1;
    padding: 20px 24px;
    border-right: 1px solid var(--border-light);
}
.stat-cell:last-child { border-right: none; }
.stat-num {
    font-family: 'DM Serif Display', serif;
    font-size: 32px;
    font-weight: 400;
    color: var(--gold-deep);
    line-height: 1;
}
.stat-lbl {
    font-family: 'Inter', sans-serif;
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text3);
    margin-top: 5px;
}

/* ── FEATURE CARDS ── */
.feat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    position: relative;
    overflow: hidden;
    transition: all 0.25s ease;
    height: 100%;
}
.feat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--gold), transparent);
}
.feat-card:hover {
    border-color: var(--border-light);
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    background: var(--surface2);
}
.feat-icon {
    width: 40px; height: 40px;
    border-radius: 10px;
    background: var(--gold-pale);
    border: 1px solid rgba(232,160,32,0.2);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    margin-bottom: 16px;
}
.feat-title {
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 6px;
    letter-spacing: -0.01em;
}
.feat-desc {
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    color: var(--text2);
    line-height: 1.7;
    font-weight: 300;
}
.feat-tag {
    display: inline-block;
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 20px;
    background: var(--surface3);
    color: var(--gold);
    border: 1px solid rgba(232,160,32,0.15);
    margin-top: 12px;
    margin-right: 5px;
}

/* ── MOVIE CARDS ── */
.movie-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 18px;
    transition: all 0.2s ease;
}
.movie-card:hover {
    border-color: rgba(232,160,32,0.3);
    background: var(--surface2);
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    transform: translateX(3px);
}
.movie-rank {
    font-family: 'DM Serif Display', serif;
    font-size: 24px;
    font-weight: 400;
    color: var(--text3);
    min-width: 34px;
    text-align: center;
    flex-shrink: 0;
}
.movie-info { flex: 1; min-width: 0; }
.movie-title {
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    font-weight: 500;
    color: var(--text);
    margin-bottom: 4px;
    letter-spacing: -0.01em;
}
.movie-score {
    font-family: 'DM Serif Display', serif;
    font-size: 22px;
    color: var(--gold);
    font-weight: 400;
    flex-shrink: 0;
}
.genre-pill {
    display: inline-block;
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 500;
    padding: 2px 8px;
    border-radius: 20px;
    background: var(--surface3);
    color: var(--text2);
    border: 1px solid var(--border);
    margin-right: 4px;
    margin-bottom: 2px;
}
.match-bar-wrap {
    height: 2px;
    background: var(--border);
    border-radius: 2px;
    margin-top: 10px;
    overflow: hidden;
}
.match-bar-fill {
    height: 100%;
    border-radius: 2px;
    background: linear-gradient(90deg, var(--gold), var(--gold-light));
}

/* ── SONG CARDS ── */
.song-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 13px 18px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 14px;
    transition: all 0.2s ease;
}
.song-card:hover {
    border-color: rgba(232,160,32,0.3);
    background: var(--surface2);
    transform: translateX(4px);
}
.song-avatar {
    width: 42px; height: 42px;
    border-radius: 10px;
    background: linear-gradient(135deg, var(--surface3), var(--gold-pale));
    border: 1px solid rgba(232,160,32,0.15);
    display: flex; align-items: center; justify-content: center;
    font-size: 17px;
    flex-shrink: 0;
}
.song-name {
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 500;
    color: var(--text);
    letter-spacing: -0.01em;
}
.song-artist {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    color: var(--text2);
    margin-top: 3px;
    font-weight: 300;
}
.song-score {
    font-family: 'DM Serif Display', serif;
    font-size: 18px;
    color: var(--gold);
    font-weight: 400;
    flex-shrink: 0;
}

/* ── METRIC CARDS ── */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.2s ease;
}
.metric-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}
.metric-card:hover {
    background: var(--surface2);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.metric-num {
    font-family: 'DM Serif Display', serif;
    font-size: 44px;
    font-weight: 400;
    color: var(--gold-deep);
    line-height: 1;
    letter-spacing: -0.02em;
}
.metric-lbl {
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text3);
    margin-top: 8px;
}

/* ── INPUTS ── */
.stTextInput > div > div > input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(232,160,32,0.5) !important;
    box-shadow: 0 0 0 3px rgba(232,160,32,0.08) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--text3) !important; }

/* ── SELECTBOX ── */
div[data-baseweb="select"] > div {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text) !important;
}
div[data-baseweb="select"] svg { color: var(--text2) !important; }
div[data-baseweb="popover"],
div[data-baseweb="menu"] {
    background: var(--surface2) !important;
}
li[role="option"] {
    background: var(--surface2) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}
li[role="option"]:hover { background: var(--surface3) !important; }

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #e8a020, #d4901a) !important;
    color: #000000 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 11px 28px !important;
    font-size: 13px !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s ease !important;
    opacity: 1 !important;
}
.stButton > button p,
.stButton > button span {
    color: #000000 !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #f5bc4a, #e8a020) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(232,160,32,0.3) !important;
}

/* ── TABS ── */
div[data-testid="stTabs"] button {
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--text2) !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--gold-deep) !important;
    border-bottom-color: var(--gold) !important;
}

/* ── ALERTS ── */
div[data-testid="stAlert"] {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    border-radius: 10px !important;
}

/* ── MISC ── */
hr { border-color: var(--border) !important; margin: 2rem 0 !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

.ornament {
    text-align: center;
    color: var(--text3);
    font-size: 12px;
    letter-spacing: 12px;
    margin: 2rem 0 0.5rem;
}

.mood-badge {
    display: inline-block;
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 20px;
    background: var(--surface3);
    color: var(--gold);
    border: 1px solid rgba(232,160,32,0.15);
    flex-shrink: 0;
}
</style>
""", unsafe_allow_html=True)


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style="margin-bottom:2.5rem">
  <div style="font-family:'Inter',sans-serif;font-size:9px;font-weight:600;
    letter-spacing:3px;color:#e8a020;text-transform:uppercase;
    border-bottom:1px solid #252a3a;padding-bottom:0.9rem;margin-bottom:1rem">  
  </div>
  <div style="font-family:'DM Serif Display',serif;font-size:20px;
    font-weight:400;color:#e8eaf0;line-height:1.3;letter-spacing:-0.01em">
    Recommendation<br>
    <em style="color:#e8a020;font-style:italic">System</em>
  </div>
</div>
<div style="font-family:'Inter',sans-serif;font-size:9px;font-weight:600;
  letter-spacing:2.5px;color:#5c6180;text-transform:uppercase;
  margin-bottom:10px">Navigate</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigate",
    ["✦  Home", "🎬  Movies", "🎵  Songs", "📊  Analytics"],
    label_visibility="collapsed"
)



# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "✦  Home":
    st.markdown('<div class="eyebrow">Curated Recommendations</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="page-title">Discover What You<br><em style="color:#e8a020;font-style:italic">Love</em></div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stats-strip">
      <div class="stat-cell"><div class="stat-num">9,742</div><div class="stat-lbl">Movies</div></div>
      <div class="stat-cell"><div class="stat-num">2,000</div><div class="stat-lbl">Songs</div></div>
      <div class="stat-cell"><div class="stat-num">124</div><div class="stat-lbl">Artists</div></div>
      <div class="stat-cell"><div class="stat-num">6</div><div class="stat-lbl">Moods</div></div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="feat-card">
          <div class="feat-icon">🎬</div>
          <div class="feat-title">Movie Engine</div>
          <div class="feat-desc">TF-IDF genre vectors with cosine similarity ranking across 9,742 titles.</div>
          <span class="feat-tag">Genre Matching</span>
          <span class="feat-tag">Ranked Results</span>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="feat-card">
          <div class="feat-icon">🎵</div>
          <div class="feat-title">Song Engine</div>
          <div class="feat-desc">8-dimensional audio fingerprint — energy, valence, danceability, tempo.</div>
          <span class="feat-tag">Audio Similarity</span>
          <span class="feat-tag">Mood Detection</span>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="feat-card">
          <div class="feat-icon">📊</div>
          <div class="feat-title">Analytics</div>
          <div class="feat-desc">Live dataset metrics — total movies, songs, and unique artists.</div>
          <span class="feat-tag">Stats</span>
          <span class="feat-tag">Live Counts</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="ornament">· · ✦ · ·</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MOVIES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🎬  Movies":
    st.markdown('<div class="eyebrow">Cinema</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Movie <em style="color:#e8a020;font-style:italic">Recommender</em></div>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Select a film and we\'ll surface the most similar titles from our catalogue.</p>', unsafe_allow_html=True)

    movie_list = get_all_movie_titles()
    selected_movie = st.selectbox("Select Movie", movie_list, label_visibility="collapsed")

    if st.button("Find Similar Movies"):
        results = get_recommendations(selected_movie)
        if not results.empty:
            st.markdown(f"""
            <div class="eyebrow" style="margin-top:2rem">
              Results for &nbsp;<em style="font-style:italic;color:#e8a020">{selected_movie}</em>
            </div>""", unsafe_allow_html=True)

            emojis = ["🎬","🎥","🎞️","📽️","🍿","🎦","🎭","🎪","🎠","🎡"]
            for i, (_, row) in enumerate(results.iterrows()):
                genres = str(row["genres"]).split("|")
                pills  = "".join(f'<span class="genre-pill">{g.strip()}</span>' for g in genres)
                score  = row["match_score"]
                st.markdown(f"""
                <div class="movie-card">
                  <div class="movie-rank">{str(i+1).zfill(2)}</div>
                  <div class="movie-info">
                    <div class="movie-title">{emojis[i%len(emojis)]} &nbsp;{row['title']}</div>
                    <div style="margin-top:5px">{pills}</div>
                    <div class="match-bar-wrap">
                      <div class="match-bar-fill" style="width:{min(score,100)}%"></div>
                    </div>
                  </div>
                  <div class="movie-score">{score}%</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No recommendations found. Try a different title.")

    st.markdown('<div class="ornament">· · ✦ · ·</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SONGS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🎵  Songs":
    st.markdown('<div class="eyebrow">Music</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Bollywood Song <em style="color:#e8a020;font-style:italic">Finder</em></div>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Discover tracks by audio similarity, mood, or your favourite artist.</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔍  Search by Song", "🎭  By Mood", "🎤  By Artist"])
    EMOJIS = ["🎸","🎹","🎷","🎵","🎶","🎻","🪗","🥁","🎺","🪘"]
    MOOD_ICONS = {"Happy":"😊","Sad":"😢","Romantic":"💕","Party":"🎉","Energetic":"⚡","Chill":"🌊"}

    with tab1:
        song_list = get_all_song_titles()
        query = st.text_input("Song Search", placeholder="Type a Bollywood song name…", label_visibility="collapsed")
        if st.button("Find Similar Songs"):
            if not query.strip():
                st.warning("Please enter a song name.")
                st.stop()
            match = process.extractOne(query, song_list)
            if match is None or match[1] < 60:
                st.error("Song not found — try a different spelling.")
                st.stop()
            selected = match[0]
            st.markdown(f'<div class="eyebrow" style="margin-top:1.5rem">Similar to &nbsp;<em style="font-style:italic;color:#e8a020">{selected}</em></div>', unsafe_allow_html=True)
            results = get_song_recommendations(selected)
            if not results.empty:
                for i, (_, row) in enumerate(results.iterrows()):
                    st.markdown(f"""
                    <div class="song-card">
                      <div class="song-avatar">{EMOJIS[i%len(EMOJIS)]}</div>
                      <div style="flex:1;min-width:0">
                        <div class="song-name">{row['track_name']}</div>
                        <div class="song-artist">{row['artists']}</div>
                      </div>
                      <div class="song-score">{row['match_score']}%</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.error("No similar songs found.")

    with tab2:
        moods = get_all_moods()
        selected_mood = st.selectbox("Select Mood", moods,
            format_func=lambda m: f"{MOOD_ICONS.get(m,'🎵')}  {m}",
            label_visibility="collapsed")
        if st.button("Find Songs by Mood"):
            results = get_songs_by_mood(selected_mood)
            if not results.empty:
                st.markdown(f'<div class="eyebrow" style="margin-top:1.5rem">{MOOD_ICONS.get(selected_mood,"🎵")} &nbsp;<em style="font-style:italic;color:#e8a020">{selected_mood}</em> &nbsp;picks</div>', unsafe_allow_html=True)
                for i, (_, row) in enumerate(results.iterrows()):
                    icon = MOOD_ICONS.get(selected_mood, "🎵")
                    st.markdown(f"""
                    <div class="song-card">
                      <div class="song-avatar">{icon}</div>
                      <div style="flex:1;min-width:0">
                        <div class="song-name">{row['track_name']}</div>
                        <div class="song-artist">{row['artists']}</div>
                      </div>
                      <span class="mood-badge">{row['mood']}</span>
                    </div>""", unsafe_allow_html=True)

    with tab3:
        artist_name = st.text_input("Artist Name", value="Arijit Singh",
            placeholder="e.g. Arijit Singh", label_visibility="collapsed")
        if st.button("Search Artist Songs"):
            results = get_songs_by_artist(artist_name)
            if not results.empty:
                st.markdown(f'<div class="eyebrow" style="margin-top:1.5rem">Songs by &nbsp;<em style="font-style:italic;color:#e8a020">{artist_name}</em></div>', unsafe_allow_html=True)
                for i, (_, row) in enumerate(results.iterrows()):
                    st.markdown(f"""
                    <div class="song-card">
                      <div class="song-avatar">{EMOJIS[i%len(EMOJIS)]}</div>
                      <div style="flex:1;min-width:0">
                        <div class="song-name">{row['track_name']}</div>
                        <div class="song-artist">{row['artists']}</div>
                      </div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning(f"No songs found for '{artist_name}'.")

    st.markdown('<div class="ornament">· · ✦ · ·</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊  Analytics":
    from song_recommender import songs
    from movie_recommender import movies

    st.markdown('<div class="eyebrow">Insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Dataset <em style="color:#e8a020;font-style:italic">Analytics</em></div>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">A live view of your dataset — counts, moods, and top artists.</p>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-num">{len(movies):,}</div><div class="metric-lbl">Total Movies</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-num">{len(songs):,}</div><div class="metric-lbl">Hindi Songs</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-num">{songs["artists"].nunique():,}</div><div class="metric-lbl">Unique Artists</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="ornament">· · ✦ · ·</div>', unsafe_allow_html=True)