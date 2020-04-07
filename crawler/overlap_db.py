import pymysql

#인스타 중복 검색
def insta_overlap(id):
    conn = pymysql.connect(host='mydb.cstof8mab94c.ap-northeast-2.rds.amazonaws.com',
                           user='admin',
                           password='123123123',
                           db='festabot',
                           charset='utf8')
    cur = conn.cursor()
    sql = 'select id from insta_tb where id = %s'
    cur.execute(sql, id)
    rows = cur.fetchone()
    # print(row)

    try:
        for row in rows:
            if(str(id) == str(row)):
                #이미 존재
               return 1
    except TypeError as e:
        return 0 #새로운 값


#새로운 데이터 중복 검색
def title_overlap(title2):
  conn = pymysql.connect(host='mydb.cstof8mab94c.ap-northeast-2.rds.amazonaws.com',
                         user='admin',
                         password='123123123',
                         db='festabot',
                         charset = 'utf8')
  cur = conn.cursor()
  sql = 'select title from festival_tb where title = %s'
  cur.execute(sql, title2)
  row = cur.fetchone()
  # print(row)

  try:
    for field in row:
     if(str(title2) == str(field)):
      #이미 존재
      return 1
  except TypeError as e:
      #존재 x
      return 0




