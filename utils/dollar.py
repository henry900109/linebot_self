import requests
def UAH2TWD():
    """
    烏克蘭 Youtube Premium 換算新臺幣
    """
    r=requests.get("https://tw.rter.info/capi.php")
    currency=r.json()
    dollar = (149/currency["USDUAH"]['Exrate'])*currency["USDTWD"]['Exrate']
    callback = "烏克蘭Youtube Premium\n" +currency["USDUAH"]['UTC'].split()[0].split("-")[0] + "年"+ currency["USDUAH"]['UTC'].split()[0].split("-")[1] + "月\n新臺幣: " + str(dollar) + "元\n6人每人: " + str(dollar/6) + "元\n更新時間: " + currency["USDUAH"]['UTC'] + "和" + currency["USDTWD"]['UTC']
    return callback
if __name__ == '__main__':
    UAH2TWD()
