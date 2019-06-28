from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb://localhost/")

with client:
    db = client.mongochat

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
            exit(1)

    elif ans.lower() in ["no", "n"]:
        print("enter a username to signup:")
        username = input()
        print("now enter password:")
        password = input()

        try:
            cur_user = db.users.find({"username": username}).next()
        except StopIteration:

            a = db.users.insert({
                "username": username,
                "password": password,
                "contacts": [],
                "channels": []
            })

            cur_user = db.users.find({
                '$and': [{"username": username}, {"password": password}]
            }).next()

        else:
            print("username already exists.")
            exit(1)

    else:
        print("wrong answer")
        exit(1)

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

            print("username to add: ")
            contact = input()

            db.users.update({"username": cur_user['username']}, {
                "$addToSet": {"contacts": contact}})

        elif command == "unfriend":
            print("username to unfriend: ")
            unfriend = input()

            db.users.update({"username": cur_user['username']}, {
                "$pull": {"contacts": unfriend}})

        elif command == "join":
            print("username to join: ")
            join = input()
            db.users.update({"username": cur_user['username']}, {
                "$addToSet": {"channels": join}})

            db.channels.update({"username": join}, {
                "$addToSet": {"members": cur_user['username']}})

        elif command == "leave":
            print("username to leave: ")
            join = input()
            db.users.update({"username": cur_user['username']}, {
                "$pull": {"channels": join}})

            db.channels.update({"username": join}, {
                "$pull": {"members": cur_user['username']}})

        elif command == "show entries":
            contacts = db.users.find({"username": cur_user['username']}, {"contacts"})
            for con in contacts:
                pprint(con)
        elif command == "load messages":
            pass
        elif command == "total messages":
            pass
        elif command == "new channel":
            pass

        command = input().lower()
