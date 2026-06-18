import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv('data/movies.csv')

tfidf = TfidfVectorizer(token_pattern=r"[^|]+")
tfidf_matrix = tfidf.fit_transform(movies['genres'])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()


def get_recommendations(title, n=10):
    try:
        idx = indices[title]
        if isinstance(idx, pd.Series):
            idx = idx.iloc[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:n+1]
        movie_indices = [i[0] for i in sim_scores]
        scores = [round(i[1] * 100, 2) for i in sim_scores]
        result = movies.iloc[movie_indices][['title', 'genres']].copy()
        result['match_score'] = scores
        return result
    except KeyError:
        return pd.DataFrame()


def get_all_movie_titles():
    return sorted(movies['title'].unique().tolist())