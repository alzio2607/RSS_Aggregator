import pymysql

class Database:
    con=""
    def __init__(self):

        host = "127.0.0.1"
        user = "root"
        password = "Skenzo_Dev"
        db = "Rss"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)

    def get_db_con(self):
        return self.con
