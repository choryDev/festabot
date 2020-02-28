from option_class import Option

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
        else:
            print("[SERVER] 재입력바랍니다")