from linebot.models import QuickReply, QuickReplyButton,PostbackAction


#縣市名
def countryname():
    location = ["宜蘭縣","花蓮縣","臺東縣","澎湖縣","金門縣","連江縣","臺北市","新北市","桃園市","臺中市","臺南市","高雄市","基隆市","新竹縣","新竹市","苗栗縣","彰化縣","南投縣","雲林縣","嘉義縣","嘉義市","屏東縣"]
    items = []
    for item in location:
        items.append(QuickReplyButton( action=PostbackAction ( label=item, data="C" + item ) ))
    quick_reply=QuickReply(items)
    return quick_reply

#區名
def town(cityname):
    if cityname == "C新北市":
        quick_reply=QuickReply(
                        items=[
                            QuickReplyButton( action=PostbackAction ( label="板橋區", data="T新北市板橋區" ) ),
                            QuickReplyButton( action=PostbackAction ( label="新莊區", data="T新北市新莊區" ) ),
                            QuickReplyButton( action=PostbackAction ( label="鶯歌區", data="T新北市鶯歌區" ) ),
                            QuickReplyButton( action=PostbackAction ( label="三重區", data="T新北市三重區" ) ),
                            ])
    else:
        quick_reply=QuickReply(
                        items=[
                            QuickReplyButton( action=PostbackAction ( label="中正區", data="T臺北市中正區" ) ),
                            QuickReplyButton( action=PostbackAction ( label="萬華區", data="T臺北市萬華區" ) ),
                            QuickReplyButton( action=PostbackAction ( label="文山區", data="T臺北市文山區" ) ),
                            QuickReplyButton( action=PostbackAction ( label="南港區", data="T臺北市南港區" ) ),
                            ])
    return quick_reply

def tomorrow_or_today(check):
    check = check + "天氣"
    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton( action=PostbackAction ( label="今天", data= "D今天" + check ) ),
                            QuickReplyButton( action=PostbackAction ( label="明天", data= "D明天" + check ) ),
                        ])
    return quick_reply