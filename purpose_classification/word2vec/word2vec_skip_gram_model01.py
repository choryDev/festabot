from word2vec_evalu import WordEmbeddingEvaluator

class Word2vecEvalu:
    def __init__(self):
        self.model = WordEmbeddingEvaluator("/home/ubuntu/festabot/purpose_classification/word2vec/word2vec_model/word2vec",
                               method="word2vec", dim=100, tokenizer_name="mecab")

    def most_similar(self, word, num):
        print(word)
        print(num)
        list = self.model.most_similar(word, topn = num)
        return list

print(Word2vecEvalu().most_similar("희망", 5))