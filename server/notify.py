import requests
import os
def notify(message):
    
    # LINE Notify 權杖
    token = os.getenv("line_notify_token")

    # HTTP 標頭參數與資料

    headers = { "Authorization": "Bearer " + token }
    data = {'message':'\n'+message}

    # 以 requests 發送 POST 請求
    requests.post("https://notify-api.line.me/api/notify",headers = headers, data = data)
    # headers = headers, data = data, files = files)
if __name__ == '__main__':
    print(notify("我是卓子揚"))
        