from interface.db_utils import DBUtils
import cryptocode

db = DBUtils("testdb", "postgres", "1590")

class Decoder:
    def __init__(self):
        self.user_keys = {}
        response = db.select_all()

        for record in response:
            self.user_keys[record[0]] = record[1]

    def decrypt(self, user, message):
        return cryptocode.decrypt(message, self.user_keys[user])
