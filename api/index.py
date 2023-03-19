from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import utils.weather as uw
import utils.introduce as ui
import utils.polite as up
import utils.proflie as uf
import utils.gpt    as ug
import root.polite as rp
import Game.Guessnumber as Guessnumber
import test.test as tt
import random
import os

#設置環境變數
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
WEATHER_API_KEY = os.getenv("weather_api")
Openai_token = os.getenv("Open_api")



app = Flask(__name__)

#預設為安靜模式
quiet_mode = True

#root權限
root_mode = False

#遊戲模式
gamemode = False
range_min,range_max,answer = 0,0,0

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

    #設定變數
    global root_mode, quiet_mode
    global gamemode, range_min, range_max, answer

    #訊息
    message = event.message.text

    #使用者ID
    userid = event.source.user_id

    # 如果root輸入 "!!quite"，則設定 root_mode 為 True，否則回傳相同訊息
    if message == "!!quite" and userid == "Uc3e869190fa11d67f2a1ff4b65070e4f":
        root_mode = True #設為絕對安靜模式

        reply_text = rp.Goodbye()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))

    elif message == "!!hello" and userid == "Uc3e869190fa11d67f2a1ff4b65070e4f":
        root_mode = False

        reply_text = rp.hello()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))

    else:
        
        # 如果使用者輸入 "!quite"，則設定 quiet_mode 為 True，否則回傳相同訊息
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
                    
                    # 認主
                    if "卓子揚" in message and "@卓子揚" not in message:
                        retext = "他是帥哥!!"
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=retext))

                    #測試模式
                    elif message == "!test":# reply_text = tt.test() #測試用
                        profile = line_bot_api.get_profile(userid)
                        reply_text = tt.profile(profile)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

                    # 知道使用者身分
                    elif message == "!whoami":
                        profile = line_bot_api.get_profile(userid)
                        reply_text = uf.profile(profile)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
                    
                    # 與gpt3.5連接
                    elif "!gpt" in message and userid == "Uc3e869190fa11d67f2a1ff4b65070e4f":
                        message = message[4:]
                        reply_text = ug.gpt3_5(Openai_token,message)
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

                    # 玩遊戲
                    elif message == "!play":
                        reply_text = "猜數字, 1~100\n\n!out 可結束遊戲"

                        #開啟遊戲模式
                        gamemode = True

                        # 設定猜數字的範圍
                        range_min = 1
                        range_max = 100
                        answer = random.randint(range_min, range_max)

                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

                    # ( 今天 / 明天 ) 新北市OO區天氣
                    elif message[0] == "!" and "天氣" == message[6:]:

                        #!明天板橋區天氣
                        if "區天氣" == message[5:]:
                            LOCATION_NAME = message[1:]
                            reply_text = uw.weather(WEATHER_API_KEY,LOCATION_NAME)
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

                    # 全臺各縣市天氣
                    elif message[0] == "!" and "天氣" == message[4:]:

                        #!文山區天氣
                        cityname = ["萬華","中正","南港","文山"]
                        if message[1:3]in cityname:
                            reply_text = uw.now_weather(message[1:4])
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

                        else:
                            reply_text = uw.get_country_weather(WEATHER_API_KEY,message)
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

                    else:

                        #確認是否在遊戲模式
                        if gamemode == True:

                            #離開遊戲模式
                            if message == "!out":
                                gamemode = False

                                reply_text = "遊戲結束\n\n答案為 " + str(answer)
                                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

                            else:
                                reply_text = Guessnumber.Guessnumber(message,range_min,range_max,answer)

                                #遊戲成功
                                if reply_text[0] == "f":
                                    reply_text = reply_text[1:]
                                    gamemode = False
                                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
                        
                        #鸚鵡
                        else:
                        
                            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))


if __name__ == "__main__":
    app.run()