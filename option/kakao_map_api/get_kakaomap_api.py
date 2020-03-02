import simplejson, requests, sys

def get_restaurant_list():

    url = "https://dapi.kakao.com/v2/local/search/keyword.json?x=127.4714689112&y=36.6441001847&radius=1000" #radius는 미터단위
    apikey = "5e5acc55c8584f36abffe26633c82550"
    query = "맛집"

    r = requests.get( url, params = {'query':query}, headers={'Authorization' : 'KakaoAK ' + apikey })
    js = simplejson.JSONEncoder().encode(r.json())

    place_list = []
    for i in range(10):
        place_list.append( {'상호명' : r.json()["documents"][i]['place_name'], '주소' : r.json()["documents"][i]['address_name'], 
                            'x' : r.json()["documents"][i]['x'], 'y' : r.json()["documents"][i]['y']} )

    # print(place_list[0]) #monitoring용
    return place_list


def get_cafe_list():

    url = "https://dapi.kakao.com/v2/local/search/keyword.json?x=127.4714689112&y=36.6441001847&radius=1000" #radius는 미터단위
    apikey = "5e5acc55c8584f36abffe26633c82550"
    query = "카페"

    r = requests.get( url, params = {'query':query}, headers={'Authorization' : 'KakaoAK ' + apikey })
    js = simplejson.JSONEncoder().encode(r.json())

    place_list = []
    for i in range(10):
        place_list.append( {'상호명' : r.json()["documents"][i]['place_name'], '주소' : r.json()["documents"][i]['address_name'], 
                            'x' : r.json()["documents"][i]['x'], 'y' : r.json()["documents"][i]['y']} )

    return place_list