# how to run the app in project root folder (in vscode terminal)

```
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python3 app.py OR flask run
```

# local testing

in local .env file, set FLASK_ENV to something other than "dev" and test database connection.

For example:

```
FLASK_ENV=test
# If some of them are not necessary, change code at app.py:line18~26
database=
host=
user=
password=
port=
```

DO NOT COMMIT .env with keys to Github!!!

# some APIs

http://127.0.0.1:5000/callapi

it should return something about cats

http://127.0.0.1:5000/db/select/<user_id>

it should return some information about user {user_id} in db

http://127.0.0.1:5000/db/update/<user_id>

it should return the new "movie_list" about user {user_id} in db
