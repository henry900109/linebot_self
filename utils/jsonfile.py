import json
import os
current_path = os.path.dirname(__file__)

def checkfile(id,username):
    with open(r'\var\task\docs\user.json') as f:
        data = json.load(f)
    if id in data:
        return True
    else:
        return False
        data[id] = username
        with open(r'..\docs\user.json', 'w') as f:
            json.dump(data, f,ensure_ascii=False)