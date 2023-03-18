import random
def hello():
    hello_dict = { 0 : "hello, master!", 1 : "your majesty, I'm here", 2 : "hey!, master" ,3 : "your majesty, what's up?" }
    num = random.randrange(4)
    return hello_dict[num]


def Goodbye():
    Goodbye_dict = { 0 : "No problem", 1 : "Yes, your majesty", 2 : "Copy that" ,3 : "Got it" }
    num = random.randrange(4)
    return Goodbye_dict[num]