from konlpy.tag import Okt
import re
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from common.DBconncter import DBconncter
from ui.ui import Ui

class FestaList:

    def __init__(self, req):
        self.content = req['userRequest']['utterance']
        self.user = req['userRequest']['user']['id']

    def month_day(stem_list):
        where_query = ""
        word = ""
        for v in stem_list:
            v = v[0]         #분류하고 난 값
            if "월" in v:     #월만 있는 경우
                word += v + ","
                v = re.sub('[^0-9]', '', v)
                if len(v) == 1:
                    v = '0' + v     #한자릿 수 일 경우 앞에 0붙임
                query = "startdate between '2020."+v+".01' and '2020."+v+".31' or "
                where_query += query #조건 한줄 씩 추가

        query = 'select * from (select * from festival_tb where enddate > sysdate()) A where '\
                + where_query[0:len(where_query) - 3]  #현재 시간 기준으로 끝나지 않은 축제만 보여줘야 함
        db_obj = DBconncter().select_query(query)
        print("하이 하이 하이 하이 하이 하이 하이 하이 하이 하이 하이 하이 하이 하이 하이 하이 하이 하이 하이 하이 하이 하이 하이 하이 ")
        print(query)
        print(db_obj)
        return Ui().festa_list_ui(db_obj[0:5], db_obj[5:], word[0:len(word) - 1])

    def main_func(self): #형태소 겟수 세는 함수
        okt = Okt()
        stem_list = okt.pos(self.content)
        counter = 0
        for c in stem_list:
            if c[1] == 'Number':
                counter += 1
        if counter is len(stem_list):
            return FestaList.month_day(stem_list)    #숫자들 만 전송
        else:
            return False

