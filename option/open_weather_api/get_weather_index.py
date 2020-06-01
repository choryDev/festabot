from datetime import datetime, timedelta
import pandas as pd

def getIndexList(startDate, endDate, currentDate):   
    festIdx = pd.date_range(start=startDate, end=endDate) #축제 날짜 정제

    currentDate = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0) #현재날짜
    afterDate = currentDate+timedelta(days=7) #Api 호출 최대날짜

    apiIdxList = []
    for i in range(8):
        apiIdxList.append(i)

    idxStart = (startDate - currentDate).days
    idxAmount = idxStart+len(festIdx.strftime("%Y%m%d").tolist())

    festIdxList = []
    for i in range(idxStart, idxAmount):
        festIdxList.append(i)

    return sorted(set(apiIdxList) & set(festIdxList))