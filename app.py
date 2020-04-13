import os
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
bot = Bot(ACCESS_TOKEN)

@app.route('/')
def index():
    return "<h1>Welcome to my bot!</h1>"

@app.route("/webhook", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            recipient_id = message['sender']['id']
            if message.get('message'):
                if message['message'].get('text'):
                    received = message['message'].get('text')
                    bot.send_text_message(recipient_id, "echo: " + received)
    return "Message Processed"

def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

if __name__ == "__main__":
    app.run("0.0.0.0", 5000)