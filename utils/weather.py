import requests
import json
from datetime import datetime,timedelta
import time
import js2py
import pandas as pd

def get_weather(WEATHER_API_KEY,locationname):
    # 請在下方填入您的 API Key
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-071"
    params = {
        "Authorization": WEATHER_API_KEY,
        "locationName": locationname,
        "elementName": "Wx,AT,T"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = json.loads(response.text)
        location = data["records"]['locations'][0]['location'][0]['weatherElement'][0]
        t = '時間:'+location["time"][0]["startTime"]
        l = '\n地點:'+data["records"]["locations"][0]["location"][0]["locationName"]
        te = "\n天氣現象:"+data['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][0]['elementValue'][0]['value']
        tp = '\n溫度:'+ location["time"][0]["elementValue"][0]["value"]+'度'
        reply_text = t+l+te+tp
        return reply_text
    else:
        return "天氣查詢失敗！"
    

def weather(WEATHER_API_KEY,user):

    now = datetime.now().date()
   
    weather_apikey = WEATHER_API_KEY
   
    dataid = 'F-D0047-069' #新北市
   
    element_name = "T,Wx,PoP6h,AT"

    url = f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/{dataid}?Authorization={weather_apikey}&locationName={user[2:5]}&elementName={element_name}'
   
    response = requests.get(url)
   
    data = response.json()

    date_code = {'今天':now,'明天':now + timedelta(days=1)}
    
    extra = data['records']['locations'][0]['location'][0]['weatherElement']


    relpy_text = user[2:] +"\n"

    for j in range(len(extra[0]['time'])):

        # 讀取資料第一筆時間
        moment = datetime.strptime(extra[0]['time'][j]['startTime'], '%Y-%m-%d %H:%M:%S')
        
        # 判斷所需的日期天氣資料

        if str(date_code[user[:2]]) in str(moment):

            relpy_text+= str(moment) 
            relpy_text+='\n'

            for i in range(len(extra)-1):

                description = extra[i]['description']

                try:
                    wx = extra[i]['time'][j]['elementValue'][0]['value']

                except IndexError:

                    wx = '尚未預測'
                relpy_text+=description+":"+ wx 
                relpy_text+='\n'

            try:

                relpy_text+=extra[-1]['description']+":"+extra[-1]['time'][j//2]['elementValue'][0]['value']+"%"
                relpy_text+='\n'
                relpy_text+='\n'

            except IndexError:

                relpy_text+='N\A'

    if relpy_text == user[2:] +"\n":
        relpy_text = "天氣查詢失敗"

    return relpy_text
    
def now_weather(name):
  timestr = time.strftime("%Y%m%d%H")
  url = 'https://www.cwb.gov.tw/Data/js/GT/TableData_GT_T_63.js?T='+timestr+'-4&_=1657432140292'
  headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47"}
  download = requests.get(url,headers = headers)
  download = download.text
  cityID = [6301200,6301100,6300600,6300400,6300100,6301000,6300700,6300500,6300300,6300200,6300900,6300800]
  cityname = {"萬華區":6,"中正區": 7,"南港區" : 10,"文山區": 11}
  aid = cityname[name]
  text = js2py.eval_js(download)
  C_AT=[]
  C_T=[]
  RH=[]
  Rain=[]
  Sunrise=[]
  Sunset=[]
  for item in cityID:
    C_AT.append(text[item]["C_AT"])
    C_T.append(text[item]["C_T"])
    Rain.append(text[item]["Rain"])
    RH.append(text[item]["RH"])
    Sunrise.append(text[item]["Sunrise"])
    Sunset.append(text[item]["Sunset"])
    

  output=[cityID,C_AT,C_T,RH,Rain,Sunrise,Sunset]
  df=pd.DataFrame(output)
  dt=df.T
  dt.columns=['Cityid','C_AT','C_T','RH','Rain','Sunrise','Sunset']
  timestr = time.strftime("%Y%m%d")
  return '\n'+timestr + '\n'+name+'降雨機率為 ' + dt['Rain'][aid]  +"%\n最高溫: "+ dt['C_AT'][aid] + " 度\n最低溫: " + dt['C_T'][aid] +'度'
# 6300700 萬華 6
#  63000500 中正 7
#6300900 南港 10
#6300800 文山 11
# print(now_weather())



def get_country_weather(WEATHER_API_KEY,locationname):
    WEATHER_API_URL = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
    locationname = locationname.replace("台","臺",True) if "台" in locationname else locationname
    country = ["宜蘭縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣", "連江縣", "臺北市", "新北市", "桃園市", "臺中市", "臺南市", "高雄市", "基隆市", "新竹縣", "新竹市", "苗栗縣", "彰化縣", "南投縣", "雲林縣", "嘉義縣", "嘉義市", "屏東縣"]
    LOCATION_NAME = locationname[1:4]
    res = requests.get(f"{WEATHER_API_URL}?Authorization={WEATHER_API_KEY}&locationName={LOCATION_NAME}")
    if res.status_code == 200:
        data = res.json()["records"]["location"][0]["weatherElement"]
        reply_text = f"{LOCATION_NAME}天氣狀況：\n\n"
        for i in range(3):
            time = data[0]["time"][i]["startTime"][5:10].replace("-", "/")
            weather = data[0]["time"][i]["parameter"]["parameterName"]
            temp = data[1]["time"][i]["parameter"]["parameterName"]
            reply_text += f"{time}:{weather}，氣溫 {temp}℃\n"
        return reply_text
    else:
        return "天氣查詢失敗！"