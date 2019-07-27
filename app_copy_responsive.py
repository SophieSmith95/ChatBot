#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAABZCF3b0HpoBAET7CoKXZCz3iUqryKso6HZAM1giogyRFBxBcNGUQlx5RNNEdlkoGIiUZBUjUNCePkHb5FID3jJ66r7TdrLtY1INSKauZAAUciJCpmUVCXPvVQbR0csRPWRZCZCAeNN0v39jAC7mJajwOH5RzvSOFMxHfo65YDMgZDZD'
VERIFY_TOKEN = 'VERIFY_TOKEN'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
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
                    questions(recipient_id, message['message'].get('text'))
    return "Message Processed"

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def questions(recipient_id, message):
#INSERT

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()