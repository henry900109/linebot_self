import json
import os


def checkfile(id,username):
    # current_path = os.path.dirname(__file__)
    # return current_path
    with open(r'/var/task/docs/user.json') as f:
        data = json.load(f)
    if id in data:
        return True
    else:
        return False
        data[id] = username
        with open(r'/var/task/docs/user.json', 'w') as f:
            json.dump(data, f,ensure_ascii=False)
