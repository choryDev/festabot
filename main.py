
from flask import Flask, request, jsonify
import sys
from option_class import Option
app = Flask(__name__)


# @app.route('/keyboard')
# def Keyboard():
#     dataSend = {
#     }
#     # return jsonify(dataSend)

@app.route('/message', methods=['POST'])
def Message():
    content = request.get_json()
    content = content['userRequest']
    return jsonify(Option(1).get_addr())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)