import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './')))
from bayes import BayesianFilter
import csv
bf = BayesianFilter()

class BayesSiml:

    def checker(self, sentence):
        f = open('/home/ubuntu/festabot/festa_list/naive_bayes/first_sentence.csv', 'r', encoding='utf-8')# 텍스트 학습
        rdr = csv.reader(f)
        for line in rdr:
            bf.fit(line[0], line[1]),
        f.close()

        # 예측
        pre, scorelist = bf.predict(sentence)
        # print("결과 = ", pre)
        # print(scorelist)
        return scorelist[0][1]