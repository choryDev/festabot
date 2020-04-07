import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
import datetime as dt
import json
import requests
import pymysql
import pandas as pd
from sqlalchemy import create_engine


def make_db(data):
 df = pd.DataFrame(data)
 engine = create_engine(
     "mysql+pymysql://admin:" + "123123123" + "@mydb.cstof8mab94c.ap-northeast-2.rds.amazonaws.com:3306/festabot?charset=utf8",
    encoding='utf-8')
# connection = pymysql.connect(host='mydb.cstof8mab94c.ap-northeast-2.rds.amazonaws.com',
#                               user='admin',
#                               password='123123123',
#                               db='festabot')
 conn = engine.connect()
# cursor = connection.cursor()

 df.to_sql(name='festival_tb', con=engine, if_exists='append', index=False)

 engine.dispose()
 #connection.close()

def insta_db(data):
 df = pd.DataFrame(data)
 engine = create_engine(
     "mysql+pymysql://admin:" + "123123123" + "@mydb.cstof8mab94c.ap-northeast-2.rds.amazonaws.com:3306/festabot?charset=utf8",
    encoding='utf-8')
# connection = pymysql.connect(host='mydb.cstof8mab94c.ap-northeast-2.rds.amazonaws.com',
#                               user='admin',
#                               password='123123123',
#                               db='festabot')
 conn = engine.connect()
# cursor = connection.cursor()

 df.to_sql(name='insta_tb', con=engine, if_exists='append', index=False)

 engine.dispose()
 #connection.close()