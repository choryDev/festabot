from konlpy.tag import Okt, Mecab
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import sys
import os
from purpose_classification.word2vec.word2vec_obj import Word2vecObj
from region_ota_checker.region_checker import region_return, region_check_flg
from date_checker.date_checker import DateChecker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from common.DBconncter import DBconncter
from common.common_stopwords import CommonStopwords
from ui import ui

okt = Okt()
mecab = Mecab()
stopwords = CommonStopwords().stop_words_another()
word2vec_obj = Word2vecObj()
year = datetime.today().strftime("%Y")
month = datetime.today().strftime("%m")
date = datetime.today().strftime("%d")

path = '/home/ubuntu/festabot/festa_list/purpose_classification/word_freq_dir/'
# with open('word_freq_dir/word_freq' + str(int(datetime.today().strftime("%Y%m%d"))-1) + '.json', 'r', encoding="utf-8") as f:
with open(path + 'word_freq20200531.json', 'r', encoding="utf-8") as f:
    json_data = json.load(f)


class FindPurpose:

    def __init__(self, sentence):
        self.word = ''
        self.sentence = sentence
        self.temp_query = 'select * from (select * from festival_tb where enddate > sysdate()) A where '  #임시 쿼리

    # okt_tokenizer : 문장에서 색인어 추출을 위해 명사,수사, ,숫자 정도의 단어만 뽑아서 normalization, stemming 처리하도록 함
    def okt_tokenizer(raw, token_tag=["Noun", "Determiner", "Number", ]):
        return [(w, t) for w, t in okt.pos(raw, norm=True, stem=True) if t in token_tag and w not in stopwords]

    def tag_number(self, word):
        mon_qu = ""
        if word[len(word) - 1] == '월':  # 월 인지 체크
            word = word[0:len(word) - 1]  # 끝에 월 또는 일 제거
            if len(word) == 1:  word = '0' + word  # 한자릿 수 일 경우 앞에 0붙임 두자릿수면 그냥 한다 ex) 11, 12
            mon_qu = "startdate between '" + year + "." + word + ".01' and '" + year + "." + word + ".31' or "

        if word[len(word) - 1] == '일':  # 몇일 뒤 체크
            date = word[0:len(word) - 1]  # 일 제거
            time_now = datetime.now()  # 현재 날짜
            st_time = time_now + timedelta(days=int(date))  # 현재 날짜에서 더함
            ed_time = st_time + timedelta(days=int(30))  # 현재 날짜에서 30일 더함
            st_time = st_time.strftime("%Y.%m.%d")
            ed_time = ed_time.strftime("%Y.%m.%d")
            mon_qu = "startdate between '" + st_time + "' and '" + ed_time + "' or"
        return mon_qu

    def tag_Determiner(self, word):
        g_month = DateChecker.de_month_generater(word)
        int_year = int(year)
        int_month = int(month)
        st_month = (datetime(int_year, int_month, 1) + relativedelta(months=g_month)).strftime(
            "%Y.%m.%d")
        ed_month = (datetime(int_year, int_month, 30) + relativedelta(months=g_month)).strftime(
            "%Y.%m.%d")
        mon_qu = "startdate between '" + st_month + "' and '" + ed_month + "' or "
        return mon_qu

    def func_list(self):
        date_query = ""
        purpose_query = ""
        region_list = ""
        title = ""
        query_cheker = False
        token_idx = 0
        pupose_words = []
        query = 'select * from (select * from festival_tb where enddate > sysdate()) A where '  # 기본 쿼리
        token = FindPurpose.okt_tokenizer(self.sentence)
        if len(token) != 0:  # 토큰화하여 처리할 문장이 있다

            while token_idx < len(token):
                word, tag = token[token_idx][0], token[token_idx][1]

                if tag == 'Number':
                    title += word + ','  # 보여질 제목에 들어갈 문장
                    date_query += FindPurpose.tag_number(self, word)  # 조건 한줄 씩 추가

                if tag == 'Determiner' or tag == 'Modifier':
                    if DateChecker.de_month_check(word):  # 월 인지 체크
                        title += word + '달 뒤,'
                        date_query += FindPurpose.tag_Determiner(self, word)  # 조건 한줄 씩 추가

                if tag == 'Noun':
                    if DateChecker.month_check(word):  # 월 인지 체크
                        title += word + ','
                        word = DateChecker.month_generater(word)
                        if len(word) == 1:  word = '0' + word  # 한자릿 수 일 경우 앞에 0붙임 두자릿수면 그냥 한다 ex) 11, 12
                        mon_qu = "startdate between '" + year + "." + word + ".01' and '" + year + "." + word + ".31' or "
                        print(mon_qu)
                        date_query += mon_qu  # 조건 한줄 씩 추가

                    elif word in ['이번', '다음주', '다음', '다다', '주말', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일'
                            , '월', '화', '수', '목', '금', '토', '일']: #향후 있을 날짜 처리 ex) 이번 달, 다음 주 일요일
                        #이번, 다음, 다다음, 토큰화 방식이 너무 다름
                        if word == '이번':
                            if token[token_idx+1][0] == '주':    #주말을 물어 봤을 경우
                                if token[token_idx+2][0] in ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일'
                                                             , '월', '화', '수', '목', '금', '토', '일']:
                                    day_of_the_week = 0
                                    for a in [('월요일', 0), ('화요일', 1), ('수요일', 2), ('목요일', 3), ('금요일', 4), ('토요일', 5), ('일요일', 6),
                                              ('월', 0), ('화', 1), ('수', 2), ('목', 3), ('금', 4), ('토', 5), ('일', 6),]:
                                        if token[token_idx+2][0] == a[0]: #무슨 요일인지 찾음
                                            day_of_the_week = a[1]

                                    today = datetime.today()
                                    day = today + timedelta(days=-today.weekday() + day_of_the_week, weeks = 0)  # 월요일
                                    mon_qu = "(startdate < '"+day.strftime("%Y.%m.%d")+"' and enddate > '"+day.strftime("%Y.%m.%d")+"') or"
                                    title += word + token[token_idx + 1][0] + ','+ token[token_idx + 2][0] + ','
                                    del token[token_idx + 1];  # 이번, "주" 제거
                                    del token[token_idx + 1];  # 이번, "주", '요일' 제거
                                    date_query += mon_qu  # 조건 한줄 씩 추가

                                else:   #주간으로 물어 봤을 경우
                                    today = datetime.today()
                                    mon_day = today + timedelta(days=-today.weekday(), weeks = 0) #월요일
                                    sun_day = today + timedelta(days=-today.weekday()+6, weeks = 0) #일요일
                                    mon_qu = "startdate between '" +mon_day.strftime("%Y.%m.%d")+\
                                                            "' and '"+sun_day.strftime("%Y.%m.%d")+"' or "
                                    title += word + token[token_idx + 1][0] + ','
                                    del token[token_idx + 1]; #이번, "주" 제거
                                    date_query += mon_qu  # 조건 한줄 씩 추가

                            elif token[token_idx+1][0] == '달' or token[token_idx+1][0] == '월':  #달, 월 로 쳤을 경우
                                st_month = (datetime(int(year), int(month), 1) + relativedelta(months = 0)).strftime(
                                    "%Y.%m.%d")
                                ed_month = (datetime(int(year), int(month), 30) + relativedelta(months= 0)).strftime(
                                    "%Y.%m.%d")
                                title += word + token[token_idx + 1][0] + ','
                                del token[token_idx + 1];  # 이번, "달" 제거
                                mon_qu = "startdate between '" + st_month + "' and '" + ed_month + "' or "
                                date_query += mon_qu  # 조건 한줄 씩 추가

                        elif word == '다음주':
                            try:
                                if token[token_idx+1][0] in ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일'
                                                             , '월', '화', '수', '목', '금', '토', '일']:
                                    day_of_the_week = 0
                                    for a in [('월요일', 0), ('화요일', 1), ('수요일', 2), ('목요일', 3), ('금요일', 4), ('토요일', 5), ('일요일', 6),
                                              ('월', 0), ('화', 1), ('수', 2), ('목', 3), ('금', 4), ('토', 5), ('일', 6),]:
                                        if token[token_idx+1][0] == a[0]: #무슨 요일인지 찾음
                                            day_of_the_week = a[1]

                                    today = datetime.today()
                                    day = today + timedelta(days=-today.weekday() + day_of_the_week, weeks = 1)  # 월요일
                                    mon_qu = "(startdate < '"+day.strftime("%Y.%m.%d")+"' and enddate > '"+day.strftime("%Y.%m.%d")+"') or"
                                    title += word + token[token_idx + 1][0] + ','
                                    del token[token_idx + 1];  # 다음주, "요일" 제거
                                    date_query += mon_qu  # 조건 한줄 씩 추가
                                else:
                                    today = datetime.today()
                                    mon_day = today + timedelta(days=-today.weekday(), weeks=1)  # 월요일
                                    sun_day = today + timedelta(days=-today.weekday() + 6, weeks=1)  # 일요일
                                    mon_qu = "startdate between '" + mon_day.strftime("%Y.%m.%d") + \
                                             "' and '" + sun_day.strftime("%Y.%m.%d") + "' or "
                                    title += word + ','
                                    date_query += mon_qu  # 조건 한줄 씩 추가
                            except IndexError:
                                today = datetime.today()
                                mon_day = today + timedelta(days=-today.weekday(), weeks=1)  # 월요일
                                sun_day = today + timedelta(days=-today.weekday() + 6, weeks=1)  # 일요일
                                mon_qu = "startdate between '" + mon_day.strftime("%Y.%m.%d") + \
                                         "' and '" + sun_day.strftime("%Y.%m.%d") + "' or "
                                title += word + ','
                                date_query += mon_qu  # 조건 한줄 씩 추가

                        elif word == '다음':
                            if token[token_idx+1][0] == '달':    #주말을 물어 봤을 경우
                                st_month = (datetime(int(year), int(month), 1) + relativedelta(months=1)).strftime("%Y.%m.%d")
                                ed_month = (datetime(int(year), int(month), 30) + relativedelta(months=1)).strftime("%Y.%m.%d")
                                title += word + token[token_idx + 1][0] + ','
                                del token[token_idx + 1];  # 다음, "" 제거달
                                mon_qu = "(startdate < '" + st_month + "' and enddate > '" + ed_month + "') or"
                                date_query += mon_qu  # 조건 한줄 씩 추가

                        elif word == '다다':
                            if token[token_idx+1][0] == '음주':    #다다음주 물어 봤을 경우
                                today = datetime.today()
                                mon_day = today + timedelta(days=-today.weekday(), weeks=2)  # 월요일
                                sun_day = today + timedelta(days=-today.weekday() + 6, weeks=2)  # 일요일
                                mon_qu = "startdate between '" + mon_day.strftime("%Y.%m.%d") + \
                                         "' and '" + sun_day.strftime("%Y.%m.%d") + "' or "
                                title += word + token[token_idx + 1][0] + ','
                                date_query += mon_qu  # 조건 한줄 씩 추가
                            if token[token_idx+1][0] == '음달':    #다다음주 물어 봤을 경우
                                st_month = (datetime(int(year), int(month), 1) + relativedelta(months=2)).strftime("%Y.%m.%d")
                                ed_month = (datetime(int(year), int(month), 30) + relativedelta(months=2)).strftime("%Y.%m.%d")
                                title += word + token[token_idx + 1][0] + ','
                                del token[token_idx + 1];  # 다음, "" 제거달
                                mon_qu = "(startdate < '" + st_month + "' and enddate > '" + ed_month + "') or"
                                date_query += mon_qu  # 조건 한줄 씩 추가

                        if word in ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일'
                            , '월', '화', '수', '목', '금', '토', '일']:
                            day_of_the_week = 0
                            for a in [('월요일', 0), ('화요일', 1), ('수요일', 2), ('목요일', 3), ('금요일', 4), ('토요일', 5),
                                      ('일요일', 6),
                                      ('월', 0), ('화', 1), ('수', 2), ('목', 3), ('금', 4), ('토', 5), ('일', 6), ]:
                                if word == a[0]:  # 무슨 요일인지 찾음
                                    day_of_the_week = a[1]

                            today = datetime.today()
                            day = today + timedelta(days=-today.weekday() + day_of_the_week, weeks=0)  # 월요일
                            mon_qu = "(startdate < '" + day.strftime("%Y.%m.%d") + "' and enddate > '" + day.strftime(
                                "%Y.%m.%d") + "') or"
                            title += word + ','
                            date_query += mon_qu  # 조건 한줄 씩 추가

                    elif region_check_flg(word):  # 지역인지 체크 오타 체크 부분
                        region = region_return(word)
                        title += region + ','
                        region_list += "'" + region + "',"
                    else:
                        title += word + ','
                        pupose_words.append(word)   #목적이 있는 단어를 하나씩 추가
                        id_list = FindPurpose.word_pupose(self, word)   #목적 단어 pk 추가
                        if len(id_list) != 0:
                            for festa_id in id_list:
                                purpose_query += "id = " + str(festa_id) + " or "
                            query_cheker = True
                token_idx += 1 #다음 인덱스

            if date_query != "":
                query += "(" + date_query[0:len(date_query) - 3] + ") and"  # where절에 마지막 or를 날린다  #날짜를 쿼리에 넣음
                self.temp_query += "(" + date_query[0:len(date_query) - 3] + ") and"  #임시 쿼
                query_cheker = True
            if region_list != "":
                query += " region in (" + region_list[:len(region_list) - 1] + ") and"  # 조건 한줄 추가 #where region in ('부산','서울')
                self.temp_query += " region in (" + region_list[:len(region_list) - 1] + ") and"  #임시 쿼리
                query_cheker = True
            if purpose_query != "":
                query += "(" + purpose_query[0:len(purpose_query) - 3] + ") and"  # where절에 마지막 or를 날린다  #날짜를 쿼리에 넣음
                query_cheker = True

            if query_cheker:  # 조건이 들어가는 쿼리가 있음
                query = query[0:len(query) - 3]
                print(query)
                db_obj = DBconncter().select_query(query)  # 조건이 있으면 db에 넣음
                if len(db_obj) == 0:  # word2vec으로 축제들을 가져왔지만 축제가 있는지 없는지
                    return self.word2vec_checker(pupose_words, title)
                else:
                    return ui.festa_list_ui(db_obj[0:5], db_obj[5:], title[0:len(title) - 1])
            else:
                return self.word2vec_checker(pupose_words, title)

        elif len(token) == 0:  # 사용자의 말에 축제 조건이 없음
            return ui.text_message("어떤 축제를 원하는지 다시 말해줄래?\n"
                                   "(ex : 지역, 월, 목적)")

    def word_pupose(self, word):
        festa_list = []
        for r in json_data:
            for v in r['freq_words']:  # 단어 들어가는 지만 체크
                if v['word'] == word:
                    festa_list.append(r['id'])
        return festa_list

    def word2vec_checker(self, pupose_words, title):
        sim_obj_list = []
        for word in pupose_words:
            print(word)
            for sim_word in word2vec_obj.most_similar(word, 5): #연관된 단어 5개 추출
                print(sim_word)
                id_query = ''
                sim_word_list = self.word_pupose(sim_word) #해당 단어를 가진 축제 있는지 체크
                if len(sim_word_list) !=0:
                    for id in sim_word_list:
                        id_query += "id = " + str(id) + " or "
                    if id_query != '':
                        exe_temp_query = self.temp_query + " (" + id_query[0:len(id_query) - 3] + ")"
                        db_obj = DBconncter().select_query(exe_temp_query)
                        print(len(db_obj))
                        if len(db_obj) !=0:
                            obj ={'word':sim_word, 'festa_list': db_obj}
                            sim_obj_list.append(obj)
        if len(sim_obj_list) == 0:
            return ui.text_message(title + "에 맞는 열릴 축제가 없나봐 ㅠ.ㅠ")
        else:
            return ui.word2vec_recommed_ui(pupose_words, sim_obj_list)

    def main(self):
        return FindPurpose.func_list(self)
