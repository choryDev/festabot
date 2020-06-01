from datetime import datetime
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../option/open_weather_api/')))
from weather_condition_dic import weather_cond_dic as wthrCondD

exit_simpleText_ui = {
    "simpleText" : {
        "text" : "다른 축제를 검색하시려면 '나가기'라고 입력하시거나 아래 '다른축제검색하기'버튼을 눌러주세요."
        }
        }

exit_quickreply_ui =[{
    "label": "다른축제검색하기",
    "action": "message",
    "messageText": "나가기"
    }
    ]

def none_festa_list_ui(word):
    send_data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": word + "에 대한 축제 정보를 못찾겠습니다. ㅠㅠ"
                    }
                }
            ]
        }
    }
    return send_data

def festa_list_ui(festa_list, another_festa_list, word):
    item_list = []
    btn_list = []
    i = 0
    for v in festa_list:
        i += 1
        item = {
                   "title": str(i)+"."+v[2],
                   "description": '' if v[10]=='null' else  v[10], #만약 null 이면 빈값
                   "imageUrl": v[15],
                   "link": {
                       "web": v[5]
                   },
               },
        btn = {
                    "label": '축제' +  str(i),
                    "action": "block",
                    "blockId": "5e50dad192690d00014efe09",
                      "extra": {
                          "id": v[0],
                      }
                },
        item_list.append(item[0]) #괄호를 지우기 위해 서 [0] 사용
        btn_list.append(btn[0])
    send_data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "listCard": {
                        "header": {
                            "title": word+'에 대한 축제 리스트 입니다.'
                        },
                        "items": item_list[:5],

                        "buttons": [ None if len(another_festa_list) == 0 else
                                     {
                                "label": "더보기",
                                "action": "block",
                                "blockId": "5e4feb4e8192ac00015843f1",
                                "extra": {
                                    "another_festa_list": another_festa_list,
                                    "word": word
                                }
                            }]
                    }
                }
            ],
            "quickReplies": btn_list
        }
    }
    return send_data

def festa_description(db_obj):
    desc = "기간 : " + db_obj[6] + " ~ " + db_obj[7] + "\n" \
            "주최/ 주관 : " + db_obj[3] + "\n" \
            "장소 : " + db_obj[8] + "\n" \
            "주소 : " + db_obj[9] + "\n" \
            "상제 정보 : " + db_obj[10]

    if str(db_obj[4][0]).isdigit():
        phoneNumber = str(db_obj[4])
    else:
        phoneNumber = ''

    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": db_obj[2],
                        "description": desc,
                        "thumbnail": {
                            "imageUrl": db_obj[15]
                        },
                        "profile": {
                            "imageUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4BJ9LU4Ikr_EvZLmijfcjzQKMRCJ2bO3A8SVKNuQ78zu2KOqM",
                            "nickname": "보물상자"
                        },
                        "social": {
                            "like": 1238,
                            "comment": 8,
                            "share": 780
                        },
                        "buttons": [
                            {
                                "label": "옵션보기",
                                "action": "message",
                                "messageText": '"상세주소", "주차장조회", "맛집조회", "카페조회", "날씨"가 있습니다.\n "주소가 뭐야?"등 자유롭게 옵션을 조회해보세요'
                            },
                            {
                                "label": "전화하기",
                                "action": "phone",
                                "phoneNumber": phoneNumber
                            },
                            {
                                "label": "공유하기",
                                "action": "share"
                            }
                        ]
                    }
                },
                exit_simpleText_ui
            ],
            "quickReplies": exit_quickreply_ui
        }
    }
    return dataSend

def text_message(sentence):
    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": sentence
                    }
                }
            ]
        }
    }
    return dataSend

########################### Jonghun UIs ###########################

