import sys, os, requests, random
from collections import defaultdict

from gensim.models import Doc2Vec

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from common.DBconncter import DBconncter

class Doc2VecEvaluator:

    def __init__(self, model_fname="data/doc2vec.vecs", use_notebook=False):
        self.model = Doc2Vec.load(model_fname)
        self.doc2idx = {el:idx for idx, el in enumerate(self.model.docvecs.doctags.keys())}
        self.use_notebook = use_notebook

    def most_similar(self, festa_id, topn=10):
        list = []
        similar_movies = self.model.docvecs.most_similar(str(festa_id), topn=topn)
        for festa_id, score in similar_movies:
            obj = {'id': festa_id,
                    'title': Doc2VecEvaluator.get_movie_title(self, festa_id),
                    'score': score}
            list.append(obj)
        return list

    def get_movie_title(self, festa_id):
        query = 'select title from festival_tb where id = '+festa_id
        title = DBconncter().select_query(query)[0][0]
        return title
