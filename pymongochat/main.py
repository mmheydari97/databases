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
        print("now enter password:")
        password = input()

        try:
            cur_user = db.users.find({
                '$and': [{"username": username}, {"password": password}]
            }).next()
        except StopIteration:
            print("incorrect username or password.")

    elif ans.lower() in ["no", "n"]:
        print("enter a username to signup:")
        username = input()
        print("now enter password:")
        password = input()

        a = db.users.insert({
            "username": username,
            "password": password,
            "contacts": [],
            "channels": []
        })
        cur_user = db.users.find({
            '$and': [{"username": username}, {"password": password}]
        }).next()

    print("enter next command or quit: ")
    command = input().lower()
    while command != "quit":
        if command == "info":
            print("first name: ")
            fname = input()

            print("last name: ")
            lname = input()

            print("student id: ")
            sid = input()

            print("stage: ")
            stage = input()

            print("entrance year: ")
            year = int(input())

            db.users.update({"username": cur_user['username']}, {
                "$set": {"info": {
                    "firstName": fname,
                    "lastName": lname,
                    "studentId": sid,
                    "stage": stage,
                    "year": year}}})

        elif command == "add contact":
            pass
        elif command == "unfriend":
            pass
        elif command == "join channel":
            pass
        elif command == "leave":
            pass
        elif command == "show entries":
            pass
        elif command == "load messages":
            pass
        elif command == "total messages":
            pass
        elif command == "new channel":
            pass

        command = input().lower()
