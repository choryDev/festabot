from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from konlpy.tag import Okt

okt = Okt()

class Keyword_extractor:

    def __init__(self, festa_pk_list, festa_summary_list):
        self.festa_pk_list = festa_pk_list
        self.festa_summary_list = festa_summary_list
        self.obj = []

    def okt_tokenizer(raw, pos=["Noun"]):
        return [
            word for word, tag in okt.pos(
                raw,
                norm=True,  # normalize 그랰ㅋㅋ -> 그래ㅋㅋ
                stem=True,  # stemming 바뀌나->바뀌다
                )
                if tag in pos
            ]


    def tf_idf_extractor(self):
        vectorizer = TfidfVectorizer(           #tf-idf 적용
            tokenizer=Keyword_extractor.okt_tokenizer,
            sublinear_tf=True)
        sp_matrix = vectorizer.fit_transform(self.festa_summary_list)

        word2id = defaultdict(lambda: 0)

        for idx, feature in enumerate(vectorizer.get_feature_names()):
            word2id[feature] = idx

        for i, sent in enumerate(self.festa_summary_list):
            arr = [{"word":token,"count": sp_matrix[i, word2id[token]]} for token in Keyword_extractor.okt_tokenizer(sent)]
            #arr = list(set(arr))  # 중복제거
            arr = list(map(dict, set(tuple(sorted(v.items())) for v in arr)))
            arr = sorted(arr, key=lambda arr: arr["count"], reverse=True)  # sort by similar

            obj ={
                "id": self.festa_pk_list[i],
                'freq_words': arr[:100]
            }
            self.obj.append(obj)

    def make_obj(self):
        Keyword_extractor.tf_idf_extractor(self)
        return self.obj
