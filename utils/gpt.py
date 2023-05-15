import openai
import time
def gpt3_5(token, message,timeout = 10):

  openai.api_key = token
  start_time = time.time()
  response = openai.Completion.create(
                model='text-davinci-003',
                prompt=message,
                max_tokens=256,
                temperature=0.9,
                frequency_penalty=0,
                #預設的 OPENAI_FREQUENCY_PENALTY 為 0.5，OPENAI_PRESENCE_PENALTY 為 0.0
                presence_penalty=0.6,
                stop=[" Human:", " AI:"]
                #
                )
            # 接收到回覆訊息後，移除換行符號
  if time.time() - start_time >= timeout:
     return 'Error(0) : 無法取得回覆，請稍後再試！'
  else:
    try:
      reply_msg = response["choices"][0]["text"][response["choices"][0]["text"].index("AI:"):]

      reply_msg = reply_msg.replace('AI:','').strip()

      return reply_msg
    except:
       return 'Error : 無法取得回覆，請稍後再試！'

def img(token, message,timeout = 10):
  start_time = time.time()
  PROMPT = message

  openai.api_key = token

  response = openai.Image.create(
    prompt=PROMPT,
    model="image-alpha-001", 
    n=1,
    temperature=0.5,
    size="256x256",
  )
  if time.time() - start_time >= timeout:
     return 'Error : 無法取得回覆，請稍後再試！'
  else:
     return response["data"][0]["url"]
   

if __name__ == '__main__':
    print(gpt3_5(token="", message="你是誰?"))
    print(img(token="", message="An eco-friendly computer from the 90s in the style of vapor"))
