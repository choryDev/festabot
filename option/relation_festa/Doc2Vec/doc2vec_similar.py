from doc2vec_evaluator import Doc2VecEvaluator

model = Doc2VecEvaluator('/home/ubuntu/festabot/option/relation_festa/Doc2Vec/model/naver_doc2vec_dataset2020.03.23.model')

def most_similar(id):
    return model.most_similar(id, topn=5)

print(most_similar(1037))


