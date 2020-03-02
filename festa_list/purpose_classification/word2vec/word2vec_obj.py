from .word2vec_evalu import WordEmbeddingEvaluator

class Word2vecObj:
    def __init__(self):
        self.model = WordEmbeddingEvaluator("/home/ubuntu/word2vec_model/word2vec",
                               method="word2vec", dim=100, tokenizer_name="mecab")

    def most_similar(self, word, num):
        result_list = []
        list = self.model.most_similar(word, topn = num)
        for word, freq in list:
            result_list.append(word)
        return result_list

# print(Word2vecObj().most_similar("희망", 5))