import argparse
from models import Message, User
from connection import get_connection
parser = argparse.ArgumentParser()
parser.add_argument('-u', "--username", help="")
parser.add_argument('-p', "--password", help="")
parser.add_argument('-l', "--list", help="")
parser.add_argument('-t', "--to", help="")
parser.add_argument('-s',"--send", help="")
parser.add_argument('-d',"--date", help="")
args = parser.parse_args()


def list_messages(username,password):
    print("LISTING ALL MESSAGES FOR GIVEN USER")
    c = get_connection()
    cursor = c.cursor()
    u = User()
    u.set_password(password, "1")

    if u.get_item_by_login(username,cursor) and u.get_user_by_password(username,cursor)[1]==u.hashed_password:
        id = u.get_user_by_password(username,cursor)[0]
        m = Message()
        allMess = m.load_all_messages_for_user(id,cursor)
        print("BODY|creation_date|from USER")
        for mess in allMess:
            print(mess)
        c.close()
    else:
        print ("Nie ma takiego usera lub podałeś złe hasło/login")


def sent_to(username,password,toUserName, bodyToUser,creation_date):
    print("SEND A MESSAGE TO A GIVEN USER")
    c = get_connection()
    cursor = c.cursor()
    u = User()
    u.set_password(password, "1")
    if u.get_item_by_login(username,cursor) and u.get_user_by_password(username,cursor)[1]==u.hashed_password and u.get_item_by_login(toUserName,cursor)[0]:
        m = Message()
        m.body = bodyToUser
        m.creation_date = creation_date
        m.from_user=u.get_user_by_password(username,cursor)[0]
        m.to_user=u.get_user_by_password(toUserName,cursor)[0]
        m.save_message(cursor)
        c.close()
    else:
        print ("Nie ma takiego usera lub podałeś złe hasło/login lub nie ma usera do ktorego chcesz cos wyslac")




if args.username and args.password and args.list:
    list_messages(args.username,args.password)


elif args.username and args.password and args.to and args.send and args.date:
    sent_to(args.username,args.password,args.to,args.send,args.date)

else:
     print(""" Improper combination or lack of parameters
     usage: python3 messages_administration.py  [-u USERNAME] [-p PASSWORD] [-l LIST]  - list all messages for a given user
                           [-u USERNAME] [-p PASSWORD] [-d DATE] [-t TO] [-s SEND]  - send a message from USERNAME TO "TO"
  """)