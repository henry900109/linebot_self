from linebot.models import QuickReply, QuickReplyButton,PostbackAction


#縣市名
def countryname():
    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton( action=PostbackAction ( label="新北市", data="C新北市" ) ),
                            QuickReplyButton( action=PostbackAction ( label="臺北市", data="C臺北市" ) ),
                            ]
    )
    return quick_reply

#區名
def town(cityname):
    if cityname == "C新北市":
        quick_reply=QuickReply(
                        items=[
                            QuickReplyButton( action=PostbackAction ( label="板橋區", data="T板橋區" ) ),
                            QuickReplyButton( action=PostbackAction ( label="新莊區", data="T新莊區" ) ),
                            QuickReplyButton( action=PostbackAction ( label="鶯歌區", data="T鶯歌區" ) ),
                            QuickReplyButton( action=PostbackAction ( label="三重區", data="T三重區" ) ),
                            ])
    else:
        quick_reply=QuickReply(
                        items=[
                            QuickReplyButton( action=PostbackAction ( label="中正區", data="T中正區" ) ),
                            QuickReplyButton( action=PostbackAction ( label="萬華區", data="T萬華區" ) ),
                            QuickReplyButton( action=PostbackAction ( label="文山區", data="T文山區" ) ),
                            QuickReplyButton( action=PostbackAction ( label="南港區", data="T南港區" ) ),
                            ])
    return quick_reply