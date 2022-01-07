import urllib.request
import csv
import json
import sqlite3
from config import *

def create_table():
    dbconn = sqlite3.connect("naver.db")
    dbcursor = dbconn.cursor()

    sql = "drop table if exists shop"
    dbcursor.execute(sql)
    sql = "create table if not exists shop (title text,link text, image text, lprice integer, hprice integer," \
          + "mallName text,productId text, brand text, maker text)"
    dbcursor.execute(sql)
    dbconn.commit()

    dbcursor.close()
    dbconn.close()

def insert_rec(results):
    dbconn = sqlite3.connect("naver.db")
    dbcursor = dbconn.cursor()

    sql = "insert into shop values (:title,:link,:image,:lprice,:hprice," \
          + ":mallName,:productId,:brand,:maker)"
    for rec in results:
        dbcursor.execute(sql, rec)

    dbconn.commit()
    dbcursor.close()
    dbconn.close()

def write_csv():
    # db에서 읽어 파일로
    dbconn = sqlite3.connect("naver.db")
    dbcursor = dbconn.cursor()

    res = dbcursor.execute("select * from shop")

    with open("shop.csv", "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        wr.writerow(["title","link","image","lprice","hprice","mallName","productId","brand","maker"])
        wr.writerows(res)

if __name__ == "__main__":
    json_result = []

    sWord = input("쇼핑 검색할 상품 : ")
    query = urllib.parse.quote(sWord)

    #idx = 0
    display = 10
    start = 1
    end = 100

    for start_index in range(start, end, display):
        url = "https://openapi.naver.com/v1/search/shop?query=" + query \
              + "&display=" + str(display) \
              + "&start=" + str(start_index)
    #          + "&sort=" + sort

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)

        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            response_dict = json.loads(response_body.decode("utf-8"))
            #print(response_body.decode("utf-8"))
            items = response_dict["items"]
            for item_index in range(0, len(items)):
                title = items[item_index]['title']
                link = items[item_index]['link']
                image = items[item_index]['image']
                lprice = items[item_index]['lprice']
                if items[item_index]['hprice'] == "":
                    hprice = 0 # items[item_index]['hprice']
                mallName = items[item_index]['mallName']
                productId = items[item_index]['productId']
                brand = items[item_index]['brand']
                maker = items[item_index]['maker']
                json_result.append({'title':title,'link':link,'image':image,'lprice':lprice,'hprice':hprice,'mallName':mallName,'productId':productId,'brand':brand,'maker':maker})
            #print(json_result)
        else:
            print("Error Code:" + rescode)

    create_table()
    insert_rec(json_result)
    write_csv()
