import requests
import json
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