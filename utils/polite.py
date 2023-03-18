import random
def hello():
    hello_dict = { 0 : "hello!", 1 : "I'm here", 2 : "hey!" ,3 : "what's up?" }
    num = random.randrange(4)
    return hello_dict[num]


def Goodbye():
    Goodbye_dict = { 0 : "Goodbye!", 1 : "Nice to see you", 2 : "ok!" ,3 : "Well.." }
    num = random.randrange(4)
    return Goodbye_dict[num]