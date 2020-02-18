import pymysql


def title_overlap(title):
  conn = pymysql.connect(host='mydb.cstof8mab94c.ap-northeast-2.rds.amazonaws.com',
                         user='admin',
                         password='123123123',
                         db='festabot',
                         charset = 'utf8')
  cur = conn.cursor()
  sql = 'select title from festival_tb where title = %s'
  cur.execute(sql, title)
  row = cur.fetchone()
  # print(row)

  try:
    for field in row:
     if(str(title) == str(field)):
      #이미 존재
      return 1
  except TypeError as e:
      #존재 x
      return 0




