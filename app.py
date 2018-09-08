from flask import Flask, render_template
import os
from watson_developer_cloud import ConversationV1
import random
from random import randint

app = Flask(__name__)
conversation = ConversationV1(
        username = 'ed0be530-4e04-4101-8736-47f45951b2a9',
        password = 'JHfRkAqCfJ87',
        version = '2017-05-26'
)
context_val = {}

@app.route('/')
@app.route('/index')
def chat():
    return render_template('chat.html')

@app.route('/send_message/<message>')
def send_mesage(message):
    global context_val
    response = conversation.message(
    workspace_id='913aef7a-8ec6-4dfd-a3d4-9f92ea7a9b54',
    input={
        'text': str(message)
    },
    context=context_val
    )

    print(context_val.keys())
    context_val = response['context']
    if('nearest_pizza_restaurant' not in context_val.keys()):
        context_val['nearest_pizza_restaurant'] = find_nearest_restaurants()
    context_val['pizza_order_id'] = find_order_id()
    return (response['output']['text'][0])

def find_nearest_restaurants():
    return random.choice(['Domino\'s', 'Vanelli\'s', 'Pizza Hut', 'Pizza Inn'])

def find_order_id():
    return randint(1000000,9999999)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
