
class Ui:
    def festa_list_ui(self, festa_list, another_festa_list, word):
        item_list = []
        btn_list = []
        i = 0
        for v in festa_list:
            i += 1
            item = {
                       "title": v[2],
                       "description": v[10],
                       "imageUrl": v[11],
                       "link": {
                           "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
                       },
                   },
            btn = {
                        "label": i + '번 축제',
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
                                    }
                                }]
                        }
                    }
                ],
                "quickReplies": btn_list
            }
        }
        return send_data