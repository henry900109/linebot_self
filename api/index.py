from flask import Flask, request, abort,send_file,session
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,PostbackEvent
from linebot.models import QuickReply, QuickReplyButton, MessageAction, ImageSendMessage,PostbackAction,DatetimePickerAction,CameraAction,CameraRollAction,LocationAction
import utils.weather as uw
import utils.weather_quickreply as uwr
import utils.introduce as ui
import utils.polite as up
import utils.proflie as uf
import utils.gpt    as ug
import root.polite as rp
import utils.dollar as ud
import Game.Guessnumber as Guessnumber
import utils.pokemon as pokemon
import utils.money as um
import utils.pwd as pwd
from utils import *
# import test.test as tt
# import test.sheet as ts
import random
import requests
import os
from os.path import join
from glob import glob
import json
from io import BytesIO
# import time


#設置環境變數
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
WEATHER_API_KEY = os.getenv("weather_api")
Openai_token = os.getenv("Open_api")
gemini_token = os.getenv("gemini_api")


app = Flask(__name__)

#預設為安靜模式
quiet_mode = True

#root權限
root_mode = False

#遊戲模式
gamemode = False
gameid = ""
range_min,range_max,answer = 0,0,0
gpttemplate = ""

# domain root
@app.route('/')
def home():
    return 'hello'
@app.route('/pk', methods=['POST'])
def process_form():
    data = request.get_data()
    # return f'{data}'
    data = eval(data)
    cp = data['cp']
    name = data['name']
    cp = str(cp)
    r = pokemon.Rank(name,cp)
    return f'{r}'
@app.route('/cube', methods=['POST'])
def cube_form():
    data = request.get_data()
    # return f'{data}'
    data = eval(data)
    name = data['name']
    name = name.replace(" ","")
    name = find_key_for_value(name).encode('big5').decode('big5')
    return name
@app.route('/photo')
def display_photo():
    # session['plot_image'] = um.draw()
    return send_file(BytesIO(um.draw()), mimetype='image/png')

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
    try:
        #設定變數
        global root_mode, quiet_mode
        global gamemode, gameid, range_min, range_max, answer,gpttemplate

        #訊息
        message = event.message.text

        #使用者ID
        userid = event.source.user_id

        # 如果root輸入 "!!quite"，則設定 root_mode 為 True，否則回傳相同訊息
        message = message.replace("！","!",True) if "！" in (message) else (message) # ！換 !
        if message == "!!quite" and userid == "Uc3e869190fa11d67f2a1ff4b65070e4f":
            root_mode = True #設為絕對安靜模式
            gameid = ""
            gamemode = False
            gpttemplate = ""

            reply_text = rp.Goodbye()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))

        elif message == "!!hello" and userid == "Uc3e869190fa11d67f2a1ff4b65070e4f":
            root_mode = False
            gpttemplate = ""

            reply_text = rp.hello()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))
        elif message == "!send":
            # line_bot_api.push_message('Uc3e869190fa11d67f2a1ff4b65070e4f', TextSendMessage(text='Hello World!!!'))
            profile = line_bot_api.get_profile(userid)
            reply_text = connect_DB(profile)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))
        else:
            
            # 如果使用者輸入 "!quite"，則設定 quiet_mode 為 True，否則回傳相同訊息
            if root_mode == False:

                if message == "!安靜"or message == "!quite":

                    quiet_mode = True #設為安靜模式
                    gamemode = False
                    gameid = ""
                    gpttemplate = ""

                    reply_text = up.Goodbye()
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))

                elif message == "!回來" or message == "!hello":

                    quiet_mode = False #關閉安靜模式
                    gpttemplate = ""
                    reply_text = up.hello()
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))
                    
                # 與gpt3.5連接
                elif "/" == message[0] :
                    # and userid == "Uc3e869190fa11d67f2a1ff4b65070e4f"
                    message = message[1:]
                    template = "以下是一個與 AI 助手的對話。AI 助手非常有幫助、有創意、聰明，並且非常友好。\n\nHuman:你好，你是誰?\nAI: 我是你的 AI 助理，請問我能怎麼幫你?\nHuman: " 
                    if gpttemplate != "":
                        gpttemplate = gpttemplate + message
                    else:
                        gpttemplate = template + message

                    try:
                        reply_text = ug.gemini(gemini_token,gpttemplate)
                        if reply_text != "Error : 無法取得回覆，請稍後再試！":
                            gpttemplate = "\nAI:" + reply_text + "\nHuman:"
                    except:
                        reply_text = "Error(1) : 無法取得回覆，請稍後再試！\n( 或輸入 !quite 重啟 )"
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
                
                elif "//" == message[:1] :
                    # and userid == "Uc3e869190fa11d67f2a1ff4b65070e4f"
                    message = message[2:]

                    if gpttemplate != "":
                        gpttemplate = gpttemplate.append({"role": "user", "content": message})
                    else:
                        gpttemplate = [{"role": "assistant", "content": "我是個 AI 助手，非常有幫助、有創意、聰明，並且非常友好"},{"role": "user", "content": message}]

                    reply_text = ug.gpt4(Openai_token,gpttemplate)
                    try:
                        reply_text = ug.gpt4(Openai_token,gpttemplate)
                        if reply_text != "Error : 無法取得回覆，請稍後再試！":
                            gpttemplate = gpttemplate.append({"role": "assistant", "content": reply_text})
                    except:
                        reply_text = "Error(1) : 無法取得回覆，請稍後再試！\n( 或輸入 !quite 重啟 )"
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))


                elif message == "!introduce" or message == "！introduce":
                    reply_text = ui.interduce()
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))


                elif "!我要查詢天氣" == message:
                    quick_reply = uwr.area()
                    reply_text = TextSendMessage(text="請選擇區域",quick_reply=quick_reply)
                    line_bot_api.reply_message(event.reply_token, reply_text)

                elif "卓子揚" in message and "@卓子揚" not in message:
                        # 認主
                    retext = "他是帥哥!!"
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=retext))

                #測試模式
