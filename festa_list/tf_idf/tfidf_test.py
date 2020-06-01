import csv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from konlpy.tag import Okt


okt = Okt()
pd.options.mode.chained_assignment = None
np.random.seed(0)

key = ["축제", "인기"]

class tf_idf_classification:
    def __init__(self):
        self.word_dictionary = dict()
        # 각 목적에 따라 문서(문장 리스트) 만들기
        self.festival_contents = ""
        self.popular_contents = ""
        self.doc_list = []

        # 각 목적에 따라 문서(문장 리스트) 만들기
        f = open('object_sentence.csv', 'r', encoding='utf-8')
        rdr = csv.reader(f)
        for line in rdr:
            if line[0] == "1":
                self.festival_contents += line[1] + " "
            elif line[0] == "2":
                self.popular_contents += line[1] + " "
        f.close()
        contents = [self.festival_contents, self.popular_contents]

        # 각 문서내용을 토큰화하여 만든 리스트를 doc_list에 붙이기
        for content in contents:
            #토큰화하여 나눈 문자열 합쳐서 doc_list에 append하기
            self.doc_list.append(' '.join(self.tokenizer(content)))


   # tokenizer : 문장에서 색인어 추출을 위해 명사,동사,알파벳,숫자 정도의 단어만 뽑아서 normalization, stemming 처리하도록 함
    def tokenizer(self, raw, pos=["Noun", "Verb", "Number"], stopword=[]):
        return [
            word for word, tag in okt.pos(
                raw,
                norm=True,  # normalize
                stem=True  # stemming
            )
            if tag in pos and word not in stopword
        ]

   
    #tf idf값을 가중치로 설정한 벡터 생성
    def tf_predict(self,msg):
        tfidf_vetorizer = TfidfVectorizer(min_df=1, tokenizer=self.tokenizer) # tfdif 백터객체
        tfidf_matrix = tfidf_vetorizer.fit_transform(self.doc_list) #document-term matrix 생성
        features = tfidf_vetorizer.get_feature_names()
        # msg를 토큰화하여 각 토큰을 가져온 뒤 feature에 해당하는 토큰 리스트만듬
        srch = [msg for msg in self.tokenizer(msg) if msg in features]

        srch_dtm = np.asarray(tfidf_matrix.toarray())[:, [
               # vectorize.vocabulary_.get 는 특정 feature 가 document-term matrix 에서 가지고 있는 index값(개수)을 리턴
               tfidf_vetorizer.vocabulary_.get(i) for i in srch
        ]]   #전체 매트릭스(toarry)에서 srch 만큼만 뽑아서 ndarray로 변환
        score = srch_dtm.sum(axis=1) #보기 쉽도록 각 열마다 더함
        print(score)
        #  0 이상이라면 딕셔너리에 넣기
        for i in range(0, len(score)):
            if score[i] > 0:
                self.word_dictionary.setdefault(key[i], score[i])
            else:
                return 0
        dic_max = max(self.word_dictionary.keys(), key=(lambda k: self.word_dictionary[k]))  #딕셔너리에서 가장 큰 값 key 뽑기
        if dic_max == "인기":
            result = self.check_value(msg)
            print(self.word_dictionary)
        return result

    #만약 값이 인기일 경우 축제조회인지 다시 확인
    def check_value(self, msg):
        stopword = ["인기", "추천","축제"]
        pos = ["Noun"]
        value_token = self.tokenizer(msg, pos, stopword)
        print(value_token)
        if not value_token:     #토큰화 후 받은 리스트가 비어있는 경우 = 인기축제 조회
            return 2
        else:
            return 1          #토큰화 후 받은 리스트가 비어있지 않은 경우 = 축제조회로
