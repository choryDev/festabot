import sys, os, requests, random
from collections import defaultdict

from gensim.models import Doc2Vec

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

class Doc2VecEvaluator:

    def __init__(self, model_fname="data/doc2vec.vecs", use_notebook=False):
        self.model = Doc2Vec.load(model_fname)
        self.doc2idx = {el:idx for idx, el in enumerate(self.model.docvecs.doctags.keys())}
        self.use_notebook = use_notebook

    def most_similar(self, festa_id, topn=10):
        list = []
        similar_movies = self.model.docvecs.most_similar(festa_id, topn=topn)
        for festa_id, score in similar_movies:
            obj = {'id': festa_id,
                    'score': score}
            list.append(obj)
        for sim_festa in list:
            print(sim_festa)
        return list
