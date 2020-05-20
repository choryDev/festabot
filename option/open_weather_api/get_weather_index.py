from datetime import datetime, timedelta
import pandas as pd

def getIndexList(startDate, endDate, currentDate):
    startDate = datetime.strptime(str(startDate),"%Y-%m-%d")
    endDate = datetime.strptime(str(endDate),"%Y-%m-%d")
    
    festIdx = pd.date_range(start=startDate, end=endDate) #축제 날짜 정제
    festset = set(festIdx.strftime("%Y%m%d").tolist()) #정제 후 set으로 변환

    currentDate = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0) #현재날짜
    afterDate = currentDate+timedelta(days=7) #Api 호출 최대날짜

    apiIdx = pd.date_range(start=currentDate, end=afterDate)
    apiSet = set(apiIdx.strftime("%Y%m%d").tolist())

    apiIdxList = []
    for i in range(8):
        apiIdxList.append(i)
    print(apiIdxList)

    idxStart = (startDate - currentDate).days
    idxAmount = idxStart+len(festIdx.strftime("%Y%m%d").tolist())

    festIdxList = []
    for i in range(idxStart, idxAmount):
        festIdxList.append(i)

    print(festIdxList)

    return sorted(set(apiIdxList) & set(festIdxList))