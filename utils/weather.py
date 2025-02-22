import requests
import json
from datetime import datetime,timedelta

def weather(WEATHER_API_KEY,user):

    now = datetime.now()

    date_code = {'今天':now,'明天':now.replace(hour=0, minute=0, second=0, microsecond = 0) + timedelta(days=1),'後天':now.replace(hour=0, minute=0, second=0, microsecond = 0) + timedelta(days=2)}
     
    weather_apikey = WEATHER_API_KEY
    
    dataid = (user[2:5]).replace("台","臺",True) if "台" in (user[2:5]) else (user[2:5]) # [user[2:5]] ex:新北市
    dataid_code = {'宜蘭縣':'001','桃園市':'005','新竹縣':'009','苗栗縣':'013','彰化縣':'017','南投縣':'021','雲林縣':'025','嘉義縣':'029',
                '屏東縣':'033','臺東縣':'037','花蓮縣':'041','澎湖縣':'045','基隆市':'049','新竹市':'053','嘉義市':'057','臺北市':'061',
                '高雄市':'065','新北市':'069','臺中市':'073','臺南市':'077','連江縣':'081','金門縣':'085'}
    
    element_name = "溫度,天氣現象,3小時降雨機率,體感溫度"

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-{dataid_code[dataid]}?Authorization={weather_apikey}&LocationName={user[5:-2]}&ElementName={element_name}'
    response = requests.get(url)
   
    data = response.json()
    with open('utils/test.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    extra = data['records']['Locations'][0]['Location'][0]['WeatherElement']
    relpy_text = user[2:] +"\n"
    for j in range(len(extra[0]['Time'])):
        # 解析時間字串
        time_str = extra[0]['Time'][j]['DataTime']
        time_str = time_str.split('+')[0].replace('T', ' ')  # 去掉時區資訊並調整格式
        moment = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

        # 確保匹配的時間資料
        if date_code[user[:2]] <= moment and str(date_code[user[:2]].date()) in str(moment):

            # 記錄時間
            relpy_text += moment.strftime('%m/%d %H點') + '\n'

            # 初始化天氣資訊變數
            weather = ""       # 天氣現象 (如 陰、多雲)
            temperature = ""   # 溫度
            apparent_temp = "" # 體感溫度
            rain_prob = "降雨機率 : 無數據"  # 預設值，避免沒有降雨機率時出錯

            for i in range(len(extra)):
                ElementName = extra[i]['ElementName']
                
                try:
                    wx = extra[i]['Time'][j]['ElementValue'][0]  # 直接取 [0]，避免後續錯誤
                except (IndexError, KeyError):
                    wx = {}

                if ElementName == '溫度':
                    temperature = wx.get('Temperature', '未知') + " 度"
                elif ElementName == '體感溫度':
                    apparent_temp = " (體：" + wx.get('ApparentTemperature', '未知') + " 度 )"

            # 處理「天氣現象」與「降雨機率」
            for i in range(len(extra)):
                ElementName = extra[i]['ElementName']

                if ElementName in ['天氣現象', '3小時降雨機率']:
                    for time_range in extra[i]['Time']:  # 遍歷所有 StartTime-EndTime 區間
                        start_time = datetime.strptime(time_range['StartTime'].split('+')[0].replace('T', ' '), '%Y-%m-%d %H:%M:%S')
                        end_time = datetime.strptime(time_range['EndTime'].split('+')[0].replace('T', ' '), '%Y-%m-%d %H:%M:%S')

                        # 檢查當前時間是否落在此範圍內
                        if start_time <= moment < end_time:
                            if ElementName == '天氣現象':
                                weather = time_range['ElementValue'][0].get('Weather', '未知')
                            elif ElementName == '3小時降雨機率':
                                rain_prob = "降雨機率 : " + time_range['ElementValue'][0].get('ProbabilityOfPrecipitation', '0') + " %"
                            break  # 找到符合條件的就跳出迴圈

            # 按照指定順序組合輸出
            relpy_text += f"{weather}, {temperature}{apparent_temp}\n{rain_prob}\n\n"

    if relpy_text == user[2:] +"\n":

        relpy_text = "天氣查詢失敗"

    else:
        relpy_text = relpy_text[:-2]
            
    return relpy_text
    
