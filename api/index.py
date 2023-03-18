from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import utils.weather as uw
import utils.introduce as ui
import utils.polite as up
import utils.proflie as uf
import test.test as tt
import requests
import os

#設置環境變數
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
WEATHER_API_KEY = os.getenv("weather_api")



app = Flask(__name__)

#預設為安靜模式
quiet_mode = True
#root權限
root_mode = False
# domain root
@app.route('/')
def home():
    return 'hello'

#連接webhook
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


#回應
@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global quiet_mode
    global root_mode
    #訊息
    message = event.message.text

    #使用者ID
    userid = event.source.user_id

    # 如果使用者輸入 "安靜"，則設定 quiet_mode 為 True，否則回傳相同訊息

    # tt.profile(line_bot_api.get_profile(userid))!="卓子揚" 設定XXX不回訊息

    if message == "!!quite" and userid == "Uc3e869190fa11d67f2a1ff4b65070e4f":
        root_mode = True

    elif message == "!!hello" and userid == "Uc3e869190fa11d67f2a1ff4b65070e4f":
        root_mode = False

    else:

        if root_mode == False:

            if message == "!安靜"or message == "!quite":

                quiet_mode = True #設為安靜模式

                reply_text = up.Goodbye()
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))

            elif message == "!回來" or message == "!hello":

                quiet_mode = False #關閉安靜模式

                reply_text = up.hello()
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))

            elif message == "!introduce":
                reply_text = ui.interduce()
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))

            elif "冰淇淋" in message and tt.profile(line_bot_api.get_profile(userid))!="詹茹萍":
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="不可以!!!"))

            else:

                if quiet_mode == False :

                    if message == "卓子揚是帥哥嗎?":
                        retext = "那是肯定的"
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=retext))

                    elif message == "!test":# reply_text = tt.test() #測試用
                        profile = line_bot_api.get_profile(userid)
                        reply_text = tt.profile(profile)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

                    elif message == "!whoami":
                        profile = line_bot_api.get_profile(userid)
                        reply_text = uf.profile(profile)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

                    elif message[0] == "!" and "天氣" == message[4:]:
                        
                        #新北市XX區天氣
                        if "區天氣" == message[3:]:
                            LOCATION_NAME = message[1:4]
                            reply_text = uw.get_weather(WEATHER_API_KEY = WEATHER_API_KEY,locationname = LOCATION_NAME)
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

                        #全臺各縣市天氣
                        else:
                            reply_text = uw.get_country_weather(WEATHER_API_KEY,message)
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

                    else:
                        #鸚鵡
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))


if __name__ == "__main__":
    app.run()