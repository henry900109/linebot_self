import gspread
import random
from oauth2client.service_account import ServiceAccountCredentials
# 猜數字的函數
def Guessnumber(user_input,range_min,range_max,answer):

    try:
        user_number = int(user_input)

        if user_number < range_min or user_number > range_max:
            gamemode = False
            return "請輸入範圍內的數字！"
        
        if user_number == answer:
            return "f恭喜你, 猜中了！" 
        
        elif user_number < answer:
            return "太小了，再猜一次！" 
        
        else:
            return "太大了，再猜一次！" 
        
    except ValueError:
        return "請輸入一個數字！"
def Guseenumder_start(userid):
    credential_path = r'/var/task/docs/optimal-signer-334903-d972d0dbeb67.json'

    # 設置要讀取的試算表名稱
    spreadsheet_name = 'linebot'


    # 建立憑證物件
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_path)

    # 連線到 Google Sheets API
    gc = gspread.authorize(credentials)
    sh = gc.open(spreadsheet_name)

    # 建立新的工作表
    worksheet_name = "Guessnumber"
    try:
        worksheet = sh.worksheet(worksheet_name)
    except:
        worksheet = sh.add_worksheet(title=worksheet_name, rows=1000, cols=1000)
        cell_list = worksheet.range('A1')
        cell_list[0].value = 'game'

        worksheet.update_cells(cell_list)
    range_min = 1
    range_max = 100
    answer = random.randint(range_min, range_max)
    count = 0
    # 寫入資料
    cell_list = worksheet.range('A2:A6')
    cell_list[0].value = userid
    cell_list[1].value = answer     #answer
    cell_list[2].value = range_min  #range_min
    cell_list[3].value = range_max  #range_max
    cell_list[4].value = count  #range_max

    worksheet.update_cells(cell_list)

    data = worksheet.get_all_values()
    return 


def Guessnumber_sheet():
    credential_path = r'/var/task/docs/optimal-signer-334903-d972d0dbeb67.json'

    # 設置要讀取的試算表名稱
    spreadsheet_name = 'linebot'


    # 建立憑證物件
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_path)

    # 連線到 Google Sheets API
    gc = gspread.authorize(credentials)
    sh = gc.open(spreadsheet_name)

    # 建立新的工作表
    worksheet_name = "Guessnumber"
    try:
        worksheet = sh.worksheet(worksheet_name)
    except:
        worksheet = sh.add_worksheet(title=worksheet_name, rows=1000, cols=1000)
        cell_list = worksheet.range('A1')
        cell_list[0].value = 'game'

        worksheet.update_cells(cell_list)

    # 寫入資料
    cell_list = worksheet.range('A6:A8')
    cell_list[0].value = int(cell_list[0][0]) + 1
    cell_list[1].value = 'True' #user_range_min
    cell_list[2].value = 'True' #user_range_max


    worksheet.update_cells(cell_list)

    data = worksheet.get_all_values()
