# -*- coding: utf-8 -*-
import re
import json
import math
import sys
import os
from datetime import datetime
import requests
import urllib.request
from urllib.request import HTTPError
import urllib.error
import urllib.parse
from bs4 import BeautifulSoup
from textrank import KeysentenceSummarizer
from konlpy.tag import Okt
import time
from WordFrequency import WordFrequency
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from common.DBconncter import DBconncter

# https://developers.naver.com/main/ 사이트에서 어플리케이션 등록
# Naver Development ID/SECRET 필요
naver_client_id = "TOA0cmpmC0DvBhBcrj5A"
naver_client_secret = "8PBNBMq8Xp"

class Naver_blog_clawer:
    def __init__(self, title):
        self.no = 0 # 몇개의 포스트를 저장하였는지 세기 위한 index
        self.all_blog_post_text = []
        self.title = title

    # 블로그 검색 결과 개수를 가져옴
    # 네이버는 최대 1000개의 포스트 결과를 보여주기 때문에 그 이상이면 1000으로 고정
    def get_blog_count(self, query, display):
        encode_query = urllib.parse.quote(query)
        search_url = "https://openapi.naver.com/v1/search/blog?query=" + encode_query
        request = urllib.request.Request(search_url)

        request.add_header("X-Naver-Client-Id", naver_client_id)
        request.add_header("X-Naver-Client-Secret", naver_client_secret)

        response = urllib.request.urlopen(request)
        response_code = response.getcode()

        if response_code is 200:
            response_body = response.read()
            response_body_dict = json.loads(response_body.decode('utf-8'))

            print("Last build date: " + str(response_body_dict['lastBuildDate']))
            print("Total: " + str(response_body_dict['total']))
            print("Start: " + str(response_body_dict['start']))
            print("Display: " + str(response_body_dict['display']))

            if response_body_dict['total'] == 0:
                blog_count = 0
            else:
                blog_total = math.ceil(response_body_dict['total'] / int(display))

                if blog_total >= 200:
                    blog_count = 200
                else:
                    blog_count = blog_total

                print("Blog total: " + str(blog_total))
                print("Blog count: " + str(blog_count))

            return blog_count

    def get_html_tag(self, blog_post_soup, tagnane): #블로그 글 한줄 씩 크롤링 하는 함수
        time.sleep(0.5)
        end_str = "안녕하세요.이 포스트는 네이버 블로그에서 작성된 게시글입니다.자세한 내용을 보려면 링크를 클릭해주세요.감사합니다."
        for blog_post_content in blog_post_soup.select(tagnane):
            blog_post_content = blog_post_content.get_text()
            blog_post_content = str(blog_post_content)
            if(end_str==blog_post_content): #네이버 형식적인 내용 필
                return blog_full_contents
            blog_post_content = re.sub("[^가-힣1-9 ]", "", blog_post_content)
            if(blog_post_content=="" or blog_post_content==" " ):
                continue
            if len(blog_post_content) > 25:
                self.all_blog_post_text.append(blog_post_content)

    # 블로그의 내용을 가져오는 함수
    def get_blog_post(self, query, display, start_index, sort):
        response_code = 0
        encode_query = urllib.parse.quote(query)
        search_url = "https://openapi.naver.com/v1/search/blog?query=" + encode_query + "&display=" + str(
            display) + "&start=" + str(start_index) + "&sort=" + sort
        
        request = urllib.request.Request(search_url)

        request.add_header("X-Naver-Client-Id", naver_client_id)
        request.add_header("X-Naver-Client-Secret", naver_client_secret)
        print('###############################################################################################################')
        try:
            response = urllib.request.urlopen(request)
            response_code = response.getcode()
        except HTTPError as e:
            code = e.getcode()
            print(code)

        if response_code is 200:
            response_body = response.read()
            response_body_dict = json.loads(response_body.decode('utf-8'))
            for item_index in range(0, len(response_body_dict['items'])):
                try:
                    remove_html_tag = re.compile('<.*?>')
                    title = re.sub(remove_html_tag, '', response_body_dict['items'][item_index]['title'])
                    link = response_body_dict['items'][item_index]['link'].replace("amp;", "")

                    self.no += 1
                    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                    print("#" + str(self.no))
                    print("Title: " + title)

                    post_code = requests.get(link)
                    post_text = post_code.text
                    post_soup = BeautifulSoup(post_text, 'lxml')

                    for mainFrame in post_soup.select('iframe#mainFrame'):
                        blog_post_url = "http://blog.naver.com" + mainFrame.get('src')
                        print("크롤링 할 url 내용있음: " + blog_post_url)
                        blog_post_code = requests.get(blog_post_url)
                        blog_post_text = blog_post_code.text
                        blog_post_soup = BeautifulSoup(blog_post_text, 'lxml')
                        Naver_blog_clawer.get_html_tag(self, blog_post_soup, "p") # 내용을 계속 이어 붙인다
                except:
                    item_index += 1

    def main(self):
        #no = 0  # 몇개의 포스트를 저장하였는지 세기 위한 index
        title = self.title
        query = re.sub("[0-9]", '',title)  # 검색을 원하는 문자열로서 UTF-8로 인코딩한다. 제목의 숫자는 없앰
        display = 10  # 검색 결과 출력 건수 지정, 10(기본값),100(최대)
        start = 1  # 검색 시작 위치로 최대 1000까지 가능
        sort = "sim"  # 정렬 옵션: sim(유사도순, 기본값), date(날짜순)

        blog_count = Naver_blog_clawer.get_blog_count(self, query, display)
        for start_index in range(start, blog_count + 1, display):
            Naver_blog_clawer.get_blog_post(self, query, display, start_index, sort)
        return self.all_blog_post_text

query = 'select id, title from (select * from festival_tb where enddate > sysdate())  A'
db_obj = DBconncter().select_query(query)

okt = Okt()
def okt_tokenizer(sent):
    words = okt.pos(sent, join=True)
    words = [w for w in words if ('Noun' in w or 'Determiner' in w or 'Verb' in w or 'Adjective' in w)]
    return words

summarizer = KeysentenceSummarizer(
    tokenize = okt_tokenizer,
    min_sim = 0.3,
    verbose = False
)

obj = []
for id, title in db_obj:
    blog_summary = ""
    sents = Naver_blog_clawer(title).main()  #id, title
    keysents = summarizer.summarize(sents, topk=100)
    for v in keysents:
        blog_summary += v[2]
    val = {
        "id": id,
        'freq_words': WordFrequency().get_noun(blog_summary)  # 단어 빈도수 담는 배열
    }
    obj.append(val)

with open('./word_freq'+datetime.today().strftime("%Y%m%d")+'.json', 'w', encoding='utf-8') as make_file:
    json.dump(obj, make_file, indent="\t")

print("hello world")
