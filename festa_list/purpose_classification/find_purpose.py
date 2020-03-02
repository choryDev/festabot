from konlpy.tag import Okt
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import sys
import os
from purpose_classification.word2vec.word2vec_obj import Word2vecObj
from region_ota_checker.region_checker import region_translater, region_check_flg
from date_checker.date_checker import DateChecker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from common.DBconncter import DBconncter
from common.common_stopwords import CommonStopwords
from ui.ui import Ui

okt = Okt()
ui = Ui()
stopword = CommonStopwords()
word2vec_obj = Word2vecObj()
year = datetime.today().strftime("%Y")
month = datetime.today().strftime("%m")
date = datetime.today().strftime("%d")

path = '/home/ubuntu/festabot/festa_list/purpose_classification/word_freq_dir/'
with open(path + 'word_freq20200220.json', 'r', encoding="utf-8") as f:
    json_data = json.load(f)

class FindPurpose:

    def __init__(self, sentence):
        self.word = ''
        # with open('word_freq_dir/word_freq' + str(int(datetime.today().strftime("%Y%m%d"))-1) + '.json', 'r', encoding="utf-8") as f:
        self.sentence = sentence

    # tokenizer : 문장에서 색인어 추출을 위해 명사,수사, ,숫자 정도의 단어만 뽑아서 normalization, stemming 처리하도록 함
    def tokenizer(raw, pos=["Noun", "Determiner", "Number", ]):
        obj = okt.pos(
            raw,
            norm=True,  # normalize 그랰ㅋㅋ -> 그래ㅋㅋ
            stem=True,  # stemming 바뀌나->바뀌다
        )
        list = []
        for word, tag in obj:
            if tag in pos and word not in stopword.stop_words_another(): #형태소 태그, 불용어 처리
                list.append((word, tag))
        return list

    def main(self):
        date_query = ""
        purpose_query = ""
        region_list = ""
        title = ""
        query = 'select * from (select * from festival_tb where enddate > sysdate()) A where '  # 기본 쿼리
        token = FindPurpose.tokenizer(self.sentence)
        if len(token) != 0 :
            for word, tag in token:
                if tag == 'Number':
                    title += word + ','     #보여질 제목에 들어갈 문장
                    if word[len(word)-1] == '월':    #월 인지 체크
                        word = word[0:len(word) - 1]  # 끝에 월 또는 일 제거
                        if len(word) == 1:  word = '0' + word  # 한자릿 수 일 경우 앞에 0붙임 두자릿수면 그냥 한다 ex) 11, 12
                        mon_qu = "startdate between '" + year + "." + word + ".01' and '" + year + "." + word + ".31' or "
                        date_query += mon_qu  # 조건 한줄 씩 추가
                    if word[len(word)-1] == '일':    #몇일 뒤 체크
                        date = word[0:len(word) - 1]  # 일 제거
                        time_now = datetime.now()   #현재 날짜
                        st_time = time_now + timedelta(days=int(date))  #현재 날짜에서 더함
                        ed_time = st_time + timedelta(days=int(30))  # 현재 날짜에서 30일 더함
                        st_time = st_time.strftime("%Y.%m.%d")
                        ed_time = ed_time.strftime("%Y.%m.%d")
                        mon_qu = "startdate between '"+st_time+"' and '"+ed_time+"' or"
                        date_query += mon_qu  # 조건 한줄 씩 추가

                if tag == 'Determiner' or tag == 'Modifier':
                    if DateChecker.de_month_check(word):   #월 인지 체크
                        title += word+'달 뒤,'
                        g_month = DateChecker.de_month_generater(word)
                        int_year = int(year)
                        int_month = int(month)
                        st_month = (datetime(int_year, int_month, 1) + relativedelta(months=g_month)).strftime("%Y.%m.%d")
                        ed_month = (datetime(int_year, int_month, 30) + relativedelta(months=g_month)).strftime("%Y.%m.%d")
                        mon_qu = "startdate between '"+st_month+"' and '"+ed_month+"' or "
                        date_query += mon_qu  # 조건 한줄 씩 추가

                if tag == 'Noun':
                    if DateChecker.month_check(word):   #월 인지 체크
                        title += word+','
                        g_month = int(DateChecker.month_generater(word[0:len(word)-1]))
                        int_year = int(year)
                        int_month = int(month)
                        st_month = (datetime(int_year, int_month, 1) + relativedelta(months=g_month)).strftime("%Y.%m.%d")
                        ed_month = (datetime(int_year, int_month, 30) + relativedelta(months=g_month)).strftime("%Y.%m.%d")
                        mon_qu = "startdate between '"+st_month+"' and '"+ed_month+"' or "
                        date_query += mon_qu  # 조건 한줄 씩 추가
                    elif region_check_flg(word): #지역인지 체크
                        region = region_translater(word)
                        title += region+','
                        region_list += "'"+region+"',"
                    else:
                        id_list = FindPurpose.word_pupose(self, word)
                        if len(id_list) !=0 :
                            for festa_id in id_list:
                                purpose_query += "id = " + str(festa_id) + " or "

            if date_query != "" :
                query += "("+date_query[0:len(date_query) - 3]+") and" #where절에 마지막 or를 날린다  #날짜를 쿼리에 넣음
            if region_list != "":
                query += " region in (" + region_list[0:len(region_list) - 1] + ") and"  # 조건 한줄 추가 #where region in ('부산','서울')
            if purpose_query != "":
                query += "("+purpose_query[0:len(purpose_query) - 3]+") and" #where절에 마지막 or를 날린다  #날짜를 쿼리에 넣음

            if len(query) != 76:
                query = query[0:len(query)-3]

        db_obj = DBconncter().select_query(query)
        if len(db_obj) == 0 or len(query) == 76:
            print(word)
            for v in word2vec_obj.most_similar(word, 10):
                print(v)
        # if len(db_obj) == 0:
        #     id_list = []
        #     print(word+'필요한 단어')
        #     for v in word2vec_obj.most_similar(word, 10):
        #         print(v+'연관된 단어 들 word2vec')
        #         print(FindPurpose.word_pupose(self, v))
        #         id_list += FindPurpose.word_pupose(self, v)
        #     print(id_list)

    def word_pupose(self, word):
        festa_list = []
        for r in json_data:
            for v in r['freq_words']:    #단어 들어가는 지만 체크
                if v['word'] == word:
                    festa_list.append(r['id'])
        return festa_list
    # def location_condition_search(self, word): #단어만 온 경우
    #     self.word = word
    #     festa_list = []
    #     for r in self.json_data:
    #         if r['region'] in '대전':
    #             for v in r['freq_words']:
    #                 if v['word'] == word:
    #                     festa_list.append(r['id'])
    #     return festa_list
    #
    # def db_query_list (self, festa_list):
    #     condition_query = ''  # where 절 쿼리 만듬
    #     get_festa_list = festa_list[0:5]
    #     for v in get_festa_list:
    #         condition_query += ' id = ' + str(v) + ' or'
    #     where_query = condition_query[0:len(condition_query) - 3]
    #     query = 'select * from festival_tb where' + where_query
    #     db_obj = DBconncter().select_query(query)
    #     return ui.festa_list_ui(db_obj, festa_list[5:], self.word)
    #
    # def none_condition_search(self, word):     #단어로 만 뽑고 조건이 없는 경우
    #     self.word = word
    #     festa_list = []
    #     for r in self.json_data:
    #         for v in r['freq_words']:    #단어 들어가는 지만 체크
    #             if v['word'] == word:
    #                 festa_list.append(r['id'])
    #
    #     if len(festa_list) == 0:         #json파일에 맞는게 없는 경우
    #         dataSend = {
    #             "version": "2.0",
    #             "template": {
    #                 "outputs": [
    #                     {
    #                         "simpleText": {
    #                             "text": str(self.word2vec_obj.most_similar(self.word, 5))
    #                         }
    #                     }
    #                 ]
    #             }
    #         }
    #         return dataSend
    #     else:
    #         return Find_purpose.db_query_list(self, festa_list)
    #
    # def month_condition_search(self, word):
    #     self.word = word
    #     festa_list = []
    #     for r in self.json_data:
    #         if r['startdate'] in '01':
    #             for v in r['freq_words']:
    #                 if v['word'] == word:
    #                     festa_list.append(r['id'])
    #     return festa_list
    #
    #
    #
    # def find_purpose_first(self, word): #첫번째 단계
    #     return Find_purpose.none_condition_search(self, word)

    # def word2vec_similar_word(self):