def address_ui(datalist): #주소UI
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
                    "label": "지도로 위치 보기",
                    "webLinkUrl": "daummaps://search?q=" + str(datalist[2]) + "&p=" + str(datalist[3]) + "," + str(datalist[4])
                    },
                    {
                    "action": "webLink",
                    "label": "지도로 자동차 길찾기",
                    "webLinkUrl": "daummaps://route?sp=35.1516077265, 129.1173479525&ep=" + str(datalist[3]) + "," + str(datalist[4]) + "&by=CAR"
                    },
                    {
                    "action": "webLink",
                    "label": "지도로 대중교통 길찾기",
                    "webLinkUrl": "daummaps://route?sp=35.1516077265, 129.1173479525&ep=" + str(datalist[3]) + "," + str(datalist[4]) + "&by=PUBLICTRANSIT"
                    }
                ]
                }
            }
            ]
        }
    }
    return dataSend

def parkinglot_ui(datalist): #주차장UI
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
                    "label": "주변 주차장 지도로 보기",
                    "webLinkUrl": "daummaps://search?q=주차장&p=" + str(datalist[3]) + "," + str(datalist[4])	
                    }
                ]
                }
            }
            ]
        }
    }
    return dataSend

def month_weather_ui(month, weatherDBlist):
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                        {
                            "simpleText": {
                            "text": "상세 날씨는 축제 시작 1 주일 전 부터 조회가 되어 평년 날씨를 알려드릴게요."
                        }
                    },
                    {
                            "simpleText": {
                            "text": str(month) + "월 " + str(weatherDBlist[0][0]) + "의 평년 날씨는 " + str(weatherDBlist[0][month]) + "입니다."
                        }
                    }
                ]
            }
        }
        return dataSend

def each_weather(weekly_weather, fest_idx_list):
    items_list = []
    another_idx = fest_idx_list[5:len(fest_idx_list)]
    for i in fest_idx_list[:5]:
        items_list.append(
            {
                "title" : str(datetime.fromtimestamp(weekly_weather[i]['dt']).month) + "/" + str(datetime.fromtimestamp(weekly_weather[i]['dt']).day) + " " + str(wthrCondD[int(weekly_weather[i]['weather'][0]['id'])]),
                "description" : str(weekly_weather[i]['temp']['max'])+"°C/" + str(weekly_weather[i]['temp']['min'])+"°C",
                "imageUrl" : "http://openweathermap.org/img/wn/" + str(weekly_weather[i]['weather'][0]['icon']) + "@2x.png"
            }
        )

    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                "listCard": {
                    "header": {
                        "title": "날씨"
                    },
                    "items": items_list,
                    "buttons": [
                        None if len(another_idx) == 0 else {
                            "label": "더보기",
                            "action": "block",
                            "blockId": "5ec4cb3e501c670001e49b95",
                            "extra":{
                                "weekly_weather" : weekly_weather,
                                "fest_idx_list" : another_idx
                            }

                        }
                    ]
                }
            }
            ]
        }
    }

    return dataSend
   


def restaurant_ui(datalist, restaurant_list):
    items_list = []
    for obj in restaurant_list[:5]: #지역마다 추가
        items_list.append(
        {
            "title": obj['상호명'],
            "description": obj['주소'],
            "link": {
                    "web": "daummaps://look?p=" + obj['y'] + "," + obj['x'] #매뉴얼 상 y좌표가 앞, x좌표가 뒤
                }
        })

    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                "listCard": {
                    "header": {
                        "title": "반경 3km 내 추천 맛집"
                    },
                    "items": items_list,
                    "buttons": [
                        {
                            "label": "지도로 보기",
                            "action": "webLink",
                            "webLinkUrl" : "daummaps://search?q=맛집&p=" + str(datalist[0]) + "," + str(datalist[1])
                        },
                        None if len(restaurant_list[5:len(restaurant_list)]) == 0 else {
                            "label": "더보기",
                            "action": "block",
                            "blockId": "5e7077b22d3cd0000121a040",
                            "extra": {
                                "type":"restaurant",
                                "another_list" : restaurant_list[5:len(restaurant_list)],
                                "datalist": datalist
                            }
                        }
                    ]
                }
            }
            ]
        }
    }
    return dataSend

