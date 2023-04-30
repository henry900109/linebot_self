import openai

def gpt3(token, message):

  openai.api_key = token

  response = openai.Completion.create(
                model='text-davinci-003',
                prompt=message,
                max_tokens=256,
                temperature=0.5,
                )
            # 接收到回覆訊息後，移除換行符號

  reply_msg = response["choices"][0]["text"].replace('\n','')

  return reply_msg

if __name__ == '__main__':
    print(gpt3(token="", message="紅茶要怎麼做?"))

