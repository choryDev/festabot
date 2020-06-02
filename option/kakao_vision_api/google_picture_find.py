import sys
import requests
import base64
import urllib.request
import json
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from common.DBconncter import DBconncter
from ui import ui

client_id = "TOA0cmpmC0DvBhBcrj5A" # 개발자센터에서 발급받은 Client ID 값
client_secret = "8PBNBMq8Xp" # 개발자센터에서 발급받은 Client Secret 값

path = '/home/ubuntu/festabot/festa_list/purpose_classification/word_freq_dir/'
# with open('word_freq_dir/word_freq' + str(int(datetime.today().strftime("%Y%m%d"))-1) + '.json', 'r', encoding="utf-8") as f:
with open(path + 'word_freq20200526.json', 'r', encoding="utf-8") as f:
    json_data = json.load(f)

def eng_to_ko_translt(text):
    encText = urllib.parse.quote(text)
    data = "source=en&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        res_obj = json.loads(response_body.decode('utf-8'))
        res_obj = res_obj['message']['result']['translatedText']
        return res_obj
    else:
        print("Error Code:" + rescode)

def detect_labels_uri(uri):         #사진 객체 찾아 주는 함수
    """Detects labels in the file located in Google Cloud Storage or on the
    Web."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image(content=requests.get(uri).content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    label_list = ''
    for label in labels:
        label_list += '!'+ label.description
        print(label.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    if len(labels) == 0 :
        return 0
    else:
        return eng_to_ko_translt(label_list)

def word_pupose(word):
    festa_list = []
    for r in json_data:
        for v in r['freq_words']:  # 단어 들어가는 지만 체크
            if v['word'] == word:   #해당 단어가 있으면 넣음
                obj = {'id' : r['id'],
                       'word' : v['word'],
                       'count' : v['count']}
                festa_list.append(obj)
    festa_list = sorted(festa_list, key=lambda obj: obj['count'], reverse=True)
    return [a['id'] for a in festa_list] #아이디만 뽑아 냄

def picture_find(utterance):
    ui_context = None
    result = detect_labels_uri(utterance)

    if result == 0:
        return ui.text_message("사진에 맞는 축제 못찾겠어")
    else:
        pic_label_list = result
    pic_label_list = pic_label_list.split('!')
    for a in pic_label_list:
        print(a)
    id_list = []
    title = ""

    for pic_obj in pic_label_list:
        id_list += word_pupose(pic_obj)
        title += pic_obj +','
    if(len(id_list) !=0):
        query = 'select * from (select * from festival_tb where enddate > sysdate()) A where '  # 기본 쿼리
        for id in id_list:
            query += "id = " + str(id) + " or "
        print(query)
        db_obj = DBconncter().select_query(query[0:len(query)-3])
        if len(db_obj) == 0:
            ui_context = ui.text_message("사진에 맞는 축제 못찾겠어")
        else:
            ui_context = ui.festa_list_ui(db_obj[0:5], db_obj[5:], title[0:len(title) - 1])
    else:
        ui_context = ui.text_message("사진에 맞는 축제 못찾겠어")

    return ui_context
