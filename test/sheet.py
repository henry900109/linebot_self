import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 設置試算表憑證的路徑
def sheet():
    credential_path = r'/var/task/docs/optimal-signer-334903-d972d0dbeb67.json'

    # 設置要讀取的試算表名稱
    spreadsheet_name = 'linebot'


    # 建立憑證物件
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_path)

    # 連線到 Google Sheets API
    gc = gspread.authorize(credentials)
    sh = gc.open(spreadsheet_name)

    # 建立新的工作表
    new_worksheet_name = "Uc3e869190fa11d67f2a1ff4b65070e4f"
    worksheet = sh.add_worksheet(title=new_worksheet_name, rows=1000, cols=1000)

    # 寫入資料
    cell_list = worksheet.range('A1:B1')

    cell_list[0].value = 'game'
    cell_list[1].value = 'like'

    worksheet.update_cells(cell_list)

    data = worksheet.get_all_values()
    return data
