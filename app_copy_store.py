#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
import os

app = Flask(__name__)
ACCESS_TOKEN = 'EAABZCF3b0HpoBAET7CoKXZCz3iUqryKso6HZAM1giogyRFBxBcNGUQlx5RNNEdlkoGIiUZBUjUNCePkHb5FID3jJ66r7TdrLtY1INSKauZAAUciJCpmUVCXPvVQbR0csRPWRZCZCAeNN0v39jAC7mJajwOH5RzvSOFMxHfo65YDMgZDZD'
VERIFY_TOKEN = 'VERIFY_TOKEN'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        f = open("user.txt", "w+")
        return verify_fb_token(token_sent)
    else:
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('postback'):
                if message['postback'].get('payload') == "first_hand_shake":
                    recipient_id = message['sender']['id']
                    bot.send_text_message(recipient_id, "Hey")
            elif message.get('message'):
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    for filename in os.listdir("."):
                        if filename.startswith("user"):
                            os.rename(filename, recipient_id + ".txt")
                    with open(recipient_id + ".txt", "a") as file:
                        file.write(message['message'].get('text') + "\n")
                    save_position(recipient_id)
                    questions(recipient_id, message['message'].get('text'))
    return "Message Processed"

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def questions(recipient_id, message):
    global count
    with open("Position.txt", 'r') as bots:
        for line in bots:
#INSERT

def save_position(recipient_id):
    with open("position.txt", 'w') as bot:
        bot.write("ID = " + str(recipient_id) + ", Counter = " + str(count))

if __name__ == "__main__":
    app.run()