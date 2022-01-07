from bs4 import BeautifulSoup
import urllib.request as MYURL

# BeautifulSoup 사용 방법 1
# jURL = "http://rss.joins.com/joins_news_list.xml"
# response = MYURL.urlopen(jURL)
# soup = BeautifulSoup(response, "html.parser")
#
# print(soup)
# print("="*60)
#
# with open("sample.html", "w") as f:
#     f.write(soup.prettify())
#
# for item in soup.find_all("item"):
#     print("title : ", item.title.string)
#     print("description : ", item.description.string)
#     print("pubdate : ", item.pubdate.string)
#     print("-"*60)

# Bugs Music에서 Daily Ranking 1~100 가져오기 실습 #1
# artist = []
# album = []
# s_date = input("순의 검색할 날짜를 8자리로 입력하세요 [ex : 20060922 ~ 20211229] : ")
#
# URL = "https://music.bugs.co.kr/chart/track/day/total?chartdate=" + s_date
# response = MYURL.urlopen(URL)
#
# soup = BeautifulSoup(response, "html.parser")
#
# #for item in soup.find_all(name="p", attrs={"class:'ranking'"}):
# for idx, item in enumerate(soup.find_all("p", {"class":"title"})):
#     album.append(item.a.string)
#     #print(idx, item.a.string)
#
# for idx, item in enumerate(soup.find_all("p", {"class":"artist"})):
#     artist.append(item.a.string)
#     #print(idx, item.a.string)
#
# f = open("rank.txt", "w", encoding="utf-8")
#
# for idx in range(0, 100):
#     f.writelines(s_date + "," + str(idx + 1) + "," + artist[idx] + "," + album[idx] + "\n")
#
# f.close()

# Bugs 실습 #2
f = open("rank.txt", "wt", encoding="utf-8")
search_day = input("순위 검색할 닐짜를 입력 하세요 : ")
bUrl = "https://music.bugs.co.kr/chart/track/day/total?chartdate=" + search_day
url = MYURL.urlopen(bUrl)
soup = BeautifulSoup(url, "html.parser", from_encoding="utf8")

artists = []
artistRank = 0
titles = []
titleRank = 0

try:
    for link1 in soup.find_all(name="p", attrs={"class":"artist"}):
        try:
            artist = link1.a.get_text()
            #artist = link1.a.string
            #artist = link1.find("a").text
            artists.append(artist)
            artistRank += 1
        except AttributeError as artistError: # 가수 데이터가 존재하지 않을 경우 a tag가 없음
            artist = "N/A"
            artists.append(artist)
            artistRank += 1

    for link1 in soup.find_all("p", attrs={"class":"title"}):
        try:
            title = link1.a.get_text()
            titles.append(title)
            titleRank += 1
        except AttributeError as titleError: # 곡 데이터 없을 경우 a tag 없음
            title = "N/A"
            titles.append(title)
            titleRank += 1

    for i in range(0,100):
        f.write(str(search_day) + "," + str(i+1) + "," + artists[i] + "," + titles[i] + "\n")
except AttributeError as e: # p tag 없을 경우 데이터가 없음.
    print(search_day + ": 이 날 데이터가 존재하지 않습니다.")
except IndexError as index: # 페이지 내부에서 100곡이 안되면 인덱스 에러
    print("Index error... ")

f.close()
