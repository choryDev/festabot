from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
np.random.seed(0)
from konlpy.tag import Mecab
import re
import make_doc
import sys

doc_list = []
contents = [make_doc.place_contents, make_doc.parking_contents, make_doc.weather_contents,
            make_doc.restaurant_contents,
            make_doc.cafe_contents, make_doc.relation_contents, make_doc.popular_contents]
value = ["장소", "주차장", "날씨", "맛집", "카페", "연관", "인기"]
doc_list = []

class tf_idf_classification:
  def __init__(self):
      make_doc.make_doc()
      for i in range(0, len(contents)):
           self.make_dic(contents[i])

  # class tf_idf():
  def make_dic(self, content):
     value = self.tokenizer(re.sub('[-\(),:&/?]', '', content))
     doc_list.append(' '.join(value))
     return doc_list

 #pos=["Noun", "Verb", "Number"]

  def tokenizer(self, raw, pos=["NNG","NNP", "VV", "SN"], stopword=['축제']):
     mecab = Mecab()
     return [
         word for word, tag in mecab.pos(
             raw
             # norm=True,  # normalize 그랰ㅋㅋ -> 그래ㅋㅋ
             # stem=True  # stemming 바뀌나->바뀌다
         )
         if tag in pos and word not in stopword
     ]


 #tf idf값을 가중치로 설정한 벡터 생성
  def tf_predict(self, msg):
       word_dictionary = dict()
       tfidf_vetorizer = TfidfVectorizer(min_df=1, tokenizer= self.tokenizer)
       tfidf_matrix = tfidf_vetorizer.fit_transform(doc_list)

       doc_distances = (tfidf_matrix * tfidf_matrix.T)
       print(
        'fit_transform, (sentence {}, feature {})'.format(doc_distances.shape[0], doc_distances.shape[1])
       )
       print(doc_distances.toarray())
       features = tfidf_vetorizer.get_feature_names()
       #테스트 문장에서 단어 뽑아냄
       srch = [msg for msg in self.tokenizer(msg) if msg in features]
       print(srch)

       srch_dtm = np.asarray(tfidf_matrix.toarray())[:, [
       # vectorize.vocabulary_.get 는 특정 feature 가 dtm 에서 가지고 있는 index값을 리턴한다
              tfidf_vetorizer.vocabulary_.get(i) for i in srch
       ]]
        #
       score = srch_dtm.sum(axis=1)
       #tf-idf 값 정렬
       for i in range(0, len(value)):
          word_dictionary.setdefault(value[i], score[i])
       print(word_dictionary)
       dic_max = max(word_dictionary.keys(), key=(lambda k: word_dictionary[k]))
       print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
       print([dic_max, str(word_dictionary[dic_max]) ])
       print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
       return [dic_max, str(word_dictionary[dic_max]) ]



    # return str(dic_max + word_dictionary[dic_max])


#
#자연어처리시 n-gram으로 해보기/ 클래스로 모듈화 하기
