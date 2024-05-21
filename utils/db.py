from pymongo.mongo_client import MongoClient
import os
def connect_DB(profile):
    id = profile.user_id
    name = profile.display_name
    uri = os.getenv("DB_key")
    client = MongoClient(uri)
    try:
        client.admin.command('ping')
        # print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        return e
    mydb = client["linebot"]
    collection  = mydb["custom"]
    row = [row for row in collection.find({'usrID':id})]
    if (row == []):
        collection.insert_one({'name':name,"usrID":id})
    return "ok"