import requests

# 資料開放平台 API 網址
url = "https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.json"

# 指定路線編號
route = "802"

# 發送 GET 請求並取得回應
response = requests.get(f"{url}?route={route}")

# 解析 JSON 格式的回應
data = response.json()

# 顯示時刻表資訊
for stop in data["Route"]["Stop"]:
    print(f"站牌名稱：{stop['StopName']}")
    print("時刻表：")
    for time in stop["EstimateTime"]:
        print(f"\t{time}")
    print()
