import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from common.DBconncter import DBconncter
from ui import ui

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
        DBconncter().insert_festa_desc_query(user_token, id)
        return ui.festa_description(db_obj[0])