# -*- coding: utf-8 -*-
import pymysql, os, sys, json, re
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './kakao_map_api')))
from get_kakaomap_api import get_restaurant_list, get_cafe_list
from location_search_kakao_api import Location_search_kakaomap_api

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../ui')))
from ui import ui

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../common')))
from common.DBconncter import  DBconncter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './open_weather_api/')))
from get_openweather_api import get_weekly_weather
from get_weather_index import getIndexList

class Option:
    def __init__(self, requset_obj):
        self.requset_obj = requset_obj
        self.sentence = requset_obj['userRequest']['utterance']
        self.usertoken = requset_obj['userRequest']['user']['properties']['plusfriendUserKey']

    def get_fest_id(self): #유저토큰을 비교하여 축제 ID를 받아오는 메소드
    
        festaid_query = 'select festa_id from user_tb where user_token like "' + str(self.usertoken) + '";'

        return DBconncter().select_query(festaid_query)[0][0]

    def get_addr(self): #축제 주소 조회
        lo_search = Location_search_kakaomap_api()
        if lo_search.check(self.sentence) == 0 :
            query = 'select region, title, address, getX, getY, img from festival_tb where id like ' + str(Option.get_fest_id(self)) + ';'
            data = DBconncter().select_query(query)

            datalist = list(data[0]) #datalist[0] == region datalist[1] == title ... datalist[4] == getY

            return ui.address_ui(datalist)
        else:
            place_list = lo_search.searchAddr(self.usertoken)
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%SEARCH ADDRESS%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print(place_list)
            # return ui.

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

        feststartdate, festenddate = festlist[3], festlist[4] #혹시 몰라 끝나는날까지 추출

        placeXY = {'x' : festlist[5], 'y' : festlist[6]}

        start_date = datetime.strptime(feststartdate,"%Y.%m.%d")
        end_date = datetime.strptime(festenddate,"%Y.%m.%d")
        print("Transformed date : start - ", start_date, "end - ", end_date)

        current_date = (datetime.now()+timedelta(hours=9)).replace(hour=0,minute=0,second=0,microsecond=0) #오늘 날짜 #서버시간은 미국기준이라 9시간더함

        print("시작날짜", start_date, "- 금일 날짜", current_date, '=', (start_date-current_date).days)
        
        if (start_date - current_date).days > 7: #축제 시작일이 금일을 기준으로 openWeather 최대 예보일(금일이후 7일)을 넘어갈 때
            return ui.month_weather_ui(start_date.month, weatherDBlist)
        else: 
            weekly_weather = get_weekly_weather(placeXY)

            fest_idx_list = getIndexList(start_date, end_date, current_date)
            print("final index = " + str(fest_idx_list))
            return ui.each_weather(weekly_weather, fest_idx_list)

    def get_restaurant(self):
        restaurant_list = []

        query = 'select getX, getY from festival_tb where id like ' + str(Option.get_fest_id(self)) + ';'
        data = DBconncter().select_query(query)

        datalist = list(data[0])

        restaurant_list = get_restaurant_list(datalist)
        print("[SERVER] Get %d item(s)" % len(restaurant_list))
        for d in restaurant_list:
            print(d)
        if len(restaurant_list) < 1: #근방에 맛집이 없을 때, 있을 때
            return ui.empty_items_ui('r')
        else:
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
        if len(cafe_list) < 1: #근방에 카페가 있을 때, 없을 때
            return ui.empty_items_ui('c') 
        else:
            return ui.cafe_ui(datalist, cafe_list)

    def get_popular_festa(self):
        query = 'select * from popular_festa order by save_date desc limit 1'   #크롤링된 인기축제 호출
        data = DBconncter().select_query(query)
        popular_list = data[0][1:]                                              #쓸모없는 첫번째 칼럼 삭제

        print(len(popular_list))
        print(popular_list)
        query = 'select title, content, img from festival_tb where title like "%' +str(popular_list)    #인기축제10개 쿼리문
        for i in range(1,10):                                                                           #
            query = query + '%" or title like "%' + str(fest_list[i])                                   #
        query = query + '%"'                                                                            #

        data = DBconncter().select_query(query)
        datalist = list(data)
        result_list = []

        for title in fest_list: #순서가 바뀐 datalist를 재 sorting하여 result_list에 저장
            for db_title in datalist:
                if title == re.sub('[0-9]+', '', db_title[0]):
                     result_list.append(db_title)
      
        return ui.popular_festa_ui(fest_list, result_list)