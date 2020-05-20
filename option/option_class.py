# -*- coding: utf-8 -*-
import pymysql, os, sys
# from time import strptime
from datetime import datetime
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
        query = 'select region, title, address, startdate, enddate, getX, getY from festival_tb where id like ' + str(Option.get_fest_id(self)) + ';'
        data = DBconncter().select_query(query)

        festlist = list(data[0]) 
        
        query = 'select * from weather_tb where region like "' + str(festlist[0]) + '";'
        data = DBconncter().select_query(query)

        weatherDBlist = list(data)
        print(festlist) #monitoring

        feststartdate, festenddate = festlist[3], festlist[4] #혹시 몰라 끝나는날까지 추출

        placeXY = {'x' : festlist[5], 'y' : festlist[6]}

        start_date = datetime.strptime(feststartdate,"%Y.%m.%d")
        end_date = datetime.strptime(festenddate,"%Y.%m.%d")
        print("Transformed date : start - ", start_date, "end - ", end_date)
        
        return ui.weather_ui(start_date, end_date, weatherDBlist, placeXY)

    def get_restaurant(self):
        restaurant_list = []

        query = 'select getX, getY from festival_tb where id like ' + str(Option.get_fest_id(self)) + ';'
        data = DBconncter().select_query(query)

        datalist = list(data[0])

        restaurant_list = get_restaurant_list(datalist)
        print("[SERVER] Get %d item(s)" % len(restaurant_list))
        for d in restaurant_list:
            print(d)
        return ui.restaurant_ui(datalist, restaurant_list)

    def get_cafe(self):
        cafe_list = []

        query = 'select getX, getY from festival_tb where id like ' + str(Option.get_fest_id(self)) + ';'
        data = DBconncter().select_query(query)
        
        datalist = list(data[0]) 

        cafe_list = get_cafe_list(datalist)
        print("[SERVER] Get %d item(s)" % len(cafe_list))
        for d in cafe_list:
            print(d)
        return ui.cafe_ui(datalist, cafe_list)