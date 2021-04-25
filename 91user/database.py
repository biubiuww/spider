import sqlite3


class ClientSqlite():

    def __init__(self, dbName="./91user.db"):
        self.conn = sqlite3.connect(dbName)
        self.cur = self.conn.cursor()

    def close_conn(self):
        self.cur.close()
        self.conn.close()

    def create_table(self):
        sql = '''CREATE table users(
                        id int primary key ,
                        uid varchar(255) not null ,
                        name varchar(255) not null ,
                        data text
                    )'''
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            print('[ERROR] %s' + e)
            return False

    def fetchall_table(self,sql,limit_flag=True):
        try:
            war_msg = ' The [{}] is empty or equal None!'.format(sql)
            self.cur.execute(sql)
            if limit_flag == True:
                result = self.cur.fetchall()
                return result if len(result) > 0 else war_msg
            else:
                result = self.cur.fetchone()
                return result if len(result) > 0 else war_msg
        except Exception as e:
            print('[SELECT TABLE ERROR]' + e)

    def inset_update_table(self,sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            print('[INSERT/UPDATE TABLE ERROR]' + e)
            return False