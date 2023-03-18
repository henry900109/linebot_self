from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import utils.weather as uw
import utils.introduce as ui
import test.test as tt
import requests
import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
apiKey = os.getenv("weather_api")

WEATHER_API_KEY = "CWB-B64CD8B7-02BF-441E-B253-C654F478E513"
# os.getenv("WEATHER_API_KEY")



app = Flask(__name__)
quiet_mode = True
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
    userid = event.source.user_id
    # 如果使用者輸入 "安靜"，則設定 quiet_mode 為 True，否則回傳相同訊息
    if message == "!安靜"or message == "!quite":
        quiet_mode = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="好的，我會安靜"))
    elif message == "!回來" or message == "!hello":
        quiet_mode = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我回來了!"))
    elif message == "!introduce":
        reply_text = ui.interduce()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))
    else:
        if quiet_mode == False:
            if message == "卓子揚是帥哥嗎?":
                retext = "那是肯定的"
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=retext))
            elif message == "!test":
                # reply_text = tt.test()

                try:
                    groupid = event.source.group_id
                    profile = line_bot_api.get_group_summary(groupid)
                    members = line_bot_api.get_group_member_ids(groupid)
                    reply_text = tt.group(profile)
                except:
                    profile = line_bot_api.get_profile(userid)
                    reply_text = tt.profile(profile)
                # reply_text = profile.display_name
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
            elif message[0] == "!" and "天氣" == message[4:]:
                if "區天氣" == message[3:]:
                    LOCATION_NAME = message[1:4]
                    reply_text = uw.get_weather(WEATHER_API_KEY = WEATHER_API_KEY,locationname = LOCATION_NAME)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
                else:
                    reply_text = uw.get_country_weather(WEATHER_API_KEY,message)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
            else:
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=message))


if __name__ == "__main__":
    app.run()