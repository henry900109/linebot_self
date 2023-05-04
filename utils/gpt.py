import openai

def gpt3_5(token, message):

  openai.api_key = token

  response = openai.Completion.create(
                model='text-davinci-003',
                prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: " +message,
                max_tokens=256,
                temperature=0.9,
                frequency_penalty=0,
                #預設的 OPENAI_FREQUENCY_PENALTY 為 0.5，OPENAI_PRESENCE_PENALTY 為 0.0
                presence_penalty=0.6,
                stop=[" Human:", " AI:"]
                #
                )
            # 接收到回覆訊息後，移除換行符號
            
  reply_msg = response["choices"][0]["text"][response["choices"][0]["text"].index("AI:"):]

  reply_msg = reply_msg.replace('AI:','').strip()

  return reply_msg

def img(token, message):
  
  PROMPT = message

  openai.api_key = token

  response = openai.Image.create(
    prompt=PROMPT,
    n=1,
    size="256x256",
  )

  return response["data"][0]["url"]
   

if __name__ == '__main__':
    print(gpt3_5(token="", message="你是誰?"))
    print(img(token="", message="An eco-friendly computer from the 90s in the style of vapor"))
