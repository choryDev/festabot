import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './')))
from tf_idf_class import tf_idf_classification

def tfidf_sim(msg):
 #객체 생성자 생성
 tfidf = tf_idf_classification()
 #tfidf 값 구하기
 result, value = tfidf.tf_predict(msg)
 print(result)
 #결과 출력
 if float(value) > 0 :
    if result == "장소":
      return result
    elif result == "주차장":
      return result
    elif result =="날씨":
      return result
    elif result == "맛집":
      return result
    elif result == "카페":
      return result
    elif result == "연관":
      return result
    elif result == "인기" :
      return result
 else : 
    return 0

