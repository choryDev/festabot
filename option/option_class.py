# -*- coding: utf-8 -*-
import pymysql, os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './kakao_map_api')))
from get_kakaomap_api import get_restaurant_list, get_cafe_list

host='mydb.cstof8mab94c.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = '123123123'
db = 'festabot'
charset = 'utf8'

class Option:
    def __init__(self, requset_obj):
        self.requset_obj = requset_obj
        self.sentence = requset_obj['userRequest']['utterance']

    def get_addr(self): #축제 주소 조회
        conn = pymysql.connect(host=host, user = user, 
                       password=password , db=db, charset=charset)

        curs = conn.cursor()
        sql = 'select region, title, address, getX, getY, img from festival_tb where title = "전국생활문화축제 2019";'
        curs.execute(sql)
        
        data = curs.fetchall()

        datalist = list(data[0]) #datalist[0] == region datalist[1] == title ... datalist[4] == getY

        conn.close()

        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                {
                    "basicCard": {
                    "title": datalist[1],
                    "description": datalist[2],
                    "thumbnail": {
                        "imageUrl": str(datalist[5])
                    },
                    "buttons": [
                        {
                        "action": "webLink",
                        "label": "카카오맵 열기",
                        "webLinkUrl": "daummaps://search?q=" + str(datalist[2]) + "&p=" + str(datalist[3]) + "," + str(datalist[4])
                        },
                        {
                        "action":  "webLink",
                        "label": "카카오맵 길찾기",
                        "webLinkUrl": "https://map.kakao.com/link/to/" + str(datalist[2]) + ',' + str(datalist[3]) + ',' + str(datalist[4])
                        },
                        {
                        "action": "webLink",
                        "label": "카카오맵 자동차 길찾기",
                        "webLinkUrl": "daummaps://route?sp=35.1516077265, 129.1173479525&ep=" + str(datalist[3]) + "," + str(datalist[4]) + "&by=CAR"
                        }
                    ]
                    }
                }
                ]
            }
        }
        return dataSend
    
    def get_parkinglot(self): #주차장 조회
        conn = pymysql.connect(host=host, user = user, 
                       password=password , db=db, charset=charset)

        curs = conn.cursor()
        sql = 'select region, title, address, getX, getY, img from festival_tb where title = "전국생활문화축제 2019";'
        curs.execute(sql)

        data = curs.fetchall()
        datalist = list(data[0]) #datalist[0] == region datalist[1] == title ... datalist[4] == getY

        conn.close()

        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                {
                    "basicCard": {
                    "title": datalist[1],
                    "description": datalist[2],
                    "thumbnail": {
                        "imageUrl": str(datalist[5])
                    },
                    "buttons": [
                        {
                        "action": "webLink",
                        "label": "카카오맵 주변 주차장 검색",
                        "webLinkUrl": "daummaps://search?q=주차장&p=" + str(datalist[3]) + "," + str(datalist[4])	
                        },
                        {
                        "action": "message",
                        "label": "카드형으로 검색",
                        "messageText" : "카드형으로 검색"
                        }
                    ]
                    }
                }
                ]
            }
        }
        return dataSend

    def get_weather(self):
        
        from time import strptime
        conn = pymysql.connect(host=host, user = user, 
                       password=password , db=db, charset=charset)

        curs = conn.cursor()
        sql = 'select region, title, address, startdate, enddate from festival_tb where title = "전국생활문화축제 2019";'
        curs.execute(sql)

        data = curs.fetchall()
        festlist = list(data[0]) #festlist[0] == region festlist[1] == title ... festlist[4] == getY
        
        curs = conn.cursor()
        sql = 'select * from weather_tb;'
        curs.execute(sql)

        data = curs.fetchall()
        weatherlist = list(data)
        print(festlist) #테스트
        conn.close()

        feststartdate, festenddate = festlist[3], festlist[4] #혹시 몰라 끝나는날까지 추출

        print(feststartdate,festenddate)

        fest_mon = strptime(feststartdate,"%Y.%m.%d")

        for i in range(len(weatherlist)):
            if weatherlist[i][0] == festlist[0]: #지역이 일치할때까지 반복
                print(fest_mon.tm_mon,"월", weatherlist[i][0],"의 날씨는", weatherlist[i][fest_mon.tm_mon],"입니다")

        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                         "simpleText": {
                            "text": str(fest_mon.tm_mon) + "월 " + str(weatherlist[i][0]) + "의 날씨는 " + str(weatherlist[i][fest_mon.tm_mon]) + "입니다."
                        }
                    }
                ]
            }
        }
        return dataSend

    
    def get_restaurant(self):
        restaurant_list = []
        items_list = [] 
        restaurant_list = get_restaurant_list()

        for i in range(10):
            print(restaurant_list[i]) #모니터링

        for i in range(10): #지역마다 추가
            items_list.append(
                {
                    "title": restaurant_list[i]['상호명'],
                    "description": restaurant_list[i]['주소'],
                    "thumbnail": {
                        "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                    },
                    "buttons": [
                        {
                            "action" : "webLink",
                            "label" : "지도 열기",
                            "webLinkUrl": "daummaps://look?p=" + restaurant_list[i]['y'] + "," + restaurant_list[i]['x'] #매뉴얼 상 y좌표가 앞, x좌표가 뒤
                        }
                    ]
                })


        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": items_list
                    }
                }
                ]
            }
        }
        return dataSend

    def get_cafe(self):
        cafe_list = []
        items_list = [] 
        cafe_list = get_cafe_list()

        # for i in range(10):
        #     print(cafe_list[i]) #모니터링

        for i in range(5): #imageUrl은 대체이미지 찾을 때 까지 비활성
            items_list.append(
                {
                    "title": cafe_list[i]['상호명'],
                    "description": cafe_list[i]['주소'],
                    # "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg",
                    "link": {
                        "web": "daummaps://look?p=" + cafe_list[i]['y'] + "," + cafe_list[i]['x'] #매뉴얼 상 y좌표가 앞, x좌표가 뒤
                    }
                }
            )

        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                    "listCard": {
                        "header": {
                            "title": "추천 카페"
                        },
                        "items": items_list,
                        "buttons": [
                            {
                                "label": "지도로 보기",
                                "action": "webLink",
                                "webLinkUrl" : "daummaps://search?q=카페&p=" + str(cafe_list[i]['y']) + "," + str(cafe_list[i]['x'])
                            },
                            {
                                "label": "더보기",
                                "action": "block",
                                "blockId": "5e7077b22d3cd0000121a040",
                                "extra": {
                                    "another_list" : cafe_list[5:len(cafe_list)]
                                }
                            }
                        ]
                    }
                }
                ]
            }
        }
        return dataSend