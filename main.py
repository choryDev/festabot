from flask import Flask, request, jsonify
from festa_list.festa_description.festa_description import FestaDescription
from festa_list.festa_list import FestaList
from option.option_classification import Optionclassification
from ui import ui
from common.DBconncter import DBconncter
import sys
app = Flask(__name__)

@app.route('/keyboard')
def Keyboard():
    dataSend = {
    }
    return jsonify(dataSend)

@app.route('/message', methods=['POST'])
def Message():
    req = request.get_json()
    user_token = req['userRequest']['user']['properties']['plusfriendUserKey']
    query = "select * from user_tb where user_token = '" + str(user_token)+ "' "
    db_obj = DBconncter().select_query(query)
    dataSend = None
    if len(db_obj) == 0:
        dataSend = FestaList(req).main_func()
    else:
        dataSend = Optionclassification(req).option_classification()
    return jsonify(dataSend)

@app.route('/btn_more_festa_list', methods=['POST'])
def Btn_more_festa_list():
    req = request.get_json()
    other_festa_list = req['action']["clientExtra"]["another_festa_list"]
    word = req['action']["clientExtra"]["word"]
    dataSend = ui.festa_list_ui(other_festa_list[0:5], other_festa_list[5:], word)
    return jsonify(dataSend)

@app.route('/festa_description', methods=['POST'])
def festa_description():
    req = request.get_json()
    dataSend = FestaDescription().main(req)
    return jsonify(dataSend)

@app.route('/option_cafe_more', methods=['POST'])
def option_cafe_more():
    print("hello~")
    return jsonify(dataSend)

@app.route('/option_restaurant_more', methods=['POST'])
def option_restaurant_more():
    print("hello motherfucker")
    return jsonify(dataSend)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
