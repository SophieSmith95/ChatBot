# Python libraries that we need to import for our bot
import os
import pickle
import random
import json

from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAABZCF3b0HpoBAET7CoKXZCz3iUqryKso6HZAM1giogyRFBxBcNGUQlx5RNNEdlkoGIiUZBUjUNCePkHb5FID3jJ66r7TdrLtY1INSKauZAAUciJCpmUVCXPvVQbR0csRPWRZCZCAeNN0v39jAC7mJajwOH5RzvSOFMxHfo65YDMgZDZD'
VERIFY_TOKEN = 'VERIFY_TOKEN'
bot = Bot(ACCESS_TOKEN)


@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        return verify_fb_token(request.args.get("hub.verify_token"))
    else:
        for event in request.get_json()['entry']:
            for message in event['messaging']:
                if message.get('postback'):
                    handle_postback_event(message)
                elif message.get('message'):
                    handle_message_event(message)
    return "Message Processed"


def handle_postback_event(message):
    if message['postback']['payload'] == 'first_hand_shake':
        data = load_data()
        data[message['sender']['id']] = {
            'count': 0,
            'questions': [
                {
                    'question': 'What is your name?',
                    'answer': None
                },
                {
                    'question': 'What is your age?',
                    'answer': None
                },
                {
                    'question': 'How are you feeling?',
                    'answer': None
                }
            ]
        }
        save_data(data)
        #bot.send_text_message(message['sender']['id'], data[message['sender']['id']]['questions'][0]['question'])
        print(bot.send_button_message(message['sender']['id'], "Hey, this is your first time talking to me!", [
            {
                "type": "postback",
                "payload": "responsive",
                "title": "Responsive Botto"
            }, {
                "type": "postback",
                "payload": "store",
                "title": "Store Botto"
            }
        ]))


def handle_message_event(message):

    # ignore empty message text
    if not message['message'].get('text'):
        return

    data = load_data()

    if message['message'].get('text').lower() == 'reset':
        handle_postback_event({
            "sender": {
                "id": message['sender']['id']
            },
            "postback": {
                "payload": "first_hand_shake"
            }
        })
        return

    if data[message['sender']['id']]['questions'][-1]['answer']:
        bot.send_text_message(message['sender']['id'],
                              'You have already completed the questions here are your answers: ')
        bot.send_text_message(message['sender']['id'], 'answers ' + str(data[message['sender']['id']]['questions']))
        bot.send_text_message(message['sender']['id'], "If you would like to modify your answers please type 'Reset'")
        return

    count = data[message['sender']['id']]['count']
    data[message['sender']['id']]['questions'][count]['answer'] = message['message']['text']
    data[message['sender']['id']]['count'] += 1
    save_data(data)

    if data[message['sender']['id']]['questions'][-1]['answer']:
        bot.send_text_message(message['sender']['id'], 'You have completed the questions here are your answers: ')
        bot.send_text_message(message['sender']['id'], 'answers ' + str(data[message['sender']['id']]['questions']))
        bot.send_text_message(message['sender']['id'], "If you would like to modify your answers please type 'Reset'")
        # save to JSON
        with open(data[message['sender']['id']]['questions'][0]['answer'] + ".txt", "w+") as f:
            json.dump(data[message['sender']['id']]['questions'], f)
        return

    bot.send_text_message(message['sender']['id'], next_question(data[message['sender']['id']]['questions']))


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def next_question(questions):
    for question in questions:
        if not question['answer']:
            return question['question']


def load_data():
    try:
        with open('data.pickle', 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        return {}


def save_data(data):
    with open('data.pickle', 'wb') as f:
        pickle.dump(data, f)


if __name__ == "__main__":
    app.run()
