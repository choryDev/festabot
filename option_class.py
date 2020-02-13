import pymysql

host='mydb.cstof8mab94c.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = '123123123'
db = 'festabot'
charset = 'utf8'

class Option:
    def __init__(self, requset_obj):
        self.requset_obj = requset_obj

    def get_addr(self):
        # dataSend = {}
        conn = pymysql.connect(host=host, user = user, 
                       password=password , db=db, charset=charset)

        curs = conn.cursor()

        sql = 'select region, title, address, getX, getY from festival_tb where title = "부산 코믹월드 2020";'
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
                        "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
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
                        "label": "카카오맵 길찾기",
                        "webLinkUrl": "daummaps://route?sp=35.1516077265, 129.1173479525&ep=35.1690700054,129.1359569660&by=FOOT"
                        }
                    ]
                    }
                }
                ]
            }
        }
        return dataSend