from pymongo import MongoClient
from datetime import datetime

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
        print("wrong answer.")
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
            print("info updated.")

        elif command == "add contact":

            print("username to add: ")
            contact = input()

            db.users.update({"username": cur_user['username']}, {
                "$addToSet": {"contacts": contact}})
            print("contact added.")

        elif command == "unfriend":
            print("username to unfriend: ")
            unfriend = input()

            db.users.update({"username": cur_user['username']}, {
                "$pull": {"contacts": unfriend}})
            print("contact deleted.")

        elif command == "join":
            print("username to join: ")
            join = input()
            chs = db.channels.find({}, {"username"})
            for uch in chs:
                if uch['username'] == join:
                    db.users.update({"username": cur_user['username']}, {
                        "$addToSet": {"channels": join}})

                    db.channels.update({"username": join}, {
                        "$addToSet": {"members": cur_user['username']}})
                    break
            else:
                print("there is no such channel.")

        elif command == "leave":
            print("channel username to leave: ")
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

            print("contacts, sorted alphabetically: ", contacts)
            print("channels, sorted alphabetically: ", channels)

        elif command == "load messages":
            print("enter 1 for contacts or 2 for channels:")
            option = input()
            if option == "1":
                print("contact username:")
                con_l = input()
                try:
                    msg_l = db.chats.find({
                        "$and": [{"participants": cur_user['username']},
                                 {"participants": con_l}]},
                        {"messages": {"$slice": -3}}).next()['messages']
                    for ms in msg_l:
                        print("{}:\n\t {} <<{}>>".format(ms['sender'], ms['body'], ms['date']))
                except StopIteration:
                    print("no message found.")

            else:
                print("channel username:")
                cha_l = input()

                members = db.channels.find({"username": cha_l})
                try:
                    members = members.next()['members']
                except StopIteration:
                    print("channel has no members.")
                else:
                    if cur_user['username'] in members:
                        posts = db.channels.find({"username": cha_l},
                                                 {"posts": {"$slice": -5}})

                        try:
                            posts = posts.next()['posts']
                        except StopIteration:
                            print("channel has no post.")
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
                    "$and": [{"participants": cur_user['username']},
                             {"participants": user_t}]},
                    {"counter"}).next()['counter'])
            except StopIteration:
                print("something went wrong.")
            else:
                print("total number of messages between you and {} is: {}.".format(user_t, counter))

        elif command == "new channel":
            print("username for channel:")
            u_channel = input()
            all_chs = db.channels.find({}, {"username"})
            for ch in all_chs:
                if ch['username'] == u_channel:
                    print("username already exists.")
            else:
                db.channels.insert({
                    "username": u_channel,
                    "admin": cur_user['username'],
                    "members": [],
                    "posts": []})
                print("channel created.")

        elif command == "send message":
            print("enter recipient:")
            usr = input()
            snd_contacts = db.users.find({"username": cur_user['username']}, {"contacts"}).next()['contacts']
            if usr in snd_contacts:
                print("enter your message: ")
                ms_body = input()
                try:
                    db.chats.find({"$and": [
                        {"participants": cur_user['username']},
                        {"participants": usr}]}).next()
                except StopIteration:
                    db.chats.insert({
                        "participants": [cur_user['username'], usr],
                        "messages": [],
                        "counter": 0})
                finally:
                    db.chats.update({
                        "$and":
                            [{"participants": cur_user['username']},
                             {"participants": usr}]},
                        {"$inc": {"counter": 1},
                         "$addToSet": {"messages": {
                             "body": ms_body,
                             "sender": cur_user['username'],
                             "date": datetime.now()}}
                         })

                    print("sent.")
            else:
                print("user is not in your contacts.")

        elif command == "publish post":
            print("enter username of channel: ")
            ch_usr = input()
            try:
                admin = db.channels.find({"username": ch_usr}, {"admin"}).next()['admin']
            except StopIteration:
                print("there is no such channel.")
            else:
                if admin == cur_user['username']:
                    print("enter post body:")
                    post_body = input()
                    db.channels.update({"username": ch_usr}, {
                        "$addToSet": {
                            "posts": {
                                "body": post_body,
                                "date": datetime.now()
                            }
                        }
                    })
                else:
                    print("you are not the admin.")

        print("enter next command or quit: ")
        command = input().lower()
