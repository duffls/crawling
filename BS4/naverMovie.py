from bs4 import BeautifulSoup
import urllib.request as turl
import csv
import sqlite3

def execute_j_query(sql):
    dbconn = sqlite3.connect("movie.db")
    dbcursor = dbconn.cursor()

    #sql = "create table if not exists movie_rank (s_date text, m_rank integer, m_title text, m_rate integer);"
    dbcursor.execute(sql)
    dbconn.commit()

    dbcursor.close()
    dbconn.close()

def query_execute(s_date, rank, title, rate = 0):
    dbconn = sqlite3.connect("movie.db")
    dbcursor = dbconn.cursor()

    sql = "insert into movie_rank values (?, ?, ?, ?)"
    dbcursor.execute(sql, (s_date, str(rank), title, str(rate),))

    dbconn.commit()

    dbcursor.close()
    dbconn.close()

def conn_Url(url):
    res = turl.urlopen(url)
    return BeautifulSoup(res, "html.parser", from_encoding="utf-8")

def get_menu():
    global menu
    global s_date
    global s_page
    global e_page

    mn = input("메뉴 선택 1:조회순 2:평점순(현재상영영화) 3:평점순(모든영화) : ")
    s_date = input("날짜 선택 (ex:20210101) : ")
    if mn =="3":
        s_page = int(input("시작 페이지 : "))
        e_page = int(input("끝 페이지 : "))
    if mn =="1":
        menu = "cnt"
    elif mn == "2":
        menu = "cur"
    elif mn == "3":
        menu = "pnt"

def write_results(menu):
    f = open("movie.csv", "w", encoding="utf-8", newline="")
    wr = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
    for idx in range(1, len(titles)+1):
        if menu == "cnt":
            print('"{0}","{1}","{2}"'.format(s_date, str(s_page * idx), titles[idx-1]))
            wr.writerow([s_date, str(s_page * idx), titles[idx-1]])
            query_execute(s_date, str(s_page * idx), titles[idx-1])
        else:
            # print(s_date, str(((s_page - 1) * 50) + idx), titles[idx-1], points[idx-1])
            print('"{0}","{1}","{2},"{3}""'.format(s_date, str(((s_page - 1) * 50) + idx), titles[idx-1], points[idx-1]))
            wr.writerow([s_date, str(((s_page - 1) * 50) + idx), titles[idx-1], points[idx-1]])
            query_execute(s_date, str(((s_page - 1) * 50) + idx), titles[idx-1], points[idx-1])
    f.close()


if __name__ == "__main__":
    # 조회:cnt, 현재:cur, 평점:pnt
    titles = []
    points = []
    t_url = "https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel="
    s_date = ""
    menu = ""

    s_page = 1
    e_page = 1

    # db 생성
    #sql = "create table if not exists movie_rank (s_date text, m_rank integer, m_title text, m_rate integer);"
    execute_j_query("create table if not exists movie_rank (s_date text, m_rank integer, m_title text, m_rate integer);")
    #sql = "delete from movie_rank"
    execute_j_query("delete from movie_rank")

    # 메뉴 및 조건 입력
    get_menu()

    # 조건 sel 에 메뉴 넣고 date 까지  여기는 동일
    t_url += menu + "&date=" + s_date
    if menu == "cnt":
        soup = conn_Url(t_url)
        for movie in soup.find_all("div", {"class":"tit3"}):
            title = movie.a.get_text()
            titles.append(title)
    elif menu == "cur":
        soup = conn_Url(t_url)
        for movie in soup.find_all("div", {"class":"tit5"}):
            title = movie.a.get_text()
            titles.append(title)
        for movie in soup.find_all("td", {"class":"point"}):
            point = movie.get_text()
            points.append(point)
    elif menu == "pnt":
        for i in range(s_page, e_page + 1):
            t_url += "&page=" + str(i)
            soup = conn_Url(t_url)
            for movie in soup.find_all("div", {"class": "tit5"}):
                title = movie.a.get_text()
                titles.append(title)
            for movie in soup.find_all("td", {"class": "point"}):
                point = movie.get_text()
                points.append(point)

    #write_results(menu)

    # #menu = input("메뉴 선택(1:조회순, 2:평점순(현재상영영화), 3.평점순(모든영화) : ")
    # if menu == "1":
    #     s_date = input("날짜 선택 : ")
    #     s_menu = "cnt"
    #     t_url += s_menu + "&date=" + s_date
    #
    #     # res = turl.urlopen(t_url)
    #     # soup = BeautifulSoup(res, "html.parser", from_encoding="utf-8")
    #     soup = conn_Url(t_url)
    #     for movie in soup.find_all("div", {"class":"tit3"}):
    #         title = movie.a.get_text()
    #         titles.append(title)
    #
    # elif menu == "2":
    #     s_date = input("날짜 선택 : ")
    #     s_menu = "cur"
    #     t_url += s_menu + "&date=" + s_date
    #
    #     # res = turl.urlopen(t_url)
    #     # soup = BeautifulSoup(res, "html.parser", from_encoding="utf-8")
    #     soup = conn_Url(t_url)
    #     for movie in soup.find_all("div", {"class":"tit5"}):
    #         title = movie.a.get_text()
    #         titles.append(title)
    #     for movie in soup.find_all("td", {"class":"point"}):
    #         point = movie.get_text()
    #         points.append(point)
    #
    # elif menu == "3":
    #     s_date = input("날짜 선택 : ")
    #     s_menu = "pnt"
    #     s_page = int(input("시작 페이지 : "))
    #     e_page = int(input("종료 페이지 : "))
    #
    #     for i in range(s_page, e_page+1):
    #         t_url += s_menu + "&date=" + s_date + "&page=" + str(i)
    #
    #         # res = turl.urlopen(t_url)
    #         # soup = BeautifulSoup(res, "html.parser", from_encoding="utf-8")
    #         soup = conn_Url(t_url)
    #         for movie in soup.find_all("div", {"class":"tit5"}):
    #             title = movie.a.get_text()
    #             titles.append(title)
    #
    #         for movie in soup.find_all("td", {"class":"point"}):
    #             point = movie.get_text()
    #             points.append(point)
    #

    f = open("movie.csv", "w", encoding="utf-8", newline="")
    wr = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
    # 파일과 화면의 타이틀 출력

    rank = (s_page - 1) * 50
    for idx in range(1, len(titles)+1):
        if menu == "cnt":
            # 화면출력
            print('"{0}","{1}","{2}"'.format(s_date, str(rank + idx), titles[idx-1]))
            wr.writerow([s_date, rank + idx, titles[idx-1]])
            query_execute(s_date, str(rank + idx), titles[idx-1])
        else:
            # print(s_date, str(((s_page - 1) * 50) + idx), titles[idx-1], points[idx-1])
            print('"{0}","{1}","{2},"{3}""'.format(s_date, str(rank + idx), titles[idx-1], points[idx-1]))
            wr.writerow([s_date, rank + idx, titles[idx-1], points[idx-1]])
            query_execute(s_date, rank + idx, titles[idx-1], points[idx-1])
    f.close()

    # # zip 내장 함수,