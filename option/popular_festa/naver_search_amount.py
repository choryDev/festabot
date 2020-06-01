# -*- coding: utf-8 -*-
import re, json, os, sys
import urllib.request
import urllib.error
import urllib.parse
import pandas as pd
import seaborn as sns
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from common.DBconncter import DBconncter
from konlpy.tag import *
from common.common_stopwords import CommonStopwords
from datetime import datetime, timedelta

stopword = CommonStopwords()
okt = Okt()

def okt_tokenizer(raw, pos=["Noun", "Determiner", "Number", ]):
    obj = okt.pos(
        raw,
        norm=True,  # normalize 그랰ㅋㅋ -> 그래ㅋㅋ
        stem=True,  # stemming 바뀌나->바뀌다
    )
    list = []
    stopword_list = stopword.stop_words_another() + stopword.stop_words_region() + stopword.stop_words_region_sub()
    for word, tag in obj:
        if tag in pos and word not in stopword_list:  # 형태소 태그, 불용어 처리
            list.append(word)
    return list

def now_festa_list():
    list = [['축제']]

    count_query = 'select COUNT(*) from (select * from festival_tb where enddate > sysdate()) A'
    row_count = (DBconncter().select_query(count_query))[0][0]

    i = 0
    while i < row_count:
        query = 'select title from (select * from festival_tb where enddate > sysdate()) A limit '+str(i)+', 4'  # 기본 쿼리
        db_obj = DBconncter().select_query(query)
        row_list = [ re.sub('[0-9]+', '', obj[0]) for obj in db_obj]
        print(row_list)
        if len(row_list) == 4: list.append(row_list)
        i +=4

    return list

def datalab_api(keywords):

    #데이터랩 api
    naver_client_id = "TOA0cmpmC0DvBhBcrj5A"
    naver_client_secret = "8PBNBMq8Xp"

    url = "https://openapi.naver.com/v1/datalab/search"

    keywordsGroups = []
    keywordsGroups.append({"groupName": str(keywords[0]), "keywords": ['축제', '이벤트', '페스티벌', '행사', '프로그램']})
    for i in range(4):
        print(str(keywords[i+1]))
        print(okt_tokenizer(str(keywords[i+1])))
        keyword_list = okt_tokenizer(str(keywords[i+1]))[:5]
        if len(keyword_list) == 0:
            keyword_list = [str(keywords[i+1])]
        keywordsGroups.append({"groupName": str(keywords[i+1]), "keywords": [str(keywords[i+1])]})

    body = {
        "startDate": str((datetime.now()+timedelta(days=-2)).strftime("%Y-%m-%d")),
        "endDate" : str((datetime.now()+timedelta(days=-1)).strftime("%Y-%m-%d")),
        "timeUnit" : "date",
        "keywordGroups" : keywordsGroups,
    }
    body = json.dumps(body)

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", naver_client_id)
    request.add_header("X-Naver-Client-Secret", naver_client_secret)
    request.add_header("Content-Type", "application/json")
    response = urllib.request.urlopen(request, data=body.encode("utf-8"))
    json_obj = json.loads(response.read().decode('utf-8'))

    df = []
    for i in range(len(keywords)):
        if len(json_obj['results'][i]['data']) != 0:
            df_idx = len(df)
            df.append(pd.DataFrame(json_obj['results'][i]['data']))
            df[df_idx].columns = ['기간', str(keywords[i])]

    #데이터프레임 병합
    for i in range(len(df)):
        if i != len(df)-1:
            df[i+1] = df[i].merge(df[i+1], how='outer', on='기간').fillna(0)

    return df[len(df)-1]


#최소-최대 정규화를 적용한 데이터랩 검색량 조회 함수 (무제한)
def datalab_api_list(kw_list):
    print("kwlist====================================\n",kw_list,"\n==================================================\n")
    #df : '축제' 검색량 최소값, 최대값
    df = datalab_api(kw_list[0] + kw_list[1])
    a, b = df.iloc[:,1].min(), df.iloc[:,1].max()

    print('최솟값 '+format(a, '.5f')+'최대값 '+format(b, '.5f'))

    i = 2
    while i < len(kw_list):
        # df1 : '축제' 검색량 최소값, 최대값
        df1 = datalab_api(kw_list[0] + kw_list[i])
        # df1 국립공원 컬럼의 최소값, 최대값
        x, y = df1.iloc[:, 1].min(), df1.iloc[:, 1].max()
        # 최소 - 최대 정규화
        j = 2
        while j < len(df1.columns):
            print(j)
            df1.iloc[:,j] = (df1.iloc[:, j] - x) / (y - x) * (b - a) + a
            j += 1
        df1 = df1.drop(columns=['기간', '축제'])
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print(df1)
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        df = pd.concat([df, df1], axis=1)
        i += 1

    del df['축제'] #축제 column 삭제
    del df['기간']
    df = df.drop(0,0) #0번 row 삭제
    return df


df = datalab_api_list(now_festa_list()) #Main Start

df_dict = df.to_dict()

for key in df_dict.keys(): #key 하나 당 value값이 두개가 된 것을 올바른 values만 다시 삽입
    df_dict[key] = df_dict[key][1]

sorted_df = sorted(df_dict.items(), key=lambda t: t[1], reverse=True) #dict의 key, value를 value 기준으로 내림차순 sorting

# print(json.dump(sorted_df, ensure_ascii=False, indent='\t'))

sorted_df = sorted_df[:40] #리스트 40개로 제한 list [[축제명,스코어],[축제명,스코어]...[축제명,스코어]]
for i in range(40): #스코어 삭제
    sorted_df[i] = sorted_df[i][0] #정렬된 축제명만을 리스트로 삽입

query = 'select title from festival_tb where title like "%' +str(sorted_df[0])    #인기축제40개 쿼리문
for i in range(1,40):                                                                           #
    query = query + '%" or title like "%' + str(sorted_df[i])                                   #
query = query + '%"'                                                                            #
data = DBconncter().select_query(query)
datalist = list(data)
result_list = []

for title in sorted_df: #순서가 바뀐 datalist를 재 sorting하여 result_list에 저장
    for db_title in datalist:
        if title == re.sub('[0-9]+', '', db_title[0]):
                result_list.append(db_title)

for i in range(40):
    result_list[i] = result_list[i][0]

print(result_list)
currentDate = datetime.now().strftime("%Y.%m.%d") #추가 일자

str_fest = ''
columm = 'save_date'
for idx, obj in enumerate(result_list):
    columm_nm = idx+1
    columm += ', rank_' +str(columm_nm)
    str_fest += ', '+'"'+str(obj) + '"'
query = 'insert into popular_festa('+columm+') values("' + str(currentDate) + '"' + str_fest + ')'
print(query)
DBconncter().insert_query(query)
print("Send to DB complete.")
