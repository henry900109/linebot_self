from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests
import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

WEATHER_API_URL = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
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

    # 如果使用者輸入 "安靜"，則設定 quiet_mode 為 True，否則回傳相同訊息
    if message == "!安靜":
        quiet_mode = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="好的，我會安靜"))
    elif message == "!回來" or message == "!hello":
        quiet_mode = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我回來了!"))
    else:
        if quiet_mode == False:
            if message == "卓子揚是帥哥嗎?":
                retext = "那是肯定的"
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=retext))
            elif message[0] == "!" and "天氣" == message[4:]:
        # 用氣象局 API 查詢板橋區的天氣資訊
                country = ["宜蘭縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣", "連江縣", "臺北市", "新北市", "桃園市", "臺中市", "臺南市", "高雄市", "基隆市", "新竹縣", "新竹市", "苗栗縣", "彰化縣", "南投縣", "雲林縣", "嘉義縣", "嘉義市", "屏東縣"]
                LOCATION_NAME = message[1:4]
                res = requests.get(f"{WEATHER_API_URL}?Authorization={WEATHER_API_KEY}&locationName={LOCATION_NAME}")
                if res.status_code == 200:
                    data = res.json()["records"]["location"][0]["weatherElement"]
                    reply_text = f"{LOCATION_NAME}天氣狀況：\n\n"
                    for i in range(3):
                        time = data[0]["time"][i]["startTime"][5:10].replace("-", "/")
                        weather = data[0]["time"][i]["parameter"]["parameterName"]
                        temp = data[1]["time"][i]["parameter"]["parameterName"]
                        reply_text += f"{time}:{weather}，氣溫 {temp}℃\n"
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="天氣查詢失敗！"))
            else:
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=message))


if __name__ == "__main__":
    app.run()