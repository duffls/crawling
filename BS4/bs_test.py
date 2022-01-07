# need install requests package requests :파이썬으로 http호출하는 프로그램 작성시 사용되는 라이브러리
# pip install requests

import requests
from bs4 import BeautifulSoup

url = "https://kin.naver.com/search/list.nhn?query=%ED%8C%8C%EC%9D%B4%EC%8D%AC"

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    print(soup)
else:
    print(response.status_code)
