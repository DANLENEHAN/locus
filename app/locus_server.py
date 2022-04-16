from email import message
from flask import Flask, request
from flask_cors import CORS
from flask import session
from flask_session import Session
import redis
import json
import pika

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
    channel.queue_declare(queue='harrier')
    channel.basic_publish(
        exchange='',
        routing_key='harrier',
        body=json.dumps(message)
    )
    session['key'] = 123

    print('Key: ', session.get('key'))

    return {"message": "data received"}

if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    app.run(host='0.0.0.0', port=5002)