
class Ui:
    def none_festa_list_ui(self, word):
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

    def festa_list_ui(self, festa_list, another_festa_list, word):
        item_list = []
        btn_list = []
        i = 0
        for v in festa_list:
            i += 1
            item = {
                       "title": v[2],
                       "description": '' if v[10]=='null' else  v[10], #만약 null 이면 빈값
                       "imageUrl": v[11],
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
                                "title": word+'에 대한 축제 리스트 입니다.',
                                "imageUrl": "http://k.kakaocdn.net/dn/xsBdT/btqqIzbK4Hc/F39JI8XNVDMP9jPvoVdxl1/2x1.jpg"
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

    def festa_description(self, db_obj):
        desc = "기간 : " + db_obj[6] + " ~ " + db_obj[6] + "\n" \
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
                    }
                ]
            }
        }
        return dataSend
