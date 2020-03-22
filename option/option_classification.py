import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './')))
from option_class import Option
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from common.DBconncter import DBconncter

class Optionclassification:
    def __init__(self, requset_obj):
        self.requset_obj = requset_obj
        self.sentence = requset_obj['userRequest']['utterance']

    def option_classification(self):
        if self.sentence == "주소":
            return Option(self.requset_obj).get_addr()    
        elif self.sentence == "주차장":
            return Option(self.requset_obj).get_parkinglot()
        elif self.sentence == "날씨":
            return Option(self.requset_obj).get_weather()
        elif self.sentence == "맛집":
            return Option(self.requset_obj).get_restaurant()
        elif self.sentence == "카페":
            return Option(self.requset_obj).get_cafe()
        elif self.sentence == "나가기":
            user_token = self.requset_obj['userRequest']['user']['properties']['plusfriendUserKey']
            DBconncter().selected_out(user_token)
        else:
            print("[SERVER] 재입력바랍니다")