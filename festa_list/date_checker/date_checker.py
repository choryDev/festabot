month = ['일월', '이월', '삼월', '사월', '오월', '육월', '칠월', '팔월', '구월', '십월', '십일월', '십이월']

month_map = {'일월': '01', '이월': '02', '삼월': '03', '사월': '04', '오월': '05', '육월': '06', '칠월': '07',
         '팔월': '08', '구월': '09', '십월': '10', '십일월': '11', '십이월': '12'}
# de_month = ['한', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉', '열']
# de_month_map = {'한':1, '두':2, '세':3, '네':4, '다섯':5, '여섯':6, '일곱':7, '여덟':8, '아홉':9, '열':10}
de_month = ['두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉', '열']
de_month_map = {'두':2, '세':3, '네':4, '다섯':5, '여섯':6, '일곱':7, '여덟':8, '아홉':9, '열':10}

class DateChecker:

    def month_generater(word):
        for v in month:
            if v == word:
                return month_map[v]
        return word

    def month_check(word):
        flag = False
        for v in month:
            if v == word:
                flag = True
        return flag

    def de_month_generater(word):
        for v in de_month:
            if v == word:
                return de_month_map[v]
        return word

    def de_month_check(word):
        flag = False
        for v in de_month:
            if v == word:
                flag = True
        return flag

