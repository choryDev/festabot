from konlpy.tag import Okt
import re
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from common.DBconncter import DBconncter
from common.common_stopwords import CommonStopwords
from ui import ui
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './')))
from region_ota_checker.region_checker import region_translater, region_check_flg
from date_checker.date_checker import DateChecker
from tf_idf.tf_idf import tf_idf_checker
from purpose_classification.find_purpose import FindPurpose

okt = Okt()
stopword = CommonStopwords()
month_words = ['일월', '이월', '삼월', '사월', '오월', '육월', '칠월', '팔월', '구월', '십월', '십일월', '십이월']
date_words = ['월', '화요일', '일요일', '수요일', '음주', '토요일', '달', '수', '금', '금요일', '다다', '주말', '목', '목요일', '토', '다음', '월요일', '이번', '화', '다음주', '일', '음달']
region_words = stopword.stop_words_region() + stopword.stop_words_region_sub()
date_region_words = date_words + region_words + month_words

class FestaList:

    def __init__(self, req):
        self.sentence = req['userRequest']['utterance']
        self.user = req['userRequest']['user']['id']

    def tokenizer_check(self, list):  #형태소 분석해서 문장이 들어온지 단어만 들어온지 체크
        return len(list) == len([a for a in list if a[1] in ["Noun", "Determiner", "Number", "Modifier"]]) #단어만 들어 왔을때 true

    def easy_sentence_checker(self): #지역 또는 날짜만 말한 경우인지 체커
        token_list = okt.pos(
            self.sentence,
            norm=True,  # normalize 그랰ㅋㅋ -> 그래ㅋㅋ
            stem=True,  # stemming 바뀌나->바뀌다
        )
        print(token_list)
        if FestaList.tokenizer_check(self, token_list): #형태소 분석해서 문장이 들어온지 단어만 들어온지 체크
            nouns_list = okt.nouns(self.sentence)
            return len(nouns_list) == len([a for a in nouns_list if a in date_region_words]) #명사 중에 날짜, 지역만 말하였는지 체크
        else:
            return False

    def main_func(self): #형태소 겟수 세는 함수
        if FestaList.easy_sentence_checker(self):
            return FindPurpose(self.sentence).main()
        elif tf_idf_checker(self.sentence):
            return FindPurpose(self.sentence).main()
        else:
            return ui.text_message('자유롭게 말해보세요\n예)서울에는 어떤 축제가 열릴까?, 8월에 축제 있어?, 치맥축제 추천해줘')