import psycopg2

USER_CREDENTIALS_TABLE_NAME = "user_credentials"
MESSAGES_TABLE_NAME = "messages"

class DBUtils:
    def __init__(self, db_name, user, password):
        self.db_name = db_name
        self.user = user
        self.password = password

        try:
            self.conn = psycopg2.connect(f"dbname={self.db_name} user={self.user} password={self.password}")
            self.cur = self.conn.cursor()
        except Exception:
            print("/DBUtils initialization/ ...Something went wrong :(")

    def query_executor(self, query: str, data: tuple, fetch_flag: bool):
        try:
            self.cur.execute(query, data)
            response = None
            if fetch_flag:
                response = self.cur.fetchall()
            self.cur.close()
            self.conn.commit()
            return response
        except Exception:
            print("/DBUtils/ ... Something went wrong :(")


    def create_user(self, data):
        query = """
                insert into user_credentials (login, password, key) values(%s, %s, %s)
        """
        data = tuple(data.values())
        self.query_executor(query, data, fetch_flag=False)

    def get_user_info(self, login):
        query = """
                select * from user_credentials where login = %s;
        """
        data = (login,)
        return self.query_executor(query, data, fetch_flag=True)

    def save_message(self, sender, message):
        query = """
                insert into messages (sender, message) values(%s, %s)
        """
        data = (sender, message)
        self.query_executor(query, data, fetch_flag=False)

    def select_all(self):
        query = """
                select login, key from user_credentials
        """
        data = tuple()
        return self.query_executor(query, data, fetch_flag=True)

    def shutdown(self):
        if self.conn is not None:
            self.conn.close()