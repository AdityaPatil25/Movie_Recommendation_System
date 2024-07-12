import pickle

import pandas as pd
import streamlit as st
import requests


def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']




def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:7]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies_ = pickle.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_)
similarity = pickle.load(open('similarity.pkl', 'rb'))


selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)


def create_movie_grid(name,poster, rows, cols):
    grid = []
    movie_index = 0
    for _ in range(rows):
        row = st.columns(cols)
        for col in row:
            if movie_index < len(name):
                title = name[movie_index]
                img = poster[movie_index]
                col.image(img, use_column_width=True)
                col.write(title)
                movie_index += 1
        grid.append(row)


if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    create_movie_grid(recommended_movie_names, recommended_movie_posters, 2, 3)


