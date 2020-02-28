import csv
import pandas as pd

pd.options.mode.chained_assignment = None

import numpy as np

np.random.seed(0)

from konlpy.tag import Okt

okt = Okt()

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity


# tokenizer : 문장에서 색인어 추출을 위해 명사,동사,알파벳,숫자 정도의 단어만 뽑아서 normalization, stemming 처리하도록 함
def tokenizer(raw, pos=["Noun", "Verb", "Number"], stopword=[]):
    return [
        word for word, tag in okt.pos(
            raw,
            norm=True,  # normalize 그랰ㅋㅋ -> 그래ㅋㅋ
            stem=True  # stemming 바뀌나->바뀌다
        )
        if len(word) > 1 and tag in pos and word not in stopword
    ]


# 테스트 문장
rawdata = []

f = open('/home/ubuntu/festabot/festa_list/tf_idf/first_sentence.csv', 'r', encoding='utf-8')  # 텍스트 학습
rdr = csv.reader(f)
for line in rdr:
    rawdata.append(line[0])
f.close()

vectorize = TfidfVectorizer(
    tokenizer=tokenizer,
    min_df=2,
    sublinear_tf=True  # tf값에 1+log(tf)를 적용하여 tf값이 무한정 커지는 것을 막음
)
X = vectorize.fit_transform(rawdata)

print(
    'fit_transform, (sentence {}, feature {})'.format(X.shape[0], X.shape[1])
)
# fit_transform, (sentence 5, feature 7)

# 문장에서 뽑아낸 feature 들의 배열
features = vectorize.get_feature_names()


def tf_idf_checker(sentence):
    # 검색 문장에서 feature를 뽑아냄
    srch = [t for t in tokenizer(sentence) if t in features]
    print(srch)
    # ['1987', '대통령']

    # dtm 에서 검색하고자 하는 feature만 뽑아낸다.
    srch_dtm = np.asarray(X.toarray())[:, [
                                              # vectorize.vocabulary_.get 는 특정 feature 가 dtm 에서 가지고 있는 index값을 리턴한다
                                              vectorize.vocabulary_.get(i) for i in srch
                                          ]]

    score = srch_dtm.sum(axis=1)
    # array([0.         0.         1.10877443 1.40815765 0.8695635 ], dtype=int64) 문장별 feature 합계 점수

    tf_idf = False  # 체크 축제를 묻는게 맞는지 체크해주는 플래그
    score = score.argsort()[::-1]
    if score[0] > 0:
        tf_idf = True
    # for i in :
    #     if score[i] :
    #         print('{} / score : {}'.format(rawdata[i], score[i]))


    return tf_idf
