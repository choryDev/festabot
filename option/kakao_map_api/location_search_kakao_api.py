from konlpy.tag import Okt
import requests
import json
import pymysql

stopword = ['거기','길','상세','주변','주소','축제', '어디', '위치', '어딘', '말', '저기', '야', '페스타봇', '헤이','그럼','난', '임', '누', '금방', '인근', '근처']

class Location_search_kakaomap_api:

    def __init__(self):
        self.token_sentence = []
    # 토큰화
    def tokenizer(self, msg):
        okt = Okt()
        return [word for word in okt.nouns(msg) if word not in stopword]

    #받은 문장 체크하기
    def check(self, msg):#userToken 사용자 토큰 받아옴
        self.token_sentence = self.tokenizer(msg)
        return len(self.token_sentence)

    #카카오 api 주소 검색
    def searchAddr(self, user):
        x, y= self.joinData(user)
        sentence = [' '+a for a in self.token_sentence]

        url = "https://dapi.kakao.com/v2/local/search/keyword.json?x=" + str(y) + "&y=" + str(x) + "&radius=5000" #radius는 미터단위
        apikey = "5e5acc55c8584f36abffe26633c82550"
        query = str(sentence)

        r = requests.get( url, params = {'query':query}, headers={'Authorization' : 'KakaoAK ' + apikey })

        place_list = [] #호출된 데이터 dict형태로 만들어 array로 저장
        obj_list = r.json()["documents"]
        for v in obj_list:
            print(v)
            place_list.append( {
                '상호명' : v['place_name'],
                '주소' : v['address_name'],
                'x' : v['x'],
                'y' : v['y'],
                'url' : v['place_url']})

        return ' '.join(sentence), place_list
        #[msg for msg in self.tokenizer(msg) if msg in msg]

    #db에서 현재 선택한 축제의 지역명 가져오기
    def joinData(self, user):
        result = None
        db = pymysql.connect(
            host="mydb.cstof8mab94c.ap-northeast-2.rds.amazonaws.com", port=3306, user="admin", passwd="123123123", db='festabot', charset='utf8')
        try:
            cursor = db.cursor()
            sql = "select fd.getX, fd.getY from festival_tb fd inner join user_tb ut on '"+user+"' = ut.user_token and fd.id = ut.festa_id "
            cursor.execute(sql)
            result = cursor.fetchone()
            print("result = ",result)
        finally:
            db.close()
        return result
