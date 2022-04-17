from flask import Flask, request
from flask_cors import CORS
from flask import session as flask_session
from flask_session import Session
import redis
from database import create_user, user_logged_in, clear_cache, log_user_in
from helpers import get_session
import json
import os

app = Flask(__name__)
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = redis.Redis()

# https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY
app.config["SECRET_KEY"] = os.environ["SESSION_PWD"]

CORS(app)
Session(app)


@app.route("/create_account", methods=["POST"])
def create_account():
    try:
        data = json.loads(request.data.decode("UTF-8"))
    except:
        return {"error": "invalid payload"}

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([password, email, username]):
        return ({"error": "missing one of password, email or username"}, 400)

    session = get_session()
    status = create_user(
        session=session, username=username, email=email, password=password
    )

    if status.get("error"):
        return status, 400
    else:
        return status, 200


@app.route("/login", methods=["POST"])
def login_user():
    try:
        data = json.loads(request.data.decode("UTF-8"))
    except:
        return {"error": "invalid payload"}

    email = data.get("email")
    password = data.get("password")

    if not all([password, email]):
        return ({"error": "missing one of password or email"}, 400)

    session = get_session()
    response = log_user_in(session=session, email=email, password=password)
    return response


@app.route("/logout", methods=["POST"])
def logout_user():
    try:
        data = json.loads(request.data.decode("UTF-8"))
    except:
        return {"error": "invalid payload"}, 400

    email = data.get("email")

    if not email:
        return ({"error": "missing email"}, 400)

    if user_logged_in():
        result = clear_cache()
        if result:
            return {"success": "user logged out"}, 200

    return {"error": "user never logged in"}, 200


if __name__ == "__main__":

    app.run()
