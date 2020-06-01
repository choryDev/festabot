import numpy as np # linear algebra
import pandas as pd
from konlpy.tag import Okt
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import tensorflow as tf
MAXLEN = 30
NUM_WORDS = 300

okt = Okt()
stop_word = []
token_tag = ["Noun", "Verb", "Determiner"]

path = "/home/ubuntu/festabot/option/rnn_option"

global model
model = load_model(path+'/rnn_model/option_classification_model.h5')
df=pd.read_csv(path+"/category_sentence.csv", delimiter=',', encoding='utf-8')
global graph
graph = tf.get_default_graph()

sentence_value = [" ".join(["".join(w) for w, t in okt.pos(a) if t in token_tag and w not in stop_word]) for a in df['sentence'].values]

tokenizer = Tokenizer(num_words=NUM_WORDS, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~')
tokenizer.fit_on_texts(sentence_value)

def rnn_predict(sentence):
    with graph.as_default():
        new_complaint = sentence
        new_complaint = [" ".join(["".join(w) for w, t in okt.pos(new_complaint) if t in token_tag and w not in stop_word])]
        seq = tokenizer.texts_to_sequences(new_complaint)
        padded = pad_sequences(seq, maxlen=MAXLEN)
        pred = model.predict(padded)
        labels = ['날씨', '맛집', '연관', '인기', '주소', '주차', '카페']
        print(labels)
        print(pred[0], labels[np.argmax(pred)])
        return pred[0], labels[np.argmax(pred)]