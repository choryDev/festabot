from konlpy.tag import Okt
import re
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from common.DBconncter import DBconncter
from ui.ui import Ui
from datetime import datetime
from region_ota_checker.region_checker import region_translater, region_check_flg
from date_checker.date_checker import DateChecker
year = datetime.today().strftime("%Y")
month = datetime.today().strftime("%m")

class FestaList:

    def __init__(self, req):
        self.content = req['userRequest']['utterance']
        self.user = req['userRequest']['user']['id']

    def easy_list(stem_list):
        month_query = ""
        region_check = 0
        region_list = ""
        word = ""
        query = 'select * from (select * from festival_tb where enddate > sysdate()) A where ' #기본 쿼리
        for v in stem_list:
            if v[1] == 'Number' and v[0][len(v[0])-1] == '월':    #숫자를 나타내는 ex) 1월 1일
                word += v[0]+','
                v = v[0][0:len(v[0])-1]
                if len(v) == 1:  #한자릿 수 일 경우 앞에 0붙임 두자릿수면 그냥 한다 ex) 11, 12
                    v = '0' + v
                mon_qu = "startdate between '"+year+"."+ v +".01' and '"+year+"."+ v +".31' or "
                month_query += mon_qu #조건 한줄 씩 추가

            if v[1] == 'Noun':
                if DateChecker.month_check(v[0]):   #월 인지 체크
                    month = DateChecker.month_generater(v[0])
                    mon_qu = "startdate between '" + year + "." + month + ".01' and '" + year + "." + month + ".31' or "
                    month_query += mon_qu  # 조건 한줄 씩 추가
                else:
                    v = region_translater(v[0])     #지역인지 체크
                    word += v+','
                    region_check += 1
                    region_list += "'"+v+"',"

        if month_query != "" : query += "("+month_query[0:len(month_query) - 3]+")" #where절에 마지막 and를 날린다  #날짜를 쿼리에 넣음

        if region_check != 0:
            if month_query != "": query += "and region in ("+region_list[0:len(region_list)-1]+")"   #조건 한줄 추가 #and region in ('부산','서울')
            else: query += " region in ("+region_list[0:len(region_list)-1]+")"   #조건 한줄 추가 #where region in ('부산','서울')

        print(query)
        db_obj = DBconncter().select_query(query)
        print(db_obj)
        print(len(db_obj))
        if len(db_obj) == 0:    # 찾았는데 없을 경우 길이가 0 개
            return Ui().none_festa_list_ui(word[0:len(word) - 1])
        else:
            return Ui().festa_list_ui(db_obj[0:5], db_obj[5:], word[0:len(word) - 1])

    def main_func(self): #형태소 겟수 세는 함수
        okt = Okt()
        counter = 0
        stem_list = okt.pos(self.content)
        for v in stem_list:
            if v[1] == 'Number' or region_check_flg(v[0]):
                counter +=1
        if counter == len(stem_list):
            return FestaList.easy_list(stem_list)