from flask import Flask, request
from flask_cors import CORS
from flask import session as flask_session
from flask_session import Session
import redis
from database import (
    create_user, validate_user, get_user
)
from helpers import get_session
import json
import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis()

# https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY
app.config['SECRET_KEY'] = os.environ['SESSION_PWD']

CORS(app)
Session(app)


@app.route("/create_account", methods=["POST"])
def create_account():
    try:
        data = json.loads(
            request.data.decode("UTF-8")
        )
    except:
        return {"error": "invalid payload"}

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([password, email, username]):
        return (
            {
                "error": "missing one of password, email or username"
            },
            400
        )

    session = get_session()
    status = create_user(
        session=session,
        username=username,
        email=email,
        password=password
    )

    if status.get("error"):
        return status, 400
    else:
        return status, 200



@app.route("/login", methods=["POST"])
def login_user():
    try:
        data = json.loads(
            request.data.decode("UTF-8")
        )
    except:
        return {"error": "invalid payload"}

    email = data.get("email")
    password = data.get("password")

    if not all([password, email]):
        return (
            {
                "error": "missing one of password or email"
            },
            400
        )

    session = get_session()
    response = validate_user(
        session=session,
        email=email,
        password=password
    )

    if response.get("success"):
        user = get_user(session=session, email=email)
        flask_session['username'] = user['username']
        flask_session['id'] = user['id']
        flask_session['user_id'] = f"{user['username']}_{user['id']}"
        return response, 200
    else:
        return response, 400


if __name__ == "__main__":

    app.run()