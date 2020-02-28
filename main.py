import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './option')))

from flask import Flask, request, jsonify
from  option_classification import Optionclassification
app = Flask(__name__)



# @app.route('/keyboard')
# def Keyboard():
#     dataSend = {
#     }
#     # return jsonify(dataSend)

@app.route('/message', methods=['POST'])
def Message():
    requset_obj = request.get_json()
    return jsonify(Optionclassification(requset_obj).option_classification())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)