from colorama import Fore, Style
from rmq_utils import RabbitMQUtils
from db_utils import DBUtils
from getpass import getpass
from hashlib import md5
import time
import cryptocode

PASSWORD_MAPPING = 2
KEY_MAPPING = 3
SPLITTER = "__+__"

db = DBUtils("testdb", "postgres", "1590")

class Interface:
    def __init__(self):
        self.session_login = ""
        self.session_key = ""

    def login(self) -> bool:
        login = input("Your login: ")
        response = db.get_user_info(login)
        if not response:
            print(f"/Authorization/ No user was found...")
            return False

        correct_password = response[0][PASSWORD_MAPPING]
        password = getpass("Password: ")

        if correct_password != md5(password.encode("utf-8")).hexdigest():
            print("/Authorization/ Wrong password")
            return False

        print("/Authorization/ Authorization was successful")
        self.session_login = login
        self.session_key = response[0][KEY_MAPPING]

        return True

    def run(self):
        rabbitmq = RabbitMQUtils()
        command_line_text = ""
        while True:
            command_line_text = input("Entry message to send: ")
            result_message = f"{self.session_login}{SPLITTER}{cryptocode.encrypt(command_line_text, self.session_key)}"

            rabbitmq.send_message(result_message)

            if command_line_text != "quit()":
                print(f"{Fore.GREEN}Message was successfully sent {Style.RESET_ALL}\n")
            else:
                break

            time.sleep(0.001)

        rabbitmq.close_connection()
        db.shutdown()