# importing necessary libraries
from flask import Flask, request, render_template, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import psycopg2
import time
import json
import urllib.request

app = Flask(__name__, template_folder='template')

# secret key and cookie for web app
app.secret_key = ''
app.config['SESSION_COOKIE_NAME'] = ''
TOKEN_INFO = ''
IMDB_api_key = ''


# function to connect to database where spotify data will be inserted
def database_connect():
    conn = psycopg2.connect(
        database="Spotifydata",
        user="postgres",
        password='',
        host="localhost",
        port="5432"
    )
    return conn


# connect to database and create user table to store access token and movies
conn = database_connect()
cur = conn.cursor()
cur.execute(
    'CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, access_token text, movies text[])')

# route to login page


@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


# route to redirect page
@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    cur.execute('INSERT INTO users (access_token) VALUES (%s) RETURNING id',
                (token_info['access_token'],))
    session['user_id'] = cur.fetchone()[0]
    conn.commit()
    return redirect(url_for('recommend', _external=True))

# function to convert dictionary to list


def dict_to_list(dict):
    list = [value for key, value in dict.items()]
    list2 = [item for list[0] in list for item in list[0]]
    i = 0
    result = []
    for v in list2:
        result = result + [tuple((i, v))]
        i = i + 1
    return result


# function that get movies from TMDB api


def get_movies():
    list_movies = []
    i = 0
    for page in range(1, 200):
        response_TMDB = urllib.request.urlopen(
            'https://api.themoviedb.org/3/movie/popular?api_key=apikey&language=en-US&page={page}')
        TMDB_data = response_TMDB.read()
        dict = json.loads(TMDB_data)
        for film in dict['results']:
            list_movies = list_movies + \
                [tuple((i, film["original_title"], film["genre_ids"]))]
            i = i+1
    return list_movies

# function to store movies into database


def store_movies(movies_list):
    cur.execute('UPDATE users SET movies = %s WHERE id = %s',
                (movies_list, session['user_id']))
    conn.commit()
# function to match spotify genres to movie genres


def match_genres(genres, movies):
    movie_list = []
    for genre in genres:
        if "rock" in genre[1]:
            for movie in movies:
                if 28 in movie[2] or 10752 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "rap" in genre[1]:
            for movie in movies:
                if 28 in movie[2] or 878 in movie[2] or 53 in movie[2] or 18 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "hip" in genre[1] or "hop" in genre[1]:
            for movie in movies:
                if 28 in movie[2] or 53 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "pop" in genre[1]:
            for movie in movies:
                if 12 in movie[2] or 10749 in movie[2] or 10770 in movie[2] or 18 in movie[2] or 35 in movie[2] or 10751 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "orchestra" in genre[1]:
            for movie in movies:
                if 12 in movie[2] or 10402 in movie[2] or 99 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "folk" in genre[1]:
            for movie in movies:
                if 12 in movie[2] or 14 in movie[2] or 36 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "anime" in genre[1]:
            for movie in movies:
                if 16 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "comedy" in genre[1]:
            for movie in movies:
                if 35 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "sad" in genre[1]:
            for movie in movies:
                if 18 in movie[2] or 80 in movie[2] or 10749 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "soul" in genre[1]:
            for movie in movies:
                if 80 in movie[2] or 18 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "indie" in genre[1]:
            for movie in movies:
                if 99 in movie[2] or 14 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "classic" in genre[1]:
            for movie in movies:
                if 99 in movie[2] or 36 in movie[2] or 10752 in movie[2] or 9648 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "blues" in genre[1]:
            for movie in movies:
                if 18 in movie[2] or 80 in movies[2] or 9648 in movies[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "happy" in genre[1]:
            for movie in movies:
                if 10751 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "opera" in genre[1]:
            for movie in movies:
                if 36 in movie[2] or 18 in movie[2] or 10479 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "old" in genre[1]:
            for movie in movies:
                if 36 in movie[2] or 10752 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "metal" in genre[1]:
            for movie in movies:
                if 27 in movie[2] or 53 in movie[2] or 878 in movie[2] or 28 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "emo" in genre[1]:
            for movie in movies:
                if 27 in movie[2] or 53 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "punk" in genre[1]:
            for movie in movies:
                if 27 in movie[2] or 53 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "grunge" in genre[1]:
            for movie in movies:
                if 80 in movie[2] or 27 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "show tunes" in genre[1]:
            for movie in movies:
                if 10402 in movie[2] or 10749 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "jazz" in genre[1]:
            for movie in movies:
                if 80 in movie[2] or 9648 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "k-pop" in genre[1]:
            for movie in movies:
                if 10749 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "techno" in genre[1]:
            for movie in movies:
                if 878 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "dubstep" in genre[1]:
            for movie in movies:
                if 878 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "western" in genre[1]:
            for movie in movies:
                if 37 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
        if "country" in genre[1]:
            for movie in movies:
                if 37 in movie[2] or 10749 in movie[2] or 18 in movie[2]:
                    if movie[1] not in movie_list:
                        movie_list = movie_list + [movie[1]]
    return movie_list

# route to where genres are gotten


@ app.route('/recommend')
# function that gets genres from spotify and displays movies
def recommend():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        redirect(url_for("login", _external=False))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    genres = sp.recommendation_genre_seeds()
    genre_list = dict_to_list(genres)
    list_movies = get_movies()
    movies_list = match_genres(genre_list, list_movies)
    store_movies(movies_list)
    cur.execute('SELECT movies FROM users WHERE id = %s',
                (session['user_id'],))
    conn.commit()
    movies = cur.fetchone()[0]
    movies = movies[0:50]

    return render_template('muvie.html', movies=movies)

# checks if token is expired


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


# spotify api stuff ***dont post clientsecret to github***
clientID = ""
clientSecret = ""

# OAuth information


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id="",
        client_secret="",
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read")
