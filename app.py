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
FLASK_ENV = os.getenv("FLASK_ENV", "dev")
TABLENAME = "movie_list"
if FLASK_ENV != "dev":
    load_dotenv(".env")
    REQUIRED_ENV_VARS = {"database", "host", "user", "password", "port"}
    if diff := REQUIRED_ENV_VARS.difference(os.environ):
        raise EnvironmentError(f"Failed because {diff} are not set")
    database = os.environ["database"]
    host = os.environ["host"]
    user = os.environ["user"]
    password = os.environ["password"]
    port = os.environ["port"]


#  Client Keys
CLIENT_ID = ""
CLIENT_SECRET = ""

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = f"{SPOTIFY_API_BASE_URL}/{API_VERSION}"

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
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


@app.route("/")
def index():
    # Auth Step 1: Authorization
    url_args = "&".join(
        [f"{key}={quote(val)}" for key, val in auth_query_parameters.items()]
    )
    auth_url = f"{SPOTIFY_AUTH_URL}/?{url_args}"
    return redirect(auth_url)


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

    # Combine profile and playlist data to display
    display_arr = [profile_data] + playlist_data["items"]
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
    if FLASK_ENV != "dev":
        try:
            # connect to the PostgreSQL database
            conn = psycopg2.connect(
                database, host, user, password, port
            )  # set in .env, don't publish .env to github
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
    methods=(lambda: ["GET", "POST"], lambda: ["POST"])[FLASK_ENV != "dev"](),
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
    if FLASK_ENV != "dev":
        movie_list = call_api()["movie_list"]
        try:
            # connect to the PostgreSQL database
            conn = psycopg2.connect(
                database, host, user, password, port
            )  # set in .env, don't publish .env to github
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
