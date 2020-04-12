import sys
import argparse
import requests
import pymysql
import time

API_URL = "https://kapi.kakao.com/v1/vision/thumbnail/crop"
MYAPP_KEY = '5e5acc55c8584f36abffe26633c82550'
width = "600"
height = "600"

def make_thumbnail(image_url):
    headers = {'Authorization': 'KakaoAK {}'.format(MYAPP_KEY)}

    try:
        data = { 'image_url' : image_url, 'width' : width, 'height' : height}
        resp = requests.post(API_URL, headers=headers, data=data)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(str(e))
        sys.exit(0)

host = 'mydb.cstof8mab94c.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = '123123123'
db = 'festabot'

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from common.DBconncter import DBconncter

query = 'select id, img from (select * from festival_tb where enddate > sysdate()) A'
db_obj = DBconncter().select_query(query)  # 조건이 있으면 db에 넣음

for a in db_obj:
    time.sleep(5)
    conn = pymysql.connect(host=host, user=user,
                           password=password, db=db, charset='utf8')
    curs = conn.cursor()
    thumbnail = make_thumbnail(a[1])['thumbnail_image_url']
    print(a[0])
    print('------------------------------------------------------------------------')
    sql = "UPDATE festival_tb SET thumbnail = %s WHERE id = %s"
    curs.execute(sql, (thumbnail, a[0]))
    conn.commit()
    conn.close()



