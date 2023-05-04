import json
from flask import Flask, request, redirect, g, render_template
import requests
from urllib.parse import quote
import psycopg2
import os
from dotenv import load_dotenv

# Authentication Steps, paramaters, and responses are defined at https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.


app = Flask(__name__)
DEBUG_ENV = os.getenv("DEBUG_ENV", "dev")
TABLENAME = "movie_list"
if DEBUG_ENV != "dev":
    load_dotenv(".env")
    REQUIRED_ENV_VARS = {"database", "host", "user", "password", "port"}
    diff = REQUIRED_ENV_VARS.difference(os.environ)
    if diff > 0:
        raise EnvironmentError(f"Failed because {diff} are not set")
    database = os.environ["database"]
    host = os.environ["host"]
    user = os.environ["user"]
    password = os.environ["password"]
    port = os.environ["port"]
    config = (database, host, user, password, port)

load_dotenv(".env")
#  Client Keys
CLIENT_ID = os.environ["client_id"]
CLIENT_SECRET = os.environ["client_secret"]

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = f"{SPOTIFY_API_BASE_URL}/{API_VERSION}"

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000
REDIRECT_URI = f"{CLIENT_SIDE_URL}:{PORT}/callback/q"
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID,
}


@app.route("/example")
def example():
    example_data = {
        "page": 1,
        "results": [
            {
                "poster_path": "/e1mjopzAS2KNsvpbpahQ1a6SkSn.jpg",
                "overview": "From DC Comics comes the Suicide Squad, an antihero team of incarcerated supervillains who act as deniable assets for the United States government, undertaking high-risk black ops missions in exchange for commuted prison sentences.",
                "release_date": "2016-08-03",
                "genre_ids": [14, 28, 80],
                "id": 297761,
                "original_title": "Suicide Squad",
                "original_language": "en",
                "title": "Suicide Squad",
                "backdrop_path": "/ndlQ2Cuc3cjTL7lTynw6I4boP4S.jpg",
                "popularity": 48.261451,
                "vote_count": 1466,
                "vote_average": 5.91,
            },
            {
                "poster_path": "/lFSSLTlFozwpaGlO31OoUeirBgQ.jpg",
                "overview": "The most dangerous former operative of the CIA is drawn out of hiding to uncover hidden truths about his past.",
                "release_date": "2016-07-27",
                "genre_ids": [28, 53],
                "id": 324668,
                "original_title": "Jason Bourne",
                "original_language": "en",
                "title": "Jason Bourne",
                "backdrop_path": "/AoT2YrJUJlg5vKE3iMOLvHlTd3m.jpg",
                "popularity": 30.690177,
                "vote_count": 649,
                "vote_average": 5.25,
            },
            {
                "poster_path": "/hU0E130tsGdsYa4K9lc3Xrn5Wyt.jpg",
                "overview": "One year after outwitting the FBI and winning the public’s adulation with their mind-bending spectacles, the Four Horsemen resurface only to find themselves face to face with a new enemy who enlists them to pull off their most dangerous heist yet.",
                "release_date": "2016-06-02",
                "genre_ids": [28, 12, 35, 80, 9648, 53],
                "id": 291805,
                "original_title": "Now You See Me 2",
                "original_language": "en",
                "title": "Now You See Me 2",
                "backdrop_path": "/zrAO2OOa6s6dQMQ7zsUbDyIBrAP.jpg",
                "popularity": 29.737342,
                "vote_count": 684,
                "vote_average": 6.64,
            }
        ],
        "total_results": 19629,
        "total_pages": 982,
    }
    example_data = example_data["results"]
    return render_template("example.html", sorted_array=example_data)


@app.route("/")
def index():
    # Auth Step 1: Authorization
    url_args = "&".join(
        [f"{key}={quote(val)}" for key, val in auth_query_parameters.items()]
    )
    auth_url = f"{SPOTIFY_AUTH_URL}/?{url_args}"
    return redirect(auth_url)

