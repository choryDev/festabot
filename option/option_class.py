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
                        "messageText" : "test"
                        }
                    ]
                    }
                }
                ]
            }
        }
        return dataSend

    def get_weather(self):
        print("[SERVER] Received '날씨'")
  
    
    def get_restaurant(self):
        restaurant_list = []
        items_list = [] 
        restaurant_list = get_restaurant_list()

        for i in range(10):
            print(restaurant_list[i]) #모니터링

        for i in range(10):
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

        for i in range(10):
            print(cafe_list[i]) #모니터링

        for i in range(10):
            items_list.append(
                {
                    "title": cafe_list[i]['상호명'],
                    "description": cafe_list[i]['주소'],
                    "thumbnail": {
                        "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                    },
                    "buttons": [
                        {
                            "action" : "webLink",
                            "label" : "지도 열기",
                            "webLinkUrl": "daummaps://look?p=" + cafe_list[i]['y'] + "," + cafe_list[i]['x'] #매뉴얼 상 y좌표가 앞, x좌표가 뒤
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