from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

app = Flask(__name__)
quiet_mode = False
# domain root
@app.route('/')
def home():
    return 'hello'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'



@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global quiet_mode
    message = event.message.text

    # 如果使用者輸入 "安靜"，則設定 quiet_mode 為 True，否則回傳相同訊息
    if message == "!安靜":
        quiet_mode = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="好的，我會安靜"))
    elif message == "!回來":
        quiet_mode = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我回來了!"))
    else:
        if quiet_mode == False:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=message))


if __name__ == "__main__":
    app.run()