import urllib.request
import datetime
import json
import sqlite3
import csv
import re
from config import *

def insert_records(results):
    dbconn = sqlite3.connect("naver.db")
    dbcursor = dbconn.cursor()

    dbcursor.execute("drop table if exists blog")
    sql = "create table if not exists blog (title text, bloggername text, description text, bloggerlink  text," \
          " link text, postdate text)"
    dbcursor.execute(sql)
    # 정규식 [^가-힝0-9a-zA-z<>&]
    # sql = "insert into blog values (?, ?, ?, ?, ?, ?)"
    sql = "insert into blog values (:title, :bloggername, :description, :bloggerlink, :link, :postdate)"

    for rec in results:
        try:
            dbcursor.execute(sql, rec)
        except: # 데이터 중 encoding 오류 데이터 처리
            for reckey in rec:
                rec[reckey] = re.sub("^가-힝0-9a-zA-Z<>&,.?:/#\[\]\\\s", " ", rec[reckey]) # 없는 값 공백으로 대체

    dbconn.commit()
    dbcursor.close()
    dbconn.close()

def write_csv():
    # db에서 읽어서 처리
    dbconn = sqlite3.connect("naver.db")
    dbcursor = dbconn.cursor()

    recs = dbcursor.execute("select * from blog")
    with open("blog.csv", "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        wr.writerow(["title", "bloggername", "description", "bloggerlink", "link", "postdate"])

        wr.writerows(recs)

        #for rec in recs:
            #wr.writerow()
            #wr.writerows(rec)

    dbcursor.close()
    dbconn.close()
    # with open("blog.csv", "w", encoding="utf-8", newline="") as f:
    #     wr = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
    #     wr.writerow([title, bloggername, bloggerlink, description, link, postdate])
    # f = open("movie.csv", "w", encoding="utf-8", newline="")
    # wr = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
    # wr.writerow([title, bloggername, bloggerlink, description, link, postdate])
    # f.close()

def query_execute(sql):
    dbconn = sqlite3.connect("naver.db")
    dbcursor = dbconn.cursor()

    dbcursor.execute(sql)
    dbcursor.execute("delete from blog")

    dbconn.commit()
    dbcursor.close()
    dbconn.close()


# code 1
def get_request_url(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode("utf-8")
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

# code 2
def getNaverSearchResult(sNode, search_text, page_start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % sNode
    parameters = "?query=%s&start=%s&dispaly=%s" % (urllib.parse.quote(search_text), page_start, display)
    url = base + node + parameters
    # print(url)

    retData = get_request_url(url)

    if (retData == None):
        return None
    else:
        return json.loads(retData)

# code 3
def getPostData(post, jsonResult):
    title = post["title"]
    link = post["link"]
    description = post["description"]
    postdate = post["postdate"]
    bloggername = post["bloggername"]
    bloggerlink = post["bloggerlink"]

    jsonResult.append({"title":title, "description":description, "bloggerlink":bloggerlink, "link":link,
                      "postdate":postdate, "bloggername":bloggername})
    return

def main():
    jsonResult = []

    # news, blog, cafearticle
    sNode = "shop"
    search_text = "컴퓨터"
    display_count = 10 # 한번에 읽어올 기사 수

    jsonSearch = getNaverSearchResult(sNode, search_text, 1, display_count)
    print("jsonSearch = ", jsonSearch)

    while ((jsonSearch != None) and (jsonSearch["display"] != 0)):
        for post in jsonSearch["items"]:
            getPostData(post, jsonResult)
        nStart = jsonSearch["start"] + jsonSearch["display"]
        if (nStart > 10):
            break

        jsonSearch = getNaverSearchResult(sNode, search_text, nStart, display_count)

    with open("%s_naver_%s.json" % (search_text, sNode), "w", encoding="utf-8") as outfile:
        retJson = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)

        #ensure_ascii == True면, ascii가 아닌 다른 문자들은 모드 이스케이프 문자로 표현됨
        #이스케이프 문자 : 이스케이프 시퀀스를 따르며, 백슬래시로브터 시작하는 문자
        outfile.write(retJson)

    print("%s_naver_%s.json SAVED" % (search_text, sNode))


    # bloggerlink, bloggername, description, link, postdate, title
    # 읽어온 데이터를 db에 insert
    insert_records(jsonResult)
    write_csv()

if __name__ == "__main__":

    main()
