# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.tokenize import sent_tokenize
from konlpy.tag import Okt
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
from keras.callbacks import EarlyStopping
from keras.layers import Dropout
import re

MAXLEN = 30
NUM_WORDS = 300

df=pd.read_csv("./category_sentence.csv", delimiter=',', encoding='utf-8')
#df = df.sample(frac=1).reset_index(drop=True) #열 섞기

df.dtypes

df['label'].nunique()

df['label'].value_counts()

sns.countplot(df['label'])

df.isnull().sum()

space = re.compile('[/(){}\[\]\|@,;]')
symbols= re.compile('[^0-9a-z #+_]')

g=[]

for i in df['sentence']:
    g.append(i)

maxl = max([len(s) for s in g])
print ('Maximum sequence length in the list of sentences:', maxl)

okt = Okt()
stop_word = []
token_tag = ["Noun", "Verb", "Determiner"]
sentence_value = [" ".join(["".join(w) for w, t in okt.pos(a) if t in token_tag and w not in stop_word]) for a in df['sentence'].values]

for a in sentence_value:
    print(a)

tokenizer = Tokenizer(num_words=NUM_WORDS, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~')
tokenizer.fit_on_texts(sentence_value)
word_index = tokenizer.word_index
print('단어 길이 Found %s unique tokens.' % len(word_index))

X = tokenizer.texts_to_sequences(sentence_value)
X = pad_sequences(X, maxlen=MAXLEN)

print(str(X.shape)+'시퀀스 길이')

Y = pd.get_dummies(df['label'],columns=df["label"]).values

# for i in range(358):                  몇번째가 맞는 라벨인지 확인을 하기 위해
#     print(str(i)+'번째 '+ str(Y[i]))

X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.1, random_state = 42)

print(X_train.shape,Y_train.shape)
print(X_test.shape,Y_test.shape)

model=Sequential()
model.add(Embedding(NUM_WORDS,128,input_length=MAXLEN))
model.add(SpatialDropout1D(0.2))
model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(7, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(X_train, Y_train, epochs=32, batch_size=64,validation_split=0.1,callbacks=[EarlyStopping(monitor='val_loss', patience=3, min_delta=0.0001)])

accr = model.evaluate(X_test,Y_test)
print('Test set\n  Loss: {:0.3f}\n  Accuracy: {:0.3f}'.format(accr[0],accr[1]))

model.save('./rnn_model/option_classification_model.h5')

new_complaint='어디가 맛집이야'
new_complaint = [" ".join(["".join(w) for w, t in okt.pos(new_complaint) if t in token_tag and w not in stop_word])]
seq = tokenizer.texts_to_sequences(new_complaint)
padded = pad_sequences(seq, maxlen=MAXLEN)
pred = model.predict(padded)
labels = ['날씨', '맛집', '연관', '인기', '주소', '주차', '카페']
print(pred, labels[np.argmax(pred)])

new_complaint='카페 어디야'
new_complaint = [" ".join(["".join(w) for w, t in okt.pos(new_complaint) if t in token_tag and w not in stop_word])]
seq = tokenizer.texts_to_sequences(new_complaint)
padded = pad_sequences(seq, maxlen=MAXLEN)
pred = model.predict(padded)
labels = ['날씨', '맛집', '연관', '인기', '주소', '주차', '카페']
print(pred, labels[np.argmax(pred)])

new_complaint='주차장 어디'
new_complaint = [" ".join(["".join(w) for w, t in okt.pos(new_complaint) if t in token_tag and w not in stop_word])]
seq = tokenizer.texts_to_sequences(new_complaint)
padded = pad_sequences(seq, maxlen=MAXLEN)
pred = model.predict(padded)
labels = ['날씨', '맛집', '연관', '인기', '주소', '주차', '카페']
print(pred, labels[np.argmax(pred)])

new_complaint='떡갈비집 어디에 있니?'
new_complaint = [" ".join(["".join(w) for w, t in okt.pos(new_complaint) if t in token_tag and w not in stop_word])]
seq = tokenizer.texts_to_sequences(new_complaint)
padded = pad_sequences(seq, maxlen=MAXLEN)
pred = model.predict(padded)
labels = ['날씨', '맛집', '연관', '인기', '주소', '주차', '카페']
print(pred, labels[np.argmax(pred)])

new_complaint='근처에 떡갈비집 어디에 있니'
new_complaint = [" ".join(["".join(w) for w, t in okt.pos(new_complaint) if t in token_tag and w not in stop_word])]
seq = tokenizer.texts_to_sequences(new_complaint)
padded = pad_sequences(seq, maxlen=MAXLEN)
pred = model.predict(padded)
labels = ['날씨', '맛집', '연관', '인기', '주소', '주차', '카페']
print(pred, labels[np.argmax(pred)])

new_complaint='비가 올 확율 얼마나 되나?'
new_complaint = [" ".join(["".join(w) for w, t in okt.pos(new_complaint) if t in token_tag and w not in stop_word])]
seq = tokenizer.texts_to_sequences(new_complaint)
padded = pad_sequences(seq, maxlen=MAXLEN)
pred = model.predict(padded)
labels = ['날씨', '맛집', '연관', '인기', '주소', '주차', '카페']
print(pred, labels[np.argmax(pred)])


new_complaint='나랑 싸울래 시발로마?'
new_complaint = [" ".join(["".join(w) for w, t in okt.pos(new_complaint) if t in token_tag and w not in stop_word])]
seq = tokenizer.texts_to_sequences(new_complaint)
padded = pad_sequences(seq, maxlen=MAXLEN)
pred = model.predict(padded)
labels = ['날씨', '맛집', '연관', '인기', '주소', '주차', '카페']
print(pred, labels[np.argmax(pred)])


