from email import message
from flask import Flask, request
from flask_cors import CORS
import json
import pika

app = Flask(__name__)
CORS(app)



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
    return {"message": "data received"}

if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    app.run(host='0.0.0.0', port=5001)