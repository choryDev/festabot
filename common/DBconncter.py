import pymysql

host = 'mydb.cstof8mab94c.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = '123123123'
db = 'festabot'

class DBconncter:
    def select_query(self, query):
        conn = pymysql.connect(host=host, user=user,
                               password=password, db=db, charset='utf8')
        curs = conn.cursor()
        sql = query #파라미터로 쿼리를 넣음
        curs.execute(sql)
        data = curs.fetchall()
        conn.close()

        return data

