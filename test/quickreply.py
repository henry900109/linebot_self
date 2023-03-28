"""
回傳日期
if event.postback.data.startswith('action=buy&itemid='):
        # 獲取使用者選擇的日期和時間
        selected_datetime = event.postback.params['datetime']

        # 回傳日期和時間給使用者
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"您選擇的日期和時間是：{selected_datetime}")
        )
"""

"""
設定post資料
QuickReplyButton(action=PostbackAction(label="Postback",data="回傳資料")


取得post 回來的資料
postback_data = event.postback.data
"""

"""
quick_reply=QuickReply(

                    items=[
                        QuickReplyButton(
                            action=PostbackAction(label="Postback",data="回傳資料")
                            ),
                        QuickReplyButton(
                            action=MessageAction(label="文字訊息",text="回傳文字")
                            ),
                        QuickReplyButton(
                            action=DatetimePickerAction(label="時間選擇",data='action=buy&itemid=1',mode='datetime')
                            ),
                        QuickReplyButton(
                            action=CameraAction(label="拍照")
                            ),
                        QuickReplyButton(
                            action=CameraRollAction(label="相簿")
                            ),
                        QuickReplyButton(
                            action=LocationAction(label="傳送位置")
                            )
                        ]
                    )
reply_text = TextSendMessage(text="文字訊息",quick_reply=quick_reply)


line_bot_api.reply_message(event.reply_token, reply_text)

"""