from naver_blog_clawer import Naver_blog_clawer
import pymysql
from datetime import datetime
import json

def get_festa_list():
    host='mydb.cstof8mab94c.ap-northeast-2.rds.amazonaws.com'
    user = 'admin'
    password = '123123123'
    db = 'festabot'
    conn = pymysql.connect(host=host, user=user,
                           password=password, db=db, charset='utf8')

    curs = conn.cursor()

    sql = 'select id, title, region, startdate  from festival_tb'
    #sql = 'select id, title, region  from festival_tb where enddate > CURDATE() and id = 606'
    curs.execute(sql)

    # 데이타 Fetch
    rows = curs.fetchall()
    conn.close()

    return rows

obj = []
for r in get_festa_list():
    val = Naver_blog_clawer().main(r[0], r[2]) #축제명, 코드를 받음
    obj.append(val)

with open('./word_freq'+datetime.today().strftime("%Y%m%d")+'.json', 'w', encoding='utf-8') as make_file:
    json.dump(obj, make_file, indent="\t")

print("hello world")
# with open('./word_freq'+datetime.today().strftime("%Y%m%d")+'.json', 'r', encoding="utf-8") as f:
#
#     json_data = json.load(f)
#
# print(json_data)
