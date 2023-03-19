import openai

def gpt3_5(token,message):
    openai.api_key = token
    respone = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",

    messages=[
            {"role": "user", "content": message},
    ]
    )
    return respone.choices[0].message.content