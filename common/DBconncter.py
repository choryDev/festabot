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

    def insert_festa_desc_query(self, user_token, id):
        select_query = "select * from user_tb where user_token = '"+user_token+"'"
        db_obj = DBconncter.select_query('', select_query)
        conn = pymysql.connect(host=host, user=user,
                               password=password, db=db, charset='utf8')
        curs = conn.cursor()
        if len(db_obj) == 0:
            sql = "insert into user_tb values (%s, %s, NOW())"
            curs.execute(sql, (user_token, id))
        else:
            sql = "UPDATE user_tb SET festa_id = %s, time = NOW() WHERE user_token = %s"
            curs.execute(sql, (id, user_token))
        conn.commit()
        conn.close()

    def selected_out(self, user_token):         #빠져 나오는 쿼리
        delete_query = "DELETE FROM user_tb WHERE user_token = %s"
        conn = pymysql.connect(host=host, user=user,
                               password=password, db=db, charset='utf8')
        curs = conn.cursor()
        curs.execute(delete_query, (user_token))
        conn.commit()
        conn.close()

    def insert_query(self, query):
        conn = pymysql.connect(host=host, user=user,
                               password=password, db=db, charset='utf8')
        curs = conn.cursor()
        curs.execute(query)
        conn.commit()
        conn.close()

