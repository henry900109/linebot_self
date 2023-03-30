import json
from linebot.models import (
    FlexSendMessage,
    BubbleContainer,
    BoxComponent,
    TextComponent,
    ButtonComponent,
    MessageAction
)
def test():
    return "hello world"
def profile(profile):
    # name = profile.display_name
    id = profile.user_id
    # pic = profile.picture_url
    #m = profile.status_message
        #     'profile_name': profile.display_name,
        # 'profile_id': profile.user_id,
    return id
def group(profile):
    id = profile.group_id  # 群組 ID
    name = profile.group_name  # 群組名稱
    pic = profile.picture_url # 群組照片 URL
    return name 

def flex():
    bubble = BubbleContainer(
    direction='ltr',
    body=BoxComponent(
        layout='vertical',
        contents=[
            TextComponent(text='請選擇一個選項：'),
            ButtonComponent(
                style='primary',
                color='#00a9e0',
                action=MessageAction(label='選項一', text='選項一')
            ),
            ButtonComponent(
                style='primary',
                color='#00a9e0',
                action=MessageAction(label='選項二', text='選項二')
            ),
            ButtonComponent(
                style='primary',
                color='#00a9e0',
                action=MessageAction(label='選項三', text='選項三')
            )
        ]
    )
)
    flex_message = FlexSendMessage(alt_text='請選擇一個選項：', contents=bubble)
    return flex_message

# 回覆訊息

#當使用者點擊選項按鈕時，LINE Bot 會收到一個訊息事件，其中包含了按下的按鈕的回傳值，你可以在訊息處理程式中取得該回傳值，根據不同的回傳值做出不同的回應。



