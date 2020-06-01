import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './')))
from option_class import Option
from rnn_option.rnn_predict import rnn_predict
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from common.DBconncter import DBconncter
from relation_festa.relation_option import RelationOption
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../ui')))
from ui import ui

class Optionclassification:
    def __init__(self, requset_obj):
        self.requset_obj = requset_obj
        self.sentence = requset_obj['userRequest']['utterance']
        self.label = None

    def unnecessary_option(self):
        val = str(self.pred)
        print(val)
        print(val.find('-'))
        return val.find('-')

    def option_classification(self):
        if self.sentence == "나가기":
            user_token = self.requset_obj['userRequest']['user']['properties']['plusfriendUserKey']
            DBconncter().selected_out(user_token)
            return ui.text_message("완료되었습니다. 또 다른 축제를 검색해보세요. 😃")

        self.pred, self.label = rnn_predict(self.sentence)

        if Optionclassification.unnecessary_option(self) == -1 and self.label != "주소": #필요 없는 말을 했을 경우
            return ui.text_message("축제에 대한 정보를 묻는게 아닌거 같은데 다시 말해줘")
        elif self.label == "주소":
            return Option(self.requset_obj).get_addr()
        elif self.label == "주차":
            return Option(self.requset_obj).get_parkinglot()
        elif self.label == "날씨":
            return Option(self.requset_obj).get_weather()
        elif self.label == "맛집":
            return Option(self.requset_obj).get_restaurant()
        elif self.label == "카페":
            return Option(self.requset_obj).get_cafe()
        elif self.label == "연관":
            return RelationOption(self.requset_obj).get_list()
        elif self.label == "인기":
            return Option(self.requset_obj).get_popular_festa()
        else:
            print("[SERVER] 재입력바랍니다")

