#!/usr/lib/python3.5/

import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
from datetime import datetime as dt
import json
import requests
import pymysql
import overlap_db as odb
import make_db as mdb
import pandas as pd

url_list = []  # 상세페이지 url
srcpath_text = []  # 사진
region_text = []  # 지역명
title_text = []  # 축제명 배열
link_text = []  # 링크주소 배열
address_text = []  # 주소 배열
place_text = []  # 장소 배열
host_text = []  # 주최/주관 배열
content_text = []  # 행사내용 배열
start_date = []  # 시작 날짜 담을 배열
end_date = []  # 종료 날짜 담을 배열
fee = []  # 요금
tel_text = []  # 연락처
getX = []  # 위도배열
getY = []  # 경도배열

def new_data(region, code):
    count = 0
    page = 1
    now = dt.now()
    url = 'http://www.gov.kr/portal/vfnews?srchSttusCls=FOR&srchAddrCd={}'.format(code) + '&srchStdt=20130101' + \
          '&srchEddt=' + str(int(now.strftime('%Y%m%d')) + 10000) + '&srchTxt=&pageIndex=' + str(page)
    # url = 'http://www.gov.kr/portal/vfnews?srchSttusCls=FOR&srchAddrCd={}'.format(code)+'&srchStdt=' +\
    #       now.strftime('%Y%m%d') + '&srchEddt=' + str(int(now.strftime('%Y%m%d'))+10000)+'&srchTxt=&pageIndex='+str(page)
    resp = requests.get(url)  # request 객체로 만듦
    html_doc = resp.text
    soup = BeautifulSoup(html_doc, 'html.parser')  # 뷰티풀소프 인자값 지정

    #전체 페이지 구하기
    allpage = soup.find('span', class_='sum').text
    if(int(allpage)%6 == 0):
        maxpage = int(allpage)//6
    else:
        maxpage = int(allpage)//6+1

    while page <= maxpage:
       url2 = 'http://www.gov.kr/portal/vfnews?srchSttusCls=FOR&srchAddrCd={}'.format(code) + '&srchStdt=20130101' + \
              '&srchEddt=' + str(int(now.strftime('%Y%m%d')) + 10000) + '&srchTxt=&pageIndex=' + str(page)
       # url2 = 'http://www.gov.kr/portal/vfnews?srchSttusCls=FOR&srchAddrCd={}'.format(code)+'&srchStdt=' +\
       #    now.strftime('%Y%m%d') + '&srchEddt=' + str(int(now.strftime('%Y%m%d'))+10000)+'&srchTxt=&pageIndex='+str(page)
       resp2 = requests.get(url2)  # request 객체로 만듦
       html_doc = resp2.text
       soup = BeautifulSoup(html_doc, 'html.parser')
       divtag = soup.find('div', class_='gallery_wrap k-festival')
       dttags = divtag.find_all('dt')
       for dttag in dttags:
       #제목 가져오기
         title = dttag.find('a').text
         title = re.sub(r'\[[^)]*\]', '', title)

       #url 가져오기
         base_url = 'http://www.gov.kr/'
         url_text = urljoin(base_url, dttag.find("a")["href"])
       #기존 데이터와 비교
         v = odb.title_overlap(title)
         if(v==1):
             #중복값존재o
             pass
         elif(v==0):
             #중복값존재x
             # print("출력")
             detail_page(url_text)
             link_text.append(url_text)
             count += 1
       page += 1
    #지역 넣기
    for i in range(0, count):
        region_text.append(region)




