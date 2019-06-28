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
            contacts = db.users.find({"username": cur_user['username']}, {"contacts"}).next()['contacts']
            channels = db.users.find({"username": cur_user['username']}, {"channels"}).next()['channels']

            contacts = sorted(contacts)
            channels = sorted(channels)

            print("contacts, sorted alphabetically", contacts)
            print("channels, sorted alphabetically", channels)

        elif command == "load messages":
            print("enter 1 for contacts or 2 for channels")
            option = input()
            if option == "1":
                print("contact username:")
                con_l = input()
                msg_l = db.chats.find({
                    "$and": [{"participant": cur_user['username']},
                             {"participant": con_l}]},
                    {"messages": {"$slice": -3}}).next()['messages']
                for ms in msg_l:
                    print("{}:\n\t {} <<{}>>".format(ms['sender'], ms['body'], ms['date']))

            else:
                print("channel username:")
                cha_l = input()

                members = db.channels.find({"username": cha_l})
                try:
                    members = members.next()['members']
                except StopIteration:
                    print("channel has no members")
                else:
                    if cur_user['username'] in members:
                        posts = db.channels.find({"username": cha_l},
                                                 {"posts": {"$slice": -5}})

                        try:
                            posts = posts.next()['posts']
                        except StopIteration:
                            print("channel has no post")
                        else:
                            for post in posts:
                                print("{} <<{}>>".format(post['body'], post['date']))

                    else:
                        print("you are not a member of this channel.")

        elif command == "total messages":
            print("username to show:")
            user_t = input()
            try:
                counter = int(db.chats.find({
                    "$and": [{"participant": cur_user['username']},
                             {"participant": user_t}]},
                    {"counter"}).next()['counter'])
            except StopIteration:
                print("something went wrong.")
            else:
                print("total number of messages between you and {} is: {}".format(user_t, counter))

        elif command == "new channel":
            pass

        elif command == "send message":
            pass
        elif command == "publish post":
            pass

        print("enter next command or quit: ")
        command = input().lower()
