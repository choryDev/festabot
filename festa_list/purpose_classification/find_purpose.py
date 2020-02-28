from konlpy.tag import Okt
import json
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from common.DBconncter import DBconncter
from common.common_stopwords import CommonStopwords
from word2vec.word2vec_obj import Word2vecObj
from ui.ui import Ui

ui = Ui()
stopword = CommonStopwords()

class FindPurpose:

    def __init__(self, sentence):
        path = '/home/ubuntu/festabot/festa_list/purpose_classification/word_freq_dir/'
        self.word = ''
        # with open('word_freq_dir/word_freq' + str(int(datetime.today().strftime("%Y%m%d"))-1) + '.json', 'r', encoding="utf-8") as f:
        with open(path+'word_freq20200220.json', 'r', encoding="utf-8") as f:
            json_data = json.load(f)
        self.json_data = json_data
        self.word2vec_obj = Word2vecObj()
        self.sentence = sentence

    # tokenizer : 문장에서 색인어 추출을 위해 명사,수사, ,숫자 정도의 단어만 뽑아서 normalization, stemming 처리하도록 함
    def tokenizer(raw, pos=["Noun", "Determiner", "Number"], stopword=stopword.stop_words_another):
        return [
            word for word, tag in okt.pos(
                raw,
                norm=True,  # normalize 그랰ㅋㅋ -> 그래ㅋㅋ
                stem=True  # stemming 바뀌나->바뀌다
            )
            if len(word) > 1 and tag in pos and word not in stopword
        ]

    def main(self):
        print(FindPurpose.tokenizer(self.sentence))

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
