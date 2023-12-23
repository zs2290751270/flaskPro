import pymysql


class Execute:

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 3306
        self.username = 'root'
        self.password = 'Lova_0115'
        self.db = 'race'

        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            db=self.db
        )
        self.cursor = self.conn.cursor()

    def get_data_list(self, sql):
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        self.cursor.close()
        self.conn.close()
        return res

    def get_data_one(self, sql):
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        self.cursor.close()
        self.conn.close()
        return res

    def write_data_info(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        return self.cursor.rowcount



