import json
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.DBconncter import DBconncter

class Find_purpose:

    def __init__(self, word):
        self.word = word
        with open('word_freq_dir/word_freq' + str(int(datetime.today().strftime("%Y%m%d"))-1) + '.json', 'r', encoding="utf-8") as f:
            json_data = json.load(f)
        self.json_data = json_data

    def exist_data_ui(festa_list):
        list = []
        for v in festa_list:
            item = {
                       "title": v[2],
                       "description": v[10],
                       "imageUrl": v[11],
                       "link": {
                           "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
                       },
                       "action": "block",
                       "blockId": "5e4feb4e8192ac00015843f1",
                       "extra": {
                           "test": "test 디제이~",
                           "test2": "test 디제이~"
                       }
                   },
            list.append(item[0])
        send_data = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "listCard": {
                            "header": {
                                "title": "카카오 i 디벨로퍼스를 소개합니다",
                                "imageUrl": "http://k.kakaocdn.net/dn/xsBdT/btqqIzbK4Hc/F39JI8XNVDMP9jPvoVdxl1/2x1.jpg"
                            },
                            "items": list[:5],
                            "buttons": [
                                {
                                    "label": "구경가기",
                                    "action": "block",
                                    "blockId": "5e4feb4e8192ac00015843f1",
                                    "extra": {
                                        "test": "test 디제이~",
                                        "test2": "test 디제이~"
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }
        return send_data

    def location_condition_search(self): #단어만 온 경우
        festa_list = []
        for r in self.json_data:
            if r['region'] in '대전':
                for v in r['freq_words']:
                    if v['word'] == self.word:
                        festa_list.append(r['id'])
        return festa_list

    def none_condition_search(self):     #조건이 없음
        festa_list = []
        for r in self.json_data:
            for v in r['freq_words']:    #단어 들어가는 지만 체크
                if v['word'] == self.word:
                    festa_list.append(r['id'])

        if len(festa_list) == 0:
            print("없네")
        else:
            condition_query = ''             #쿼리 만듬
            for v in festa_list:
                condition_query += ' id = ' + str(v) + ' or'
            where_query = condition_query[0:len(condition_query)-3]
            query = 'select * from festival_tb where' + where_query
            db_obj = DBconncter().select_query(query)
            return Find_purpose.exist_data_ui(db_obj)

    def month_condition_search(self):
        festa_list = []
        for r in self.json_data:
            if r['startdate'] in '01':
                for v in r['freq_words']:
                    if v['word'] == self.word:
                        festa_list.append(r['id'])
        return festa_list

    def find_purpose_first(self): #첫번째 단계
        word = self.word
        return Find_purpose.none_condition_search(self)