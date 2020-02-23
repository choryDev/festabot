from flask import Flask, request, jsonify
from purpose_classification.Find_purpose import Find_purpose
from purpose_classification.word2vec.word2vec_obj import Word2vecObj
from festa_list import FestaList
import sys
app = Flask(__name__)

word2vec = Word2vecObj()


@app.route('/keyboard')
def Keyboard():
    dataSend = {
    }
    return jsonify(dataSend)

@app.route('/message', methods=['POST'])
def Message():
    req = request.get_json()
    # req = req['userRequest']
    # content = req['utterance']
    # user = req['user']['id']

    # dataSend = Find_purpose(word2vec).find_purpose_first(content)
    dataSend = FestaList(req).main_func()
    return jsonify(dataSend)

@app.route('/btn_more_festa_list', methods=['POST'])
def Btn_more_festa_list():
    req = request.get_json()
    other_festa_list = req['action']["clientExtra"]["another_festa_list"]
    dataSend = Find_purpose(word2vec).db_query_list(other_festa_list)
    return jsonify(dataSend)

@app.route('/festa_description', methods=['POST'])
def festa_description():
    req = request.get_json()
    other_festa_list = req['action']["clientExtra"]["another_festa_list"]
    content = ""
    dataSend = Find_purpose(word2vec).db_query_list(other_festa_list)
    return jsonify(dataSend)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
