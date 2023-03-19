import openai

def gpt3_5(token,message):
    openai.api_key = token
    respone = openai.ChatCompletion.create(

    model="gpt-3.5-turbo",

    messages = [ {"role": "user", "content": message}]

    )

    respone = respone.choices[0].message.content

    respone = respone.replace("\n","",True) if "\n" in respone[10] else respone

    return respone

if __name__ == '__main__':
    print(gpt3_5(token="",message="你是誰?"))