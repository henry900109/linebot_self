import requests
from pprint import pprint
import json

# app_id = '409170177-a68f40a8-d82a-4f84'
# app_key = '95b175d8-ac70-48da-9a2f-c65c26011bd7'

# auth_url="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
# url = "https://tdx.transportdata.tw/api/basic/v3/Rail/TRA/Station?%24top=30&%24format=JSON"
# url = 'https://tdx.transportdata.tw/api/basic/v3/Rail/TRA/DailyTrainTimetable/OD/Inclusive/{0900}/to/{1070}/{2023-07-11}?%24top=30&%24format=JSON'
# url = 'https://tdx.transportdata.tw/api/basic/v3/Rail/TRA/DailyTrainTimetable/OD/0900/to/1070/2023-07-11?%24format=JSON'

class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        content_type = 'application/x-www-form-urlencoded'
        grant_type = 'client_credentials'

        return{
            'content-type' : content_type,
            'grant_type' : grant_type,
            'client_id' : self.app_id,
            'client_secret' : self.app_key
        }

class data():

    def __init__(self, app_id, app_key, auth_response):
        self.app_id = app_id
        self.app_key = app_key
        self.auth_response = auth_response

    def get_data_header(self):
        auth_JSON = json.loads(self.auth_response.text)
        access_token = auth_JSON.get('access_token')

        return{
            'authorization': 'Bearer '+access_token
        }

if __name__ == '__main__':
    try:
        d = data(app_id, app_key, auth_response)
        data_response = requests.get(url, headers=d.get_data_header())
    except:
        a = Auth(app_id, app_key)
        auth_response = requests.post(auth_url, a.get_auth_header())
        d = data(app_id, app_key, auth_response)
        data_response = requests.get(url, headers=d.get_data_header())    
    print(auth_response)
    pprint(auth_response.text)
    print(data_response)
    pprint(data_response.text)