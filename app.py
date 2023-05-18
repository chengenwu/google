from googlesearch import search
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

app = Flask(__name__)

line_bot_api = LineBotApi('8eAMDtKP5QlPkKbgcd3040qBqPaPHSTcCFsDx2lYo9Zx6JwojKq9woEJoRe2ojUvrv4uyToLQqExQ15Y2nd5ARCKuvL1RXePUiHmQQ/iYfmC/30GYLuSEfmSUTGWsxvZDBFiLT5cN6lt+1fyEb3wVAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b5858c3a3ed5e7333d2be5442e98a014')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if event.message.text[0:2] == '搜尋':        

        query = event.message.text[2:]
        Str = ''
        for j in search(query, stop=5, pause=1.0): 
            Str = Str + '\n' + '\n' + j

        Str = Str[2:]

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(Str))        


if __name__ == "__main__":
    app.run()