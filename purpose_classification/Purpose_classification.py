from konlpy.tag import Okt
import pymysql
from common.DBconncter import DBconncter
from konlpy.tag import Okt
from collections import Counter

class Purpose_classification:

    # def __init__(self, response_obj):
    #     self.okt = Okt()
    #     self.req = response_obj['userRequest']
    #     self.content = response_obj['utterance']
    #     self.user = response_obj['user']['id']

    def selected_festa_checker(self): #사용자가 축제를 선택한 지 보여주는 함수
        checker = DBconncter().select_query('select * from user_tb where ='+ self.user) is ()
        return checker

    def stemming_number_counter(self, content): #형태소 겟수 세는 함수
        okt = Okt()
        stem_list = okt.pos(content)
        counter = 0
        for c in stem_list:
            if c[1] == 'Number':
                counter += 1
        if counter is len(stem_list):
            return True
        else:
            return False

    def stemming_region_counter(self, content):
        okt = Okt()
        stem_list = okt.pos(content)


d = Purpose_classification().func_stemming_counter('1월 2월')
print(d)

