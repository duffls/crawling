import urllib.request
import json
from config import *

# 1. request 할 url 만들기
# url 요청 변수들. query:검색어, display:검색 결과출력건수(default,10.~100까지가능)
# start: 검색 시작위치(최대 1000), sort: 정렬옵션, sim:유사도, date:날짜순
# 검색 카테고리(블로그,뉴스,책,지식in...)에 따라 다름.
search_word = urllib.parse.quote("검색어")
url = "https://openapi.naver.com/v1/search/blog?query=" + search_word   #json

# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + search_word  # xml 결과
request = urllib.request.Request(url)

# 2. 네이버 오픈 API 이용 ID, Secret header에 추가
request.add_header("X-Naver-Clien-Id", client_id)
request.add_header("X-Naver-Clien-Secret", client_secret)

# 3. response 에 request 결과 받기
response = request.urlopen(request)
rescode = response.getcode()

# 4. response.getcode == 200 정상
if (rescode == 200):
    response_body = response.read()
    print(response_body.decode("utf-8"))
else:
    print("Error Code:" + rescode)
