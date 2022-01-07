import urllib.request
import re
from requests import get
from bs4 import BeautifulSoup

soso = 0
kospi = "https://finance.naver.com/sise/sise_quant.naver?sosok=0"
kosdaq = "https://finance.naver.com/sise/sise_quant.naver?sosok=1"
title = []

# table "class":"type_2"

# BeautifulSoup 사용 방법 1
# url = kospi
response = urllib.request.urlopen(kospi)
soup = BeautifulSoup(response, "html.parser", from_encoding='utf-8')
# request = get(kospi)
# soup = BeautifulSoup(request.content.decode('euc-kr', 'replace'))

# 타이틀 가져오기
#print(soup.find("table", {"class":"type_2"}).find_all("th"))
for tt in soup.find("table", {"class":"type_2"}).find_all("th"):
    title.append(tt.get_text())

#for tt in soup.select("table > th")
# 거래 상위 100 한 종목씩. table>td class="black~~~면 패스
tags = soup.select('table.type_2 tr')
print(tags)
