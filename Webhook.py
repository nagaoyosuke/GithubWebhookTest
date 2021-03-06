#herokuならコメントアウト
#import config

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


import os
import json
import urllib

app = Flask(__name__)
#環境変数取得(herokuだけ)
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
LINEGROUPID = os.environ["LINEGROUPID"]
LINEID = os.environ["LINEID"]


line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

#ローカル
#YOUR_CHANNEL_ACCESS_TOKEN = config.LINE_CHANNEL_ACCESS_TOKEN 
#YOUR_CHANNEL_SECRET = config.LINE_CHANNEL_SECRET
#LINEGROUPID = config.LINEGROUPID
#LINEID = config.LINEID


@app.route("/gitcallback", methods=['POST'])
def gitcallback():
    try:
        data = json.loads(request.data)
        m = len(data['commits']) - 1
        s = ''
        s = s + str("コミットしたのは: {}".format(data['commits'][m]['author']['name']))
        s = s + "\n\n"
        s = s + str("コミットメッセージは:\n {}".format(data['commits'][m]['message']))
        s = s + "\n\n"
        s = s + str("コミットした時間は: {}".format(data['commits'][m]['timestamp']))
        s = s + '\n 以上です'
        s = s + '\n https://github.com/nagaoyosuke/GithubWebhookTest' 
        Send(s,LINEGROUPID)
    except:
        Send('エラーです',LINEID)
    return 'OK'

def Send(text,user_id):
    url = 'https://api.line.me/v2/bot/message/push'
    channel_access_token = YOUR_CHANNEL_ACCESS_TOKEN
    # 送信用のデータ
    data = {
        'to' : user_id,
        'messages' : [
            {
                'type' : 'text',
                'text' : text
            }
        ]
    }
    jsonstr = json.dumps(data).encode('ascii')
    print(jsonstr)
    # Content-Type:application/json
    # Authorization:Bearer {channel access token}
    # method:post
    request = urllib.request.Request(url, data=jsonstr)
    request.add_header('Content-Type', 'application/json')
    request.add_header('Authorization', 'Bearer ' + channel_access_token)
    request.get_method = lambda: 'POST'
    # 送信実行
    response = urllib.request.urlopen(request)
    ret = response.read()
    print('Response:', ret)
    
'''
def localtest():
    with open('test.json') as file:
        data = json.load(file)
        m = len(data['commits']) - 1
        s = ''
        s = s + str("コミットしたのは: {}".format(data['commits'][m]['author']['name']))
        s = s + "\n\n"
        s = s + str("コミットメッセージは:\n {}".format(data['commits'][m]['message']))
        s = s + "\n\n"
        s = s + str("コミットした時間は: {}".format(data['commits'][m]['timestamp']))
        s = s + '\n 以上です'
        s = s + '\n https://github.com/nagaoyosuke/GithubWebhookTest' 
        print(s)
    return 'OK'
'''

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    t()