@app.route("/test/q")
def test():
    test_data={
  "genres": ["acoustic", "afrobeat", "alt-rock", "alternative", "ambient", "anime",
             "black-metal", "bluegrass", "blues", "bossanova", "brazil", "breakbeat", "british", "cantopop", 
             "chicago-house", "children", "chill", "classical", "club", "comedy", "country", "dance", "dancehall", 
             "death-metal", "deep-house", "detroit-techno", "disco", "disney", "drum-and-bass", "dub", "dubstep", "edm", 
             "electro", "electronic", "emo", "folk", "forro", "french", "funk", "garage", "german", "gospel", "goth", "grindcore", 
             "groove", "grunge", "guitar", "happy", "hard-rock", "hardcore", "hardstyle", "heavy-metal", "hip-hop", "holidays",
               "honky-tonk", "house", "idm", "indian", "indie", "indie-pop", "industrial", "iranian", "j-dance", "j-idol", "j-pop",
               "j-rock", "jazz", "k-pop", "kids", "latin", "latino", "malay", "mandopop", "metal", "metal-misc", "metalcore", 
               "minimal-techno", "movies", "mpb", "new-age", "new-release", "opera", "pagode", "party", "philippines-opm", "piano", 
               "pop", "pop-film", "post-dubstep", "power-pop", "progressive-house", "psych-rock", "punk", "punk-rock", "r-n-b", 
               "rainy-day", "reggae", "reggaeton", "road-trip", "rock", "rock-n-roll", "rockabilly", "romance", "sad", "salsa", 
               "samba", "sertanejo", "show-tunes", "singer-songwriter", "ska", "sleep", "songwriter", "soul", "soundtracks",
                 "spanish", "study", "summer", "swedish", "synth-pop", "tango", "techno", "trance", "trip-hop", "turkish", 
                 "work-out", "world-music"]
    }
    test_data = test_data["genres"]
    return render_template("index.html", sorted_array=test_data)

@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args["code"]
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization": f"Bearer {access_token}"}

    # Get profile data
    user_profile_api_endpoint = f"{SPOTIFY_API_URL}/me"
    profile_response = requests.get(
        user_profile_api_endpoint, headers=authorization_header
    )
    profile_data = json.loads(profile_response.text)

    # Get user playlist data
    playlist_api_endpoint = f'{profile_data["href"]}/playlists'
    playlists_response = requests.get(
        playlist_api_endpoint, headers=authorization_header
    )
    playlist_data = json.loads(playlists_response.text)
    
    # get genre
    # topitem_api_endpoint= f'{SPOTIFY_API_URL}/me/top/artists'
    # topitem_genre=requests.get(
    #     topitem_api_endpoint, headers=authorization_header
    # )
    # print(str(topitem_genre))
    # topitem_data=topitem_genre.json()
    # json.loads(topitem_genre.text)

    # Combine profile and playlist data to display
    display_arr = [profile_data] + playlist_data["items"]
    # display_arr = topitem_data["items"]
    # display_genres= [genre for genres in display_arr["genres"] for genre in genres]

    return render_template("index.html", sorted_array=display_arr)


api_url = "https://catfact.ninja/fact"


@app.route("/callapi")
def call_api():
    response = requests.get(api_url)
    return response.json()


@app.get("/db/select/<user_id>")
def read_db(user_id: str):
    some_information_about_user = (
        f"pretend it queries user {{{user_id}}} in the database. (placeholder in dev)"
    )
    if DEBUG_ENV != "dev":
        try:
            # connect to the PostgreSQL database
            conn = psycopg2.connect(config)  # set in .env, don't publish .env to github
            # create a new cursor
            cursor = conn.cursor()
            # execute SELECT statement
            cursor.execute(f"SELECT * FROM {TABLENAME} c WHERE c.user_id = {user_id}")
            # get all records back
            some_information_about_user = cursor.fetchall()
            # close communication with the database
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    return some_information_about_user


@app.route(
    "/db/update/<user_id>",
    methods=(lambda: ["GET", "POST"], lambda: ["POST"])[DEBUG_ENV != "dev"](),
)
def update_user_movie_recommendation(user_id: str):
    def create_user_if_not_exist(user_id: str, cursor):
        # check user exist
        cursor.execute(
            f"SELECT exists ( SELECT 1 FROM {TABLENAME} c WHERE c.user_id = {user_id})"
        )
        if not cursor.fetchone()[0]:
            # insert user if not exist
            cursor.execute(
                f"INSERT INTO {TABLENAME}(user_id) VALUES({user_id}) RETURNING user_id;"
            )
        return cursor.fetchone()[0]

    movie_list = f"pretend it updates user {{{user_id}}} with movie_list [Test,None,Nah,OMG,Ahh] in the database. (placeholder in dev)"
    updated_rows = 0
    if DEBUG_ENV != "dev":
        movie_list = call_api()["movie_list"]
        try:
            # connect to the PostgreSQL database
            conn = psycopg2.connect(config)  # set in .env, don't publish .env to github
            # create a new cursor
            cursor = conn.cursor()
            # create user if not exist
            if not create_user_if_not_exist(user_id, cursor):
                raise ValueError(
                    "create_user_if_not_exist did something unexpected, check database if something is wrong"
                )
            # execute UPDATE query
            cursor.execute(
                f"UPDATE {TABLENAME} SET movie_list = {movie_list} WHERE user_id = {user_id}"
            )
            # get the number of updated rows
            updated_rows = cursor.rowcount
            # Commit the changes to the database
            conn.commit()
            # Close communication with the PostgreSQL database
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    return movie_list


if __name__ == "__main__":
    app.run(debug=True, port=PORT)
