# how to run the app
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python3 app.py

# some APIs

http://127.0.0.1:5000/callapi

it should return something about cats


http://127.0.0.1:5000/db/select/<user_id>

it should return some information about user {user_id} in db


http://127.0.0.1:5000/db/update/<user_id>

it should return the new "movie_list" about user {user_id} in db