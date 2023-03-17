import requests
import json
def get_weather(apiKey,locationname):
    # 請在下方填入您的 API Key
    apiKey = "CWB-B64CD8B7-02BF-441E-B253-C654F478E513"
    locationname = "板橋區"
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-071"
    params = {
        "Authorization": apiKey,
        "locationName": locationname,
        "elementName": "Wx,AT,T"
    }

    response = requests.get(url, params=params)
    data = json.loads(response.text)

    location = data["records"]['locations'][0]['location'][0]['weatherElement'][0]
    t = '時間:'+location["time"][0]["startTime"]
    l = '\n地點:'+data["records"]["locations"][0]["location"][0]["locationName"]
    te = "\n天氣現象:"+data['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][0]['elementValue'][0]['value']
    tp = '\n溫度:'+ location["time"][0]["elementValue"][0]["value"]+'度'
    reply_text = t+l+te+tp
    return reply_text