import simplejson, requests, sys

def get_restaurant_list(datalist):

    url = "https://dapi.kakao.com/v2/local/search/keyword.json?x=" + str(datalist[1]) + "&y=" + str(datalist[0]) + "&radius=1000" #radius는 미터단위
    apikey = "5e5acc55c8584f36abffe26633c82550"
    query = "맛집"

    r = requests.get( url, params = {'query':query}, headers={'Authorization' : 'KakaoAK ' + apikey })

    place_list = []
    for i in range(len(r.json()["documents"])):
        place_list.append( {'상호명' : r.json()["documents"][i]['place_name'], '주소' : r.json()["documents"][i]['address_name'], 
                            'x' : r.json()["documents"][i]['x'], 'y' : r.json()["documents"][i]['y']} )

    return place_list


def get_cafe_list(datalist):

    url = "https://dapi.kakao.com/v2/local/search/keyword.json?x=" + str(datalist[1]) + "&y=" + str(datalist[0]) + "&radius=1000" #radius는 미터단위
    apikey = "5e5acc55c8584f36abffe26633c82550"
    query = "카페"

    r = requests.get( url, params = {'query':query}, headers={'Authorization' : 'KakaoAK ' + apikey })
    
    place_list = []
    for i in range(len(r.json()["documents"])):
        place_list.append( {'상호명' : r.json()["documents"][i]['place_name'], '주소' : r.json()["documents"][i]['address_name'], 
                            'x' : r.json()["documents"][i]['x'], 'y' : r.json()["documents"][i]['y']} )

    return place_list