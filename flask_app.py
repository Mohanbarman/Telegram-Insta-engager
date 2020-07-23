from flask import Flask
from flask import request
from flask import Response
from link import *
from key import *
import requests
import json
import sys
import os

app = Flask(__name__)
key = get_key()

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Shutting down the server...')
    func()

def delete_webhook():
    requests.get(f'https://api.telegram.org/bot{key}/setWebhook')

def send_message(chat_id, text):
    requests.get(f'https://api.telegram.org/bot{key}/sendMessage?chat_id={chat_id}&text={text}')

def set_webhook(url):
    res = requests.get(f'https://api.telegram.org/bot{key}/setWebhook?url={url}')
    print(json.loads(res.text))
    print(f'Successfuly set webhook to : {url}')

def get_pending_update_count():
    res = requests.get(f'https://api.telegram.org/bot{key}/getWebhookInfo')
    res_json = json.loads(res.text)
    count = res_json['result']['pending_update_count']
    return int(count)

args = sys.argv
print(args)
set_webhook(args[1])

link_capture_started = 0
post_links = []
profile_names = []

ran_fist_time = True

@app.route('/', methods=['POST', 'GET'])
def index():
    global link_capture_started
    global post_links
    global profile_names
    global ran_fist_time
    shutdown = 0

    if request.method == 'POST':
        pending_count = get_pending_update_count()

        if ran_fist_time and pending_count >= 1:
            ran_fist_time = False
            return Response('ok', 200)

        res = request.get_json()
        if len(res) == 0:
            return Response('Ok', status=200)
        
        if 'message' in res:
            msg = res['message']
        else:
            msg = res['edited_message']
            
        chat_id = msg['chat']['id']
        text = msg['text']

        if text == '/start':
            send_message(chat_id, 'Send me the links....')
            link_capture_started = 1
            return Response('Ok', status=200)


        if text == '/stop':
            send_message(chat_id, 'Stopped receiving links..')
            link_capture_started = 0

            with open('ig_links.json', 'w') as f:
                data = {'profile_names': profile_names, 'post_links': post_links}
                json.dump(data, f)

        if text == '/result':
            print(f'post links : {post_links}')
            print(f'profile names: {profile_names}')
        
        if text == '/engage':
            send_message(chat_id, 'Starting to engage with the users...')
            print('deleting webhook..')

            delete_webhook()
            print('Shutting down the server...')
            shutdown_server()

        if link_capture_started:
            link_type = identify_link_type(text)

            if link_type == 1:
                p_url = extract_post_link(text)

                if p_url == None:
                    return Response('Ok', status=200)

                print(f'post link stored : {p_url}')
                post_links.append(p_url)
            
            elif link_type == 2:
                p_url = extract_username(text)

                if p_url == None:
                    return Response('Ok', status=200)

                print(f'profile name stored : {p_url}')
                profile_names.append(p_url)
        
        return Response('Ok', status=200)
    else:
        return '<h1>Engagement bot<h1>'


if __name__ == '__main__':
    try:
        app.run(debug=False)
    except:
        delete_webhook()
