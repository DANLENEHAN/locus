from crypt import methods
from email import message
from flask import Flask, request
from flask_cors import CORS
from flask import session
from flask_session import Session
import redis
import json
import os
import hashlib

app = Flask(__name__)
SECRET_KEY = '123456789012345678901234'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis()
app.config['SECRET_KEY'] = SECRET_KEY
CORS(app)
Session(app)


@app.route("/", methods=["POST"])
def hello():
    user_info = request.data.decode("UTF-8")
    message_tag = "create_user_attempt"
    message = [message_tag, user_info]
    print("Request", user_info)
    session['key'] = 123
    print('Key: ', session.get('key'))

    return {"message": "data received"}

@app.route("/create_account", methods=["POST"])
def create_account():
    data = request.data.decode("UTF-8")

    username = data.get("username")
    email = data.get("email")
    password = data.get("email")

    if not all([password, email, username]):
        return (
            {
                "error": "missing one of password, email or username"
            },
            400
        )

    hash = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('utf-8'),
        salt=os.environ["SALT"].encode('utf-8'),
        iterations=100000
    )

    return {"success": "Account created"}, 200


if __name__ == "__main__":

    app.run(host='0.0.0.0', port=5002)