import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
from datetime import datetime as dt
import json
import requests
import pymysql
import make_db as mdb
import pandas as pd
from sqlalchemy import create_engine
import selenium.webdriver as webdriver
import overlap_db as odb
from pyvirtualdisplay import Display
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from common.common_stopwords import CommonStopwords

region_list = CommonStopwords().stop_words_region() + CommonStopwords().stop_words_region_sub()

id = []
title1 = []  #지역명존재o
title2 = []  #지역명존재x
countNum = []  #지역명존재o
countNum2 = [] #지역명존재o

# 검색할 태그명
def get_festival(festival_name, flg): #flg는 주 따봉수 인지 서브 따봉수 인지

 # 인스타그램 태그 페이지 URL
 url = 'https://www.instagram.com/explore/tags/{}'.format(festival_name)

 # 크롬창을 띄우지 않는 옵션을 넣는다
 options = webdriver.ChromeOptions()
 options.add_argument('headless')
 options.add_argument('disable-gpu')

 display = Display(visible=0, size=(1024, 768))
 display.start()
 path = '/home/ubuntu/festabot/crawler/chromedriver'
 driver = webdriver.Chrome(path)

 # 암시적으로 최대 1초간 대기
 driver.implicitly_wait(1)
 try:
  # url에 접근
  driver.get(url)

  # 게시물 개수 정보를 가져옴
  totalCount = driver.find_element_by_class_name('g47SY').text

  # ','제거
  totalCount = totalCount.replace(",", "")

  # 게시물 개수를 출력

  if flg == '0':
      print(festival_name + '의 따봉수는 ' + totalCount +'타이틀1 토탈')
      countNum.append(totalCount)
  else:
      print(festival_name + '의 따봉수는 ' + totalCount)
      countNum2.append(totalCount)
  display.stop()
 except:
  if flg == '0':
      countNum.append('0')
  else:
      countNum2.append('0')

  driver.quit()
 finally:
  # 열어둔 webdriver를 종료
  driver.quit()

def connet_festa_db():
    now = dt.now()  # 현재날짜
    start = now.strftime('%Y.%m.%d')  # 포맷변경
    #   db연결
    conn = pymysql.connect(host='mydb.cstof8mab94c.ap-northeast-2.rds.amazonaws.com',
                         user='admin',
                         password='123123123',
                         db='festabot',
                         charset='utf8')
    cur = conn.cursor()
    sql = 'SELECT id, title FROM festival_tb where startdate >= %s;'
    cur.execute(sql, start)
    row = cur.fetchall()

    for i in row:
        id.append(i[0])

        hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')  # 한글과 띄어쓰기를 제외한 모든 글자
        cleand_cont = hangul.sub('', i[1])  # 한글과 띄어쓰기를 제외한 모든 부분을 제거

        title1.append(cleand_cont) #뛰어쓰기 안하고 보여져야 하므로

        cleand_cont = re.sub(' ', '', cleand_cont)  # 띄어쓰기 제거



        print(cleand_cont)

        cleand_cont2 = cleand_cont  # 지역명 제거하기 위한 변수
        for region in region_list: #지역명제거
            cleand_cont2 = cleand_cont2.replace(region,"")
        title2.append(cleand_cont2)  # 지역명 제거한 축제리스트

        # 축제 태그수 구하는 함수호출
        get_festival(cleand_cont, 0)
        get_festival(cleand_cont2, 1)

        print(cleand_cont)
        print(cleand_cont2)

def make_db():
    data = {'id': id, 'title1': title1, 'title1_total': countNum, 'title2': title2, 'title2_total': countNum2,}
    print(data)
    mdb.insta_db(data)

def insta():
  connet_festa_db()

def start():
    insta()
    make_db()
start()