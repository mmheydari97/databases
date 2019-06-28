from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb://localhost/")

with client:
    db = client.mongochat

    # print(db.collection_names())
    # messages = db.chats.find()
    # print(messages.next())

    print("already a member?")
    ans = input()
    if ans.lower() in ["yes", "y"]:
        print("enter a username to login:")
        username = input()
        print("now enter pass word:")
        password = input()



    elif ans.lower() in ["no", "n"]:
        print("enter a username to signup:")
        username = input()

