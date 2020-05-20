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
                   "title": v[2],
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
    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": db_obj[2],
                        "description": desc,
                        "thumbnail": {
                            "imageUrl": db_obj[11]
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
                                "action": "webLink",
                                "webLinkUrl": "https://store.kakaofriends.com/kr/products/1542"
                            },
                            {
                                "label": "전화하기",
                                "action": "phone",
                                "phoneNumber": "354-86-00070"
                            },
                            {
                                "label": "공유하기",
                                "action": "share"
                            }
                        ]
                    }
                },
                {
                    "simpleText" : {
                        "text" : "다른 축제를 검색하시려면 '나가기'라고 입력하시거나 아래 '나가기'버튼을 눌러주세요."
                    }
                }
            ],
            "quickReplies":[
                {
                    "label": '나가기',
                    "action": "message",
                    "messageText": '나가기'
                }
            ]
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
                    }#,
                    #{
                    #"action": "message",
                    #"label": "카드형으로 검색",
                    #"messageText" : "카드형으로 검색"
                    #}
                ]
                }
            }
            ]
        }
    }
    return dataSend

def weather_ui(start_date, end_date, weatherDBlist, placeXY):
    from datetime import datetime, timedelta
    import os, sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../option/open_weather_api/')))
    from get_openweather_api import get_weekly_weather
    from weather_condition_dic import weather_cond_dic as wthrCondD
    from get_weather_index import getIndexList

    current_date = (datetime.now()+timedelta(hours=9)).replace(hour=0,minute=0,second=0,microsecond=0) #오늘 날짜 #서버시간은 미국기준이라 9시간더함

    print("시작날짜", start_date, "- 금일 날짜", current_date, '=', (start_date-current_date).days)
    
    if (start_date - current_date).days > 7: #축제 시작일이 금일을 기준으로 openWeather 최대 예보일(금일이후 7일)을 넘어갈 때
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
                            "text": str(start_date.month) + "월 " + str(weatherDBlist[0][0]) + "의 평년 날씨는 " + str(weatherDBlist[0][start_date.month]) + "입니다."
                        }
                    }
                ]
            }
        }
    else: 
        weekly_weather = get_weekly_weather(placeXY)

        fest_index = getIndexList(start_date, end_date, current_date)
        print(fest_index)
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                    "listCard": {
                        "header": {
                            "title": "날씨"
                        },
                        "items": [
                            {
                                "title" : str(datetime.fromtimestamp(weekly_weather[0]['dt']).month) + "/" + str(datetime.fromtimestamp(weekly_weather[0]['dt']).day) + " " + str(wthrCondD[int(weekly_weather[0]['weather'][0]['id'])]),
                                "description" : str(weekly_weather[0]['temp']['max'])+"°C/" + str(weekly_weather[0]['temp']['min'])+"°C",
                                "imageUrl" : "http://openweathermap.org/img/wn/" + str(weekly_weather[0]['weather'][0]['icon']) + "@2x.png"
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
            # "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg",
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
                        "title": "추천 맛집"
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
                # "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg",
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
                        "title": "추천 카페"
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