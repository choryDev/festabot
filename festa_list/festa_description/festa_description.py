import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from common.DBconncter import DBconncter
from ui.ui import Ui

class FestaDescription:

    def main(self, req):
        #조회하는 쿼리
        id = req['action']["clientExtra"]["id"]
        user_token = req['userRequest']['user']['properties']['plusfriendUserKey']
        print(user_token+'유저 토큰')
        query = "select * from festival_tb where id = " + str(id)
        db_obj = DBconncter().select_query(query)

        #사용자가 조회 한 것을 넣는 쿼리
        user_token = req['userRequest']['user']['properties']['plusfriendUserKey']
        print(user_token+'유저 토큰')
        query = "INSERT INTO user_tb VALUES (user_token, id, NOW());"
        DBconncter().insert_query(query)

        return Ui().festa_description(db_obj[0])