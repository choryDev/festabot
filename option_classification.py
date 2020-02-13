from option_class import Option

class Optionclassification:
    def __init__(self, requset_obj):
        self.requset_obj = requset_obj
        self.sentence = requset_obj['userRequest']['utterance']

    def option_classification(self):
        if self.sentence == "주차장":
            return Option(self.requset_obj).get_parkinglot()
        elif self.sentence == "날씨":
            print("weather")
        elif self.sentence == "주소":
            return Option(self.requset_obj).get_addr()
        else:
            print("재입력")