def detail_page(url):
    page_resp = requests.get(url)  # 상세페이지를 resquest객체로 만듦
    page_html = page_resp.text  # html
    detail_soup = BeautifulSoup(page_html, 'html.parser')  # beautifulsoup 객체
    content = detail_soup.find(class_='contents')  # contents 클래스 찾기
    cleand_title = detail_soup.find(class_="no-bullet").text
    cleand_title = re.sub(r'\[[^)]*\]', '', cleand_title)
    title_text.append(cleand_title)  # 타이틀
    content = detail_soup.find('dl', class_="board-view-detail")

    # 날짜
    con_data = content.find_all('dd')
    dt_data = content.find_all('dt')

    date = con_data[0].get_text()  # 날짜 얻기
    date = re.sub('&nbsp;|\t|\r|\n', '', date).strip()
    cleaning_date(date)  # 날짜 가공 함수 실행

    # 장소
    if (dt_data[1].get_text() == '주최/주관'):
        tel_text.append('null')
        host = con_data[1].get_text()
        host_text.append(re.sub('&nbsp;|\t|\r|\n', '', host).strip())
    elif (dt_data[1].get_text() == '연락처'):
        tel = con_data[1].get_text()
        cleaning_tel = re.sub('&nbsp;|\t|\r|\n|[ㄱ-ㅣ가-힣]|[a-zA-Z]', '', tel).strip()
        tel_text.append(re.sub('[-\(),:&/]', '', cleaning_tel))
    else:
        place = con_data[1].get_text()
        place_text.append(re.sub('&nbsp;|\t|\r|\n', '', place).strip())

    # 연락처
    if (dt_data[2].get_text() == '주소'):
        pass
    elif (dt_data[2].get_text() == '주최/주관'):
        host = con_data[2].get_text()
        host_text.append(re.sub('&nbsp;|\t|\r|\n', '', host).strip())
    else:
        tel = con_data[2].get_text()
        cleaning_tel = re.sub('&nbsp;|\t|\r|\n|[ㄱ-ㅣ가-힣]|[a-zA-Z]', '', tel).strip()
        tel_text.append(re.sub('[-\(),:&/]', '', cleaning_tel))

    # 주최/주관
    try:
        host = con_data[3].get_text()
        if (dt_data[3].get_text() == '주최/주관'):
            host_text.append(re.sub('|\t|\r|\n', '', host).strip())
        elif (dt_data[1].get_text() == '장소' and dt_data[2].get_text() == '주최/주관'):
            tel_text.append('null')
        elif (dt_data[1].get_text() == '연락처' and dt_data[2].get_text() == '주소'):
            host_text.append('null')
            place_text.append('null')
        elif (dt_data[1].get_text() == '장소' and dt_data[2].get_text() == '연락처'):
            host_text.append('null')
        elif (dt_data[1].get_text() == '연락처' and dt_data[2].get_text() == '주최/주관'):
            place_text.append('null')
        else:
            pass

    except IndexError:
        place_text.append('null')

    try:
        # 주소 & 위도 경도
        all_xy = detail_soup.find('span', class_='ibtn small sky').find('button')
        cleand_text = re.sub('[<>"=()\;/\']', '', str(all_xy))
        cleand_text = cleand_text.replace('새창열림찾아오시는 길', '')
        cleand_text = cleand_text.replace('button onclickfncSearchLoad', '')
        cleand_text = cleand_text.replace('return false titlebutton', '')
        locate = re.split(',', cleand_text)

        address_text.append(locate[0])  # 주소
        try:
            float(locate[1])
            float(locate[2])
            getX.append(locate[2])  # 경도
            getY.append(locate[1])  # 위도
        except ValueError:
            try:
                getX.append(locate[3])  # 경도
                getY.append(locate[2])  # 위도
            except IndexError:
                getX.append("null")
                getY.append("null")
    except AttributeError:
        address_text.append("null")
        getX.append("null")
        getY.append("null")

    # 행사소개
    try:
        content = detail_soup.find('div', class_='box-cont').text
        cleand_cont = re.sub('\n|\'', '', content)
        cleand_cont = cleand_cont.replace('행사내용', '')
        cleand_cont = cleand_cont.replace('행사소개', '')
        cleand_cont = cleand_cont.replace('줄거리', '')
        cleand_cont = cleand_cont.replace('참가안내', '')
        cleand_cont = cleand_cont.replace('약력', '')
        cleand_cont = cleand_cont.replace('출     연', '')
        content_text.append(cleand_cont)
    except AttributeError as e:
        content_text.append('null')

    #사진
    srcpath = detail_soup.find('p', class_='thumb-img').find('img')
    m = re.search(
        'http:(.*?).jpg|http:(.*?).JPG|http:(.*?).png|http:(.*?).PNG|http:(.*?).jpeg|http:(.*?).JPEG|http:(.*?).GIF|http:(.*?).gif|http:(.*?).BMP|http:(.*?).bmp|http:(.*?).TIFF|http:(.*?).tiff|http:(.*?).RAW|http:(.*?).raw',
        str(srcpath))
    srcpath_text.append(m.group())


# 주최/주관
def cleaning_host(host):
    if (host == '주최/주관'):
        host_text.append(re.sub('|\t|\r|\n', '', host).strip())
    else:
        pass

# 날짜 정제화 함수
def cleaning_date(date):
    date_array = re.split(' ~ ', date)  # 정규표현식 사용하여 date를 날짜 리스트로 돌려줌
    start_date.append(date_array[0])  # 시작날짜
    end_date.append(date_array[1])  # 종료날짜


def make_db():
    data = {'region': region_text, 'title': title_text, 'host': host_text, 'tel': tel_text, 'link': link_text,
            'startdate': start_date, 'enddate': end_date, 'place': place_text, 'address': address_text,
            'content': content_text, 'img': srcpath_text, 'getX': getX, 'getY': getY}
    columns = ['id', 'region', 'title', 'host', 'tel', 'link', 'startdate', 'enddate', 'place', 'address', 'content',
               'img', 'getX', 'getY']
    # df = pd.DataFrame(data, columns)
    print(data)
    mdb.make_db(data)


    print(title_text)
    print(content_text)
    print(address_text)
    print(getX)
    print(getY)
    print(host_text)
    print(tel_text)
    print(start_date)
    print(srcpath_text)
    print(region_text)

    # print(len(content_text))
    # print(len(getX))
    # print(len(getY))
    # print(len(host_text))
    # print(len(tel_text))
    # print(len(start_date))
    # print(len(region_text))
    # print(len(end_date))
    # print(len(link_text))
    # print(len(title_text))
    # print(len(address_text))
    # print(len(srcpath_text))


region_name = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원',
               '충북', '충남', '전북', '전남', '경북', '경남', '제주']
area_text = ['1100000000', '2600000000', '2700000000', '2800000000', '2900000000', '3000000000',
             '3100000000', '3600000000', '4100000000', '4200000000', '4300000000', '4400000000',
             '4500000000', '4600000000', '4700000000', '4800000000', '5000000000']

def start():
 new_data(region_name[0], area_text[0])
 make_db()
# new_data(region_name[0], area_text[0])

start()
