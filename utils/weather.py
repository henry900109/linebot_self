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
    element_name = "溫度,天氣現象,3小時降雨機率,體感溫度"

    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-{dataid_code[dataid]}?Authorization={weather_apikey}&LocationName={user[5:-2]}&ElementName={element_name}'
    response = requests.get(url)
   
    data = response.json()

    extra = data['records']['Locations'][0]['Location'][0]['WeatherElement']
    relpy_text = user[2:] +"\n"
    # 以「3小時降雨機率」的 StartTime 為基準，每 3 小時一次
    for time_range in extra[2]['Time']:  # 3小時降雨機率
        start_time = datetime.strptime(time_range['StartTime'].split('+')[0].replace('T', ' '), '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(time_range['EndTime'].split('+')[0].replace('T', ' '), '%Y-%m-%d %H:%M:%S')

        # 檢查是否符合使用者選擇的時間範圍
        if date_code[user[:2]] <= start_time and str(date_code[user[:2]].date()) in str(start_time):

            # 記錄時間（統一顯示 3 小時區間的開始時間）
            relpy_text += start_time.strftime('%m/%d %H點') + '\n'

            # 初始化天氣資訊變數
            weather = "未知"      # 天氣現象 (如 陰、多雲)
            temperature = "未知"  # 溫度
            apparent_temp = ""    # 體感溫度
            rain_prob = "降雨機率 : 無數據"  # 預設

            # 取得「3小時降雨機率」
            rain_prob = "降雨機率 : " + time_range['ElementValue'][0].get('ProbabilityOfPrecipitation', '0') + " %"

            # 取得「天氣現象」
            for wx_time in extra[3]['Time']:  # 天氣現象
                wx_start = datetime.strptime(wx_time['StartTime'].split('+')[0].replace('T', ' '), '%Y-%m-%d %H:%M:%S')
                wx_end = datetime.strptime(wx_time['EndTime'].split('+')[0].replace('T', ' '), '%Y-%m-%d %H:%M:%S')

                if wx_start <= start_time < wx_end:
                    weather = wx_time['ElementValue'][0].get('Weather', '未知')
                    break  # 找到符合條件的就跳出迴圈

            # 取得「溫度」與「體感溫度」對應的 `DataTime`
            for temp_time in extra[0]['Time']:  # 溫度
                temp_dt = datetime.strptime(temp_time['DataTime'].split('+')[0].replace('T', ' '), '%Y-%m-%d %H:%M:%S')

                if start_time <= temp_dt < end_time:
                    temperature = temp_time['ElementValue'][0].get('Temperature', '未知') + " 度"
                    break  # 找到符合條件的就跳出迴圈

            for app_temp_time in extra[1]['Time']:  # 體感溫度
                app_temp_dt = datetime.strptime(app_temp_time['DataTime'].split('+')[0].replace('T', ' '), '%Y-%m-%d %H:%M:%S')

                if start_time <= app_temp_dt < end_time:
                    apparent_temp = " (體：" + app_temp_time['ElementValue'][0].get('ApparentTemperature', '未知') + " 度 )"
                    break  # 找到符合條件的就跳出迴圈

            # 按照指定順序組合輸出
            relpy_text += f"{weather}, {temperature}{apparent_temp}\n{rain_prob}\n\n"

    if relpy_text == user[2:] +"\n":

        relpy_text = "天氣查詢失敗"

    else:
        relpy_text = relpy_text[:-2]
            
    return relpy_text
    

