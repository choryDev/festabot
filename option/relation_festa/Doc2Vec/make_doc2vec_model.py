import sys, os, argparse
from gensim.models import Doc2Vec, ldamulticore
from gensim.models.doc2vec import TaggedDocument

from supervised_nlputils import get_tokenizer

class Doc2VecInput:

    def __init__(self, fname, tokenizer_name="mecab"):
        self.fname = fname
        self.tokenizer = get_tokenizer(tokenizer_name)

    def __iter__(self):
        with open(self.fname, encoding='utf-8') as f:
            for line in f:
                try:
                    sentence, festa_id = line.strip().split("\u241E")
                    tokens = self.tokenizer.morphs(sentence)
                    tagged_doc = TaggedDocument(words=tokens, tags=[festa_id])
                    yield tagged_doc
                except:
                    continue

def make_save_path(full_path):
    model_path = '/'.join(full_path.split("/")[:-1])
    if not os.path.exists(model_path):
       os.makedirs(model_path)


def doc2vec(corpus_fname, output_fname):
    make_save_path(output_fname)
    corpus = Doc2VecInput(corpus_fname)
    model = Doc2Vec(corpus, vector_size=100)
    model.save(output_fname)

corpus_fname = '/home/ubuntu/festabot/option/relation_festa/Doc2Vec/dataset/naver_doc2vec_dataset2020.03.01.txt'
output_fname = '/home/ubuntu/festabot/option/relation_festa/Doc2Vec/model/naver_doc2vec_dataset2020.03.01.model'
doc2vec(corpus_fname, output_fname)



