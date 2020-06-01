import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './')))
from region_ota_translater import ota_translater
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from common.common_stopwords import CommonStopwords




obj = CommonStopwords()

def region_translater(word):
    for v in obj.stop_words_region(): #지역이 있는지 체크
        if v in word:
            return v
    for v in obj.stop_words_region_sub(): #시, 군일 경우 매핑
        if v in word:
            key = v
            return obj.stop_words_region_sub_map()[key] #오타 처리
    return ota_translater(word)

def region_check_flg(word):
    for v in obj.stop_words_region_sub()+obj.stop_words_region(): #지역이 있는지 체크
        if v in word:
            flag =  True
    return flag

def region_return(word):
    for v in obj.stop_words_region(): #지역이 있는지 체크
        if v in word:
            return v
    for v in obj.stop_words_region_sub(): #시, 군일 경우 매핑
        if v in word:
            key = v
            return obj.stop_words_region_sub_map()[key]