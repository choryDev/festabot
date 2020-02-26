# from bayes import BayesianFilter
import bayes
import csv
bf = bayes.BayesianFilter()

class BayesSiml:

    def checker(self, sentence):
        f = open('first_sentence.csv', 'r', encoding='utf-8')# 텍스트 학습
        rdr = csv.reader(f)
        for line in rdr:
            bf.fit(line[0], line[1]),
        f.close()

        # 예측
        pre, scorelist = bf.predict(sentence)
        # print("결과 = ", pre)
        # print(scorelist)
        return scorelist[0][1]