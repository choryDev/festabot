import sys
from konlpy.tag import Okt
from collections import Counter
from common_stopwords import Common_stopwords
import re

class WordFrequency:

    def get_noun(self, sentence, ntags=300): #명사만 뽑는 함수
        okt = Okt()
        nouns = okt.nouns(sentence)
        count = Counter(nouns)
        return_list = []
        stop_words = Common_stopwords().stop_words_region() # 지역이름
        stop_words.extend(Common_stopwords().stop_words_another()) #쓸때 없는 단어
        for n, c in count.most_common(ntags):
            flag = 1
            for stop_word in stop_words : # 불용어 들어가는지 체크
                if stop_word in n or len(n) == 1:        # 불용어 들어가면 false
                    flag = 0
            if bool(flag):                # 불용어 안들어가면 true
                temp = {'word': n, 'count': c}
                return_list.append(temp)
        return return_list

    def split_festa_title(self, festa_title, blog_title):
        #축제 제목을 토큰화 시켜서 그 단어가 블로그 제목에 있는지 확인하는 함수
        flag = False
        stop_words = Common_stopwords().stop_words_region()

        okt = Okt()
        festa_title = re.sub('[0-9]', '', festa_title) #숫자 제거

        for word in okt.nouns(festa_title):
            for stop_word in stop_words:
                if stop_word in word: #불용어 있으면 무시
                    continue
                if word in blog_title: #만약 축제 제목을 나눈 것이 있으면 1
                    flag = 1
        return flag