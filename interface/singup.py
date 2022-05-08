from hashlib import md5
from db_utils import DBUtils
from getpass import getpass

db = DBUtils("testdb", "postgres", "1590")

def quiz():
    login = input("Login: ")
    password = getpass("Password: ")
    confirm = getpass("Confirm Password: ")

    if password != confirm:
        print("Passwords are not the same")
        return

    db.create_user({"login": login, 
                    "password": md5(password.encode('utf-8')).hexdigest(), 
                    "key": md5(f'{login}_{password}'.encode('utf-8')).hexdigest()})
    print("User created")

if __name__ == "__main__":
    quiz()
    db.shutdown()