def cafe_ui(datalist, cafe_list):
    items_list = []
    for obj in cafe_list[:5]: #지역마다 추가
        items_list.append(
            {
                "title": obj['상호명'],
                "description": obj['주소'],
                "link": {
                    "web": "daummaps://look?p=" + obj['y'] + "," + obj['x'] #매뉴얼 상 y좌표가 앞, x좌표가 뒤
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
                        "title": "반경 3km 내 추천 카페"
                    },
                    "items": items_list,
                    "buttons": [
                        {
                            "label": "지도로 보기",
                            "action": "webLink",
                            "webLinkUrl" : "daummaps://search?q=카페&p=" + str(datalist[0]) + "," + str(datalist[1])
                        },
                        None if len(cafe_list[5:len(cafe_list)]) == 0 else {
                            "label": "더보기",
                            "action": "block",
                            "blockId": "5e7077b22d3cd0000121a040",
                            "extra": {
                                "type":"cafe",
                                "another_list" : cafe_list[5:len(cafe_list)],
                                "datalist": datalist
                            }
                        }
                    ]
                }
            }
            ]
        }
    }
    return dataSend

def empty_items_ui(sel): #추천 맛집이나 카페가 없을 때 출력할 function
    if sel == 'r':
        text = "반경 3km 이내에 추천맛집이 없습니다"
    else:
        text = "반경 3km 이내에 추천카페가 없습니다"

    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": text
                    }
                }
            ]
        }
    }
    return dataSend

def popular_festa_ui(result_list):
    another_list = result_list[5:len(result_list)]
    result_list = result_list[:5]
    items_list = []
    quickReplies = []

    for idx, val in enumerate(result_list):
        items_list.append(
            {
                "title": str(idx+1)+'.'+val[1],
                "description": val[2],
                "imageUrl": val[3],
                "link": {
                    "web": val[4]
                },
            }
        )
        quickReplies.append({
                "label": '축제' +  str(idx+1),
                "action": "block",
                "blockId": "5e50dad192690d00014efe09",
                  "extra": {
                      "id": val[0],
                  }
            }
        )
    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText" : {
                        "text" : "*네이버DataLab. 검색어트렌드 기준 순위입니다."
                    }
                },
                {
                "listCard": {
                    "header": {
                        "title": "인기 축제"
                    },
                    "items": items_list,
                    "buttons": [
                        None if len(another_list) == 0 else {
                            "label": "더보기",
                            "action": "block",
                            "blockId": "5eccb6eb7a9c4b00010632ed",
                            "extra": {
                                "another_list" : another_list,
                            }
                        }
                    ]
                }
            }
            ],
            "quickReplies": quickReplies
        }
    }
    return dataSend

def keyword_place_ui(datalist, keyword):
    items_list = []
    for obj in datalist[:5]: #지역마다 추가
        items_list.append(
            {
                "title": obj['상호명'],
                "description": obj['주소'],
                "link": {
                    "web": obj['url']
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
                        "title": "반경 5km 내"+keyword +"😊"
                    },
                    "items": items_list,
                    # "buttons": [
                    #     {
                    #         "label": "지도로 보기",
                    #         "action": "webLink",
                    #         "webLinkUrl" : "daummaps://search?q=카페&p=" + str(datalist[0]) + "," + str(datalist[1])
                    #     },
                    #     None if len(cafe_list[5:len(cafe_list)]) == 0 else {
                    #         "label": "더보기",
                    #         "action": "block",
                    #         "blockId": "5e7077b22d3cd0000121a040",
                    #         "extra": {
                    #             "type":"cafe",
                    #             "another_list" : cafe_list[5:len(cafe_list)],
                    #             "datalist": datalist
                    #         }
                    #     }
                    # ]
                }
                }
            ]
        }
    }
    return dataSend

def word2vec_recommed_ui(title_arr, sim_obj_list):
    btn_list = []
    title = ' '.join(title_arr)
    for v in sim_obj_list:
        btn = {
                "label": v['word'],
                "action": "block",
                "blockId": "5e4feb4e8192ac00015843f1",
                 "extra": {
                     "another_festa_list": v['festa_list'],
                     "word": v['word']
                }
            }
        btn_list.append(btn)
    send_data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "현재 "+ title +"에 대한 축제는 없나봐😭 조건에맞는 비슷한 것들에 대한 축제는 있는데 이건 어때?"
                    }
                }
            ],
            "quickReplies": btn_list
        }
    }
    return send_data
