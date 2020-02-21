from flask import Flask, request, jsonify
from Find_purpose import Find_purpose
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
    req = req['userRequest']
    content = req['utterance']
    user = req['user']['id']

    dataSend = Find_purpose(content).find_purpose_first()

    return jsonify(dataSend)

@app.route('/festa_info', methods=['POST'])
def FestaInfo():
    req = request.get_json()
    print(req)
    req = req['userRequest']
    content = req['utterance']
    user = req['user']['id']

    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": content
                    }
                }
            ]
        }
    }
    return jsonify(dataSend)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
