import openai

def gpt3_5(token, message):

  openai.api_key = token

  response = openai.Completion.create(
                model='text-davinci-003',
                prompt=message,
                max_tokens=256,
                temperature=0,
                frequency_penalty=0,
                #預設的 OPENAI_FREQUENCY_PENALTY 為 0.5，OPENAI_PRESENCE_PENALTY 為 0.0
                presence_penalty=0.6
                #
                )
            # 接收到回覆訊息後，移除換行符號

#   reply_msg = response["choices"][0]["text"].replace('\n','')
  reply_msg = response["choices"][0]["text"]
  return reply_msg

if __name__ == '__main__':
    print(gpt3_5(token="", message="你是誰?"))
