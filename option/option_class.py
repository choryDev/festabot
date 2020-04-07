# -*- coding: utf-8 -*-
import pymysql, os, sys
from time import strptime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './kakao_map_api')))
from get_kakaomap_api import get_restaurant_list, get_cafe_list

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../ui')))
from ui import ui

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../common')))
from common.DBconncter import  DBconncter

class Option:
    def __init__(self, requset_obj):
        self.requset_obj = requset_obj
        self.sentence = requset_obj['userRequest']['utterance']
        self.usertoken = requset_obj['userRequest']['user']['properties']['plusfriendUserKey']

    def get_fest_id(self): #유저토큰을 비교하여 축제 ID를 받아오는 메소드
        festaid_query = 'select festa_id from user_tb where user_token like "' + str(self.usertoken) + '";'

        return DBconncter().select_query(festaid_query)[0][0]

    def get_addr(self): #축제 주소 조회
        query = 'select region, title, address, getX, getY, img from festival_tb where id like ' + str(Option.get_fest_id(self)) + ';'
        data = DBconncter().select_query(query)

        datalist = list(data[0]) #datalist[0] == region datalist[1] == title ... datalist[4] == getY

        return ui.address_ui(datalist)
    
    def get_parkinglot(self): #주차장 조회
        query = 'select region, title, address, getX, getY, img from festival_tb where id like ' + str(Option.get_fest_id(self)) + ';'
        data = DBconncter().select_query(query)

        datalist = list(data[0]) #datalist[0] == region datalist[1] == title ... datalist[4] == getY

        return ui.parkinglot_ui(datalist)

    def get_weather(self):
        query = 'select region, title, address, startdate, enddate from festival_tb where id like ' + str(Option.get_fest_id(self)) + ';'
        data = DBconncter().select_query(query)

        festlist = list(data[0]) #festlist[0] == region festlist[1] == title ... festlist[4] == getY
        
        query = 'select * from weather_tb where region like "' + str(festlist[0]) + '";'
        data = DBconncter().select_query(query)

        weatherlist = list(data)
        print(festlist) #monitoring

        feststartdate, festenddate = festlist[3], festlist[4] #혹시 몰라 끝나는날까지 추출
        print(feststartdate,festenddate) #시작일, 마지막날 모니터링

        fest_mon = strptime(feststartdate,"%Y.%m.%d")

        return ui.weather_ui(fest_mon, weatherlist)

    def get_restaurant(self):
        restaurant_list = []
        items_list = [] 

        query = 'select getX, getY from festival_tb where id like ' + str(Option.get_fest_id(self)) + ';'
        data = DBconncter().select_query(query)

        datalist = list(data[0]) 

        restaurant_list = get_restaurant_list(datalist)

        for i in range(5): #지역마다 추가
            items_list.append(
                {
                    "title": restaurant_list[i]['상호명'],
                    "description": restaurant_list[i]['주소'],
                    # "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg",

                    "link": {
                            "web": "daummaps://look?p=" + restaurant_list[i]['y'] + "," + restaurant_list[i]['x'] #매뉴얼 상 y좌표가 앞, x좌표가 뒤
                        }
                }
            )
        return ui.restaurant_ui(datalist, items_list, restaurant_list)

    def get_cafe(self):
        cafe_list = []
        items_list = [] 

        query = 'select getX, getY from festival_tb where id like ' + str(Option.get_fest_id(self)) + ';'
        data = DBconncter().select_query(query)

        datalist = list(data[0]) 

        cafe_list = get_cafe_list(datalist)

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
        return ui.cafe_ui(datalist, items_list, cafe_list)