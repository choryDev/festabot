import simplejson,requests
import sys

def test():
    url = "https://dapi.kakao.com/v2/local/search/keyword.json?y=36.6441001847&x=127.4714689112&radius=1000" #y에 x좌표 넣고, x에 y좌표 넣어야 함 radius는 미터단위

    apikey = "5e5acc55c8584f36abffe26633c82550"
    query = "맛집"
    r = requests.get( url, params = {'query':query}, headers={'Authorization' : 'KakaoAK ' + apikey })
    js = simplejson.JSONEncoder().encode(r.json())

    print(len(r.json()["documents"]), "개 검색 완료")
    for i in range(len(r.json()["documents"])):
        print(i,"\t", r.json()["documents"][i]['address_name'])
        print("\t"+r.json()["documents"][i]['place_name'])