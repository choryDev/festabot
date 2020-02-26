month = ['일월', '이월', '삼월', '사월', '오월', '육월', '칠월', '팔월', '구월', '십월', '십일월', '십이월']

month_map = {'일월': '01', '이월': '02', '삼월': '03', '사월': '04', '오월': '05', '육월': '06', '칠월': '07',
         '팔월': '08', '구월': '09', '십월': '10', '십일월': '11', '십이월': '12'}

class DateChecker:

    def month_generater(self, word):
        for v in month:
            if v == word:
                return month_map[v]
        return word

    def month_check(self, word):
        flag = False
        for v in month:
            if v == word:
                flag = True
        return flag
