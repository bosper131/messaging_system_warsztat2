import argparse
from models import User
from connection import get_connection
parser = argparse.ArgumentParser()
parser.add_argument('-u', "--username", help="")
parser.add_argument('-p', "--password", help="")
parser.add_argument('-i', "--email", help="")
parser.add_argument('-n',"--new-pass", help="")
parser.add_argument('-e',"--edit", help="")
parser.add_argument('-d', "--delete", help="")
parser.add_argument('-l', "--list", help="")

args = parser.parse_args()
print(args)

print(args.username)
print(args.password)
print(args.email)
print(args.edit)
print(args.delete)

def create_user(username,password,email):
    print("CREATING NEW USER")
    c = get_connection()
    cursor = c.cursor()
    u = User()
    if u.get_item_by_login(username,cursor)==None and u.get_item_by_email(email,cursor)==None and len(password)>=8:
        u.username = username
        u.set_password(password, "1")
        u.email = email
        u.save(cursor)
        c.close()
    else:
        print ("Oj stary mail/login już jest w bazie.Ewentualnie hasło za krótkie. Ma być >= 8 znaków. Zmień login/mail lub hasło")

def change_password(username,password,loginToEdit,new_pass):
    print("CHANGING PASSWORD IN PROGRESS")
    c = get_connection()
    cursor = c.cursor()
    u = User()
    u.set_password(password, "1")
    if u.get_user_by_password(username,cursor)[1]==u.hashed_password and u.get_item_by_login(loginToEdit,cursor) and len(new_pass)>=8:
        u._User__id = u.get_user_by_password(username,cursor)[0]
        u.username = username
        u.set_password(new_pass, "1")
        u.email = u.get_user_by_password(username,cursor)[2]
        u.save(cursor)
        c.close()
    else:
        print(
            "Nie ma takiego loginu lub hasło jest nie to samo. Ewentualnie hasło za krótkie. Ma być >= 8 znaków. Podaj inne/poprawne hasło albo poprawny login ")

def delete_user(username, password):
    print("DELETE USER IN PROGRESS")
    c = get_connection()
    cursor = c.cursor()
    u = User()
    u.set_password(password, "1")
    if u.get_user_by_password(username, cursor)[1] == u.hashed_password:
        u.delete_user(username,cursor)
        c.close()
    else:
        print("Złe hasło/login")

def list_users():
    print("SHOW ALL USERS")
    c = get_connection()
    cursor = c.cursor()
    u = User()
    allUsers = u.show_users(cursor)
    for i in allUsers:
        print(i)
    c.close()



if args.username and args.password and not args.edit and not args.delete:
    create_user(args.username,args.password,args.email)


elif args.username and args.password and args.edit and args.new_pass and not args.delete:
    change_password(args.username,args.password,args.edit, args.new_pass)

elif args.username and args.password and args.delete:
    delete_user(args.username,args.password)

elif args.list:
    list_users()

else:
    print(""" Improper combination
    usage: python3 user_administration.py [-u USERNAME] [-p PASSWORD] [-i EMAIL]  - create user
                            [-u USERNAME] [-p PASSWORD] [-e EDIT] [-n NEW_PASS] - change password
                            [-u USERNAME] [-p PASSWORD] [-d DELETE] - delete user
                            [-l LIST] - list of all users """)