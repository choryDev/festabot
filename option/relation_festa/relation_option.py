import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './')))
from Doc2Vec.doc2vec_evaluator import Doc2VecEvaluator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from common.DBconncter import DBconncter
from ui import ui

model = Doc2VecEvaluator('/home/ubuntu/festabot/option/relation_festa/Doc2Vec/model/2020.05.29.model')

class RelationOption:
    def __init__(self, requset_obj):
        self.requset_obj = requset_obj
        self.id = 0
        self.user_token = self.requset_obj['userRequest']['user']['properties']['plusfriendUserKey']

    def get_festa_id(self):
        query = "select festa_id from user_tb where user_token = '"+self.user_token+"'"
        self.id = DBconncter().select_query(query)[0][0]

    def most_similar(self):
        RelationOption.get_festa_id(self)
        return model.most_similar(self.id, topn = 10)

    def festa_title(self):
        query = "select title from festival_tb where id = '" + str(self.id) + "'"
        return DBconncter().select_query(query)[0][0]

    def get_list(self):
        sim_list = RelationOption.most_similar(self)
        print(sim_list)
        list = [ obj['id'] for obj in sim_list if obj['score'] > 0.5] #스코어가 0.5 이상일때
        query = "select * from (select * from festival_tb where enddate > sysdate()) A where "
        for id in list[:3]: #최대 3개만 보여
            query += "id = "+str(id)+" or "
        query = query[:len(query)-3]
        db_obj = DBconncter().select_query(query)   #연관된 축제 불러와 쿼리 가져 옴
        title = RelationOption.festa_title(self)    #선택했던 축제의 이름
        return ui.festa_list_ui(db_obj, [], title)  #ui 호출