#                 elif message == "!test":# reply_text = tt.test() #測試用
#                     profile = line_bot_api.get_profile(userid)
#                     reply_text = tt.profile(profile)
#                     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

                # 知道使用者身分
                elif message == "!whoami":
                    profile = line_bot_api.get_profile(userid)
                    reply_text = uf.profile(profile)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
                
                elif message == "!pwd":
                    profile = line_bot_api.get_profile(userid)
                    reply_text = pwd.generate_monthly_password(profile)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
                
                # 玩遊戲
                elif message == "!play":
                    gameid = userid
                    reply_text = "猜數字, 1~100\n\n!out 可結束遊戲"

                    #開啟遊戲模式
                    gamemode = True

                    # 設定猜數字的範圍
                    range_min = 1
                    range_max = 100
                    answer = random.randint(range_min, range_max)
                    Guessnumber.Guseenumder_start(userid)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

                # ( 今天 / 明天 ) 新北市OO區天氣
                elif message[0] == "!" and "天氣" == message[9:]:
                        
                    LOCATION_NAME = message[1:]
                    reply_text = uw.weather(WEATHER_API_KEY,LOCATION_NAME)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

                # 全臺各縣市天氣
                elif message[0] == "!" and "天氣" == message[4:]:
                    reply_text = uw.get_country_weather(WEATHER_API_KEY,message)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

#                 elif message == "測試flex":
#                     reply_text = tt.flex()
#                     line_bot_api.reply_message(event.reply_token, reply_text)

#                 elif message == "測試sheet":
#                     reply_text = ts.sheet(userid)
#                     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))

                elif "!img" in message :
                    reply_text = []
                    url = ug.img(Openai_token,message[4:])
                    reply_text.append(ImageSendMessage(original_content_url=url,preview_image_url=url))
                    line_bot_api.reply_message(event.reply_token,reply_text)

                elif message == "!youtube":
                    reply_text = ud.UAH2TWD()
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))
                elif "!pokemon" in message:
                    message = message[8:]
                    messageA,messageB  = message.split(" ")[0],message.split(" ")[1]
                    reply_text = pokemon.Attributes_Table(messageB,messageA)
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))
                elif "!pokename" in message:
                    message = message[9:]
                    if " " in message:
                        messageA,messageB  = message.split(" ")[0],message.split(" ")[1]
                        reply_text = pokemon.Rank(messageA,messageB)
                    else:
                        reply_text = pokemon.Rank(message)
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))

                elif "!money" in message:
                    img_url = "https://linebot-self.vercel.app/photo"
                    img_message = ImageSendMessage(original_content_url=img_url, preview_image_url=img_url)
                    line_bot_api.reply_message(event.reply_token,img_message)

                elif "aaaa" == message:
                    with open(r'/var/task/data/attr.json','r') as file:
                        file_content = file.read()
                    file_content = json.JSONDecoder().decode(file_content)
                    print(file_content)
                    reply_text = str(a)
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))
                    
                else:

                    #確認是否在遊戲模式
                    if gamemode == True and gameid == userid:

                        #離開遊戲模式
                        if message == "!out":
                            gameid = ""
                            gamemode = False

                            reply_text = "遊戲結束\n\n答案為 " + str(answer)
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

                        else:
                            reply_text = Guessnumber.Guessnumber(message,range_min,range_max,answer)

                            #遊戲成功
                            if reply_text[0] == "f":
                                gameid = ""
                                reply_text = reply_text[1:]
                                gamemode = False
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
                            
                    #鸚鵡
            
                    # if quiet_mode == False : 
                    #     reply_text = ug.gpt3_5(Openai_token,message)
                    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))     
                    #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))
    except requests.exceptions.ReadTimeout:
        reply_text = "Error : 系統忙碌中，請稍後再試！"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
@line_handler.add(PostbackEvent)
def handle_postback(event):
    postback_data = event.postback.data
    if postback_data[0] == "C":
        quick_reply = uwr.town(postback_data)
        reply_text = TextSendMessage(text="請選擇行政區",quick_reply=quick_reply)
        line_bot_api.reply_message(event.reply_token, reply_text)

    elif postback_data[0] == "T":
        quick_reply = uwr.tomorrow_or_today(postback_data[1:])
        reply_text = TextSendMessage(text="請選擇日期",quick_reply=quick_reply)
        line_bot_api.reply_message(event.reply_token, reply_text)
    
    elif postback_data[0] == "D":
        reply_text = postback_data[1:]
        reply_text = uw.weather(WEATHER_API_KEY,reply_text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
    
    elif postback_data[0] == "A":
        quick_reply = uwr.countryname(postback_data)
        reply_text = TextSendMessage(text="請選擇縣市",quick_reply=quick_reply)
        line_bot_api.reply_message(event.reply_token, reply_text)
               

if __name__ == "__main__":
    app.run()
