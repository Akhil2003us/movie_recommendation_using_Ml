import streamlit as st
import pickle
import requests
import pandas as pd
import os
import gdown


if not os.path.exists("similarity.pkl"):
    url = url = "https://drive.google.com/uc?id=1kXal772M6TcCxEj3cZp5Jmbb1mJdlHNx"
    gdown.download(url, "similarity.pkl", quiet=False)



st.set_page_config(page_title="Movie Recommender System", layout="wide")
st.header("🎬 Movie Recommender System")

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500/"
PLACEHOLDER_POSTER = "https://placehold.co/500x750/333/FFFFFF?text=No+Poster"

movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movies_list = movies['title'].values

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={'3beffc27a0ba60c9f0b165a4e45a7727'}&language=en-US"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return POSTER_BASE_URL + poster_path
    except:
        pass
    return PLACEHOLDER_POSTER

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    movie_names = []
    movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]]['id']
        movie_names.append(movies.iloc[i[0]]['title'])
        movie_posters.append(fetch_poster(movie_id))

    return movie_names, movie_posters

selected_movie = st.selectbox("Select a movie", movies_list)

if st.button("Show Recommendation"):
    movie_names, movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for col, name, poster in zip(cols, movie_names, movie_posters):
        with col:
            st.text(name)
            st.image(poster)  