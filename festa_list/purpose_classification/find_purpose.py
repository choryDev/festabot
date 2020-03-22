from konlpy.tag import Okt, Mecab
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
from ui import ui

okt = Okt()
mecab = Mecab()
stopword = CommonStopwords()
word2vec_obj = Word2vecObj()
year = datetime.today().strftime("%Y")
month = datetime.today().strftime("%m")
date = datetime.today().strftime("%d")

path = '/home/ubuntu/festabot/festa_list/purpose_classification/word_freq_dir/'
# with open('word_freq_dir/word_freq' + str(int(datetime.today().strftime("%Y%m%d"))-1) + '.json', 'r', encoding="utf-8") as f:
with open(path + 'word_freq20200317.json', 'r', encoding="utf-8") as f:
    json_data = json.load(f)


class FindPurpose:

    def __init__(self, sentence):
        self.word = ''
        self.sentence = sentence

    # okt_tokenizer : 문장에서 색인어 추출을 위해 명사,수사, ,숫자 정도의 단어만 뽑아서 normalization, stemming 처리하도록 함
    def okt_tokenizer(raw, pos=["Noun", "Determiner", "Number", ]):
        obj = okt.pos(
            raw,
            norm=True,  # normalize 그랰ㅋㅋ -> 그래ㅋㅋ
            stem=True,  # stemming 바뀌나->바뀌다
        )
        list = []
        for word, tag in obj:
            if tag in pos and word not in stopword.stop_words_another():  # 형태소 태그, 불용어 처리
                list.append((word, tag))
        return list

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

    def tagnone_date(self, word):

         return


    def func_list(self, db_lencheck):  # db_lencheck 갯수 0개일때 다시 돌아옴
        date_query = ""
        purpose_query = ""
        region_list = ""
        title = ""
        query_cheker = False
        token_idx = 0
        query = 'select * from (select * from festival_tb where enddate > sysdate()) A where '  # 기본 쿼리
        #query = 'select * from festival_tb where'  # 기본 쿼리
        token = FindPurpose.okt_tokenizer(self.sentence)
        if len(token) != 0:  # 토큰화하여 처리할 문장이 있다
            print(str(token) + '////처음')

            for word, tag in token:

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
                        print(word)
                        if len(word) == 1:  word = '0' + word  # 한자릿 수 일 경우 앞에 0붙임 두자릿수면 그냥 한다 ex) 11, 12
                        mon_qu = "startdate between '" + year + "." + word + ".01' and '" + year + "." + word + ".31' or "
                        print(mon_qu)
                        date_query += mon_qu  # 조건 한줄 씩 추가
                    elif word in ['이번', '다음주', '다음달', '다다', '주말']: #향후 있을 날짜 처리
                        weeks = 0,
                        if word == '이번':
                            print('hello1')
                            if token[token_idx+1][0] == '주':
                                print('hello2')
                                weeks = 1
                                if token[token_idx+2][0] in ['주말', '주', '월요일', '월요일', '월요일', '월요일', '월요일', '월요일', '월요일']:
                                    print('ddd')
                                else:   #이번주 라고 쳤을 경우
                                    print('hello3')
                                    today = datetime.today()
                                    mon_day = today + datetime.timedelta(days=-today.weekday(), weeks=0)
                                    sun_day = today + datetime.timedelta(days=-today.weekday()+6, weeks=0)
                                    mon_qu = "startdate between '" + year + "." + month + "."+mon_day.strftime("%d")+\
                                                            "' and '" + year + "." + month + "."+sun_day.strftime("%d")+"' or "
                                    print(mon_qu)
                                    # date_query += mon_qu  # 조건 한줄 씩 추가

                            #elif token[token_idx+1] == '달' or token[token_idx+1] == '월'

                    elif region_check_flg(word):  # 지역인지 체크
                        region = region_translater(word)
                        title += region + ','
                        region_list += "'" + region + "',"
                    else:
                        print(word)
                        id_list = FindPurpose.word_pupose(self, word)
                        if len(id_list) != 0:
                            for festa_id in id_list:
                                purpose_query += "id = " + str(festa_id) + " or "

                        if db_lencheck:  # 조건이 없어서 word2vec 한부분
                            sim_word_list = word2vec_obj.most_similar(word, 3)  # word2vec를 이용하여 연관된 단어 가져옴
                            print(sim_word_list)
                            for sim_word in sim_word_list:
                                print(sim_word + '연관된 애들')
                                id_list = FindPurpose.word_pupose(self, sim_word)
                                print(id_list)
                                for festa_id in id_list:
                                    purpose_query += "id = " + str(festa_id) + " or "

                token_idx += 1 #다음 인덱스

            print(str(token)+'마지막')

            if date_query != "":
                query += "(" + date_query[0:len(date_query) - 3] + ") and"  # where절에 마지막 or를 날린다  #날짜를 쿼리에 넣음
                query_cheker = True
            if region_list != "":
                query += " region in (" + region_list[
                                          :len(region_list) - 1] + ") and"  # 조건 한줄 추가 #where region in ('부산','서울')
                query_cheker = True
            if purpose_query != "":
                query += "(" + purpose_query[0:len(purpose_query) - 3] + ") and"  # where절에 마지막 or를 날린다  #날짜를 쿼리에 넣음
                query_cheker = True

            if db_lencheck and query_cheker == False:  # word2vec해도 축제가 없음
                print('word2vec해도 축제 없음!')
                print(ui.text_message("조건에 맞는 열릴 축제가 없나봐 ㅠ.ㅠ"))
                return ui.text_message("조건에 맞는 열릴 축제가 없나봐 ㅠ.ㅠ")

            elif query_cheker:  # 조건이 들어가는 쿼리가 있음
                query = query[0:len(query) - 3]
                db_obj = DBconncter().select_query(query)  # 조건이 있으면 db에 넣음
                if len(db_obj) == 0:  # word2vec으로 축제들을 가져왔지만 축제가 있는지 없는지
                    return ui.text_message("조건에 맞는 열릴 축제가 없나봐 ㅠ.ㅠ")
                else:
                    return ui.festa_list_ui(db_obj[0:5], db_obj[5:], title[0:len(title) - 1])

                if len(db_obj) == 0 and db_lencheck == False:  # 만약 db에 데이터가 없으면 재귀함수로 word2vec다시호출
                    return FindPurpose.func_list(self, True)  # db에 데이터가 없어서 다시 재귀함수 호출
                else:
                    return ui.festa_list_ui(db_obj[0:5], db_obj[5:], title[0:len(title) - 1])

            elif db_lencheck == False:  # 조건이 들어가는 쿼리가 없음
                return FindPurpose.func_list(self, True)  # word2vec 이용하여 데이터가 있나 체크

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

    def main(self):
        c = FindPurpose.func_list(self, False)
        return c
