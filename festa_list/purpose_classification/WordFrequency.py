import os
import sys
from konlpy.tag import Mecab
from collections import Counter
import re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from common.common_stopwords import CommonStopwords

mecab = Mecab()
st_obj = CommonStopwords()
stop_word = st_obj.stop_words_region() + st_obj.stop_words_another()

class WordFrequency:

    def mecab_tokenizer(raw, pos=["NNP", "NNG"]):
        obj = mecab.pos(raw)
        list = []
        for word, tag in obj:
            if tag in pos and word not in stop_word:  # 형태소 태그, 불용어 처리
                list.append(word)
        return list

    def get_noun(self, sentence, ntags=50): #명사만 뽑는 함수
        nouns = WordFrequency.mecab_tokenizer(sentence)
        count = Counter(nouns)
        return_list = []
        for n, c in count.most_common(ntags):
            temp = {'word': n, 'count': c}
            return_list.append(temp)
        return return_list

    # def split_festa_title(self, festa_title, blog_title):
    #     #축제 제목을 토큰화 시켜서 그 단어가 블로그 제목에 있는지 확인하는 함수
    #     flag = False
    #     stop_words = Common_stopwords().stop_words_region()
    #
    #     okt = Okt()
    #     festa_title = re.sub('[0-9]', '', festa_title) #숫자 제거
    #
    #     for word in okt.nouns(festa_title):
    #         for stop_word in stop_words:
    #             if stop_word in word: #불용어 있으면 무시
    #                 continue
    #             if word in blog_title: #만약 축제 제목을 나눈 것이 있으면 1
    #                 flag = 1
    #     return flag
