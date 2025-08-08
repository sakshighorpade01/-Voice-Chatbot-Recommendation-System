import pickle
import streamlit as st
import requests
import os
import time

# ===============================
# CONFIG
# ===============================
# Get your TMDB API key from: https://www.themoviedb.org/settings/api
API_KEY = "dec4059796ccfb9a3b2a3bcac7ef6339"

# ===============================
# HELPER FUNCTIONS
# ===============================
def fetch_poster(movie_id):
    """Fetch movie poster from TMDB API with retries and fallback."""
    url = f"https://api.themoviedb.org/3/movie/{int(movie_id)}?api_key={API_KEY}&language=en-US"
    
    for attempt in range(3):  # retry up to 3 times
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get("poster_path")
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
            else:
                return "https://via.placeholder.com/500x750?text=No+Image"
        except requests.exceptions.RequestException:
            if attempt < 2:  # wait and retry
                time.sleep(1)
            else:  # all retries failed
                return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie):
    """Return top 5 recommended movie names and posters."""
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = int(movies.iloc[i[0]].movie_id)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    
    return recommended_movie_names, recommended_movie_posters

# ===============================
# STREAMLIT APP
# ===============================
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.header('🎬 Movie Recommender System')

# Load model files
try:
    movies = pickle.load(open('model/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('model/similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model files not found. Please ensure 'movie_list.pkl' and 'similarity.pkl' are in the 'model/' folder.")
    st.stop()

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendations'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            st.image(poster)
