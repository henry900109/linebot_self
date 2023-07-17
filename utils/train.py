from authorization import data, Auth
import json
import requests
import re
from pprint import pprint
from datetime import datetime


def check_success(url):
    try:
        d = data(app_id, app_key, auth_response)
        data_response = requests.get(url, headers=d.get_data_header())

    except:
        a = Auth(app_id, app_key)
        auth_response = requests.post(auth_url, a.get_auth_header())
        d = data(app_id, app_key, auth_response)
        data_response = requests.get(url, headers=d.get_data_header())

    """查看是否成功get"""
    # print(auth_response)
    # print(data_response)

    return data_response


def search_sta_id(sta_name):
    """獲取最新車站資訊"""
    # url = "https://tdx.transportdata.tw/api/basic/v3/Rail/TRA/Station?%24format=JSON"
    # full_data = json.loads(check_success(url).text)['Stations']
    # pprint(full_data)

    """讀取JSON"""
    with open('train_station.json', encoding='utf-8') as json_data:
        full_data = json.load(json_data)['Stations']

    """判斷使用者是否錯字"""
    try:
        filtered_stations = filter(
            lambda x: x["StationName"]["Zh_tw"] == sta_name, full_data)
        station_id = next(filtered_stations, None)
        response = station_id['StationID']
        return response

    except:
        response = '請確認「' + sta_name + '」是否打錯車站名稱！'
        print(response)
        return TypeError


def find_Fare(start, end):
    """獲取最新車票資訊"""
    url = f'https://tdx.transportdata.tw/api/basic/v3/Rail/TRA/ODFare/{start}/to/{end}?%24format=JSON'
    data_file = json.loads(check_success(url).text)

    return data_file


def sche_time(start, end):

    # 當前時間與日期
    time = datetime.now().strftime("%H:%M")
    date = datetime.now().date()

    # 過濾過期時刻表
    filter_pa = f"StopTimes/any(st: st/StationID eq \'{start}\' and st/DepartureTime ge \'{time}\')"

    # 取得前5筆資料
    top_par = 5

    url = f'https://tdx.transportdata.tw/api/basic/v3/Rail/TRA/DailyTrainTimetable/OD/{start}/to/{end}/{date}?%24filter={filter_pa}&%24top={top_par}&%24format=JSON'

    data_file = json.loads(check_success(url).text)
    fare_da = find_Fare(start, end)['ODFares']

    for i in range(top_par):
        Info = data_file['TrainTimetables'][i]['TrainInfo']

        Direction = Info['Direction']
        Tra_Type = Info['TrainTypeCode']
        for j in range(len(fare_da)):
            fare_Train = fare_da[j]['TrainType']
            fare_Direction = fare_da[j]['Direction']
            if Direction == fare_Direction and int(Tra_Type) == fare_Train:
                fare = fare_da[j]['Fares'][0]['Price']

        Tra_Type_Name = Info['TrainTypeName']['Zh_tw']
        TrainNo = Info['TrainNo']
        Start_Sta_Na = Info['StartingStationName']['Zh_tw']
        End_Sta_Na = Info['EndingStationName']['Zh_tw']

        StopTimes = data_file['TrainTimetables'][i]['StopTimes']
        start_Dep = StopTimes[0]['DepartureTime']
        destn_Arr = StopTimes[1]['ArrivalTime']
        print(f"{Tra_Type_Name}{TrainNo} ({Start_Sta_Na} → {End_Sta_Na}) ")
        print(f'{start_Dep} {start_sta} → {destn_Arr} {destn_sta}')
        print(f'票價：${fare}')
        print()

    return


def real_time():

    # 取得指定[車次]的列車即時位置動態資料
    url = f'https://tdx.transportdata.tw/api/basic/v3/Rail/TRA/TrainLiveBoard/TrainNo/1263?%24top=30&%24format=JSON'

    with open('real_time.json', "w", encoding='utf-8') as json_file:
        data_file = json.loads(check_success(url).text)
        json.dump(data_file, json_file, ensure_ascii=False)

    # data_file = json.loads(check_success(url).text)

    return

def main(user):
    global start_sta
    global destn_sta
    pattern = r'從(.+?)到(.+)'
    match = re.search(pattern, user)

    try:
        start_sta = match.group(1)
        destn_sta = match.group(2)

    except:
        response = '輸入錯誤！\nEx：從板橋到鶯歌'
        print(response)
        return

    print('起點：' + start_sta)
    start_id = search_sta_id(start_sta)
    print('終點：' + destn_sta)
    destn_id = search_sta_id(destn_sta)

    sche_time(start_id, destn_id)



app_id = 'Your_Id'
app_key = 'Your_Key'

auth_url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"

print(main('從鶯歌到桃園'))
