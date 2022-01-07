import requests
import csv
#import urllib.request
import sqlite3
from bs4 import BeautifulSoup

def readPageWithSoup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def readColumnTitle(titles):
    for idx, title in enumerate(titles):
        header_data.append(title.get_text().strip())

def writeCsv(fileName, items):
    with open(fileName + ".csv", "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, delimiter=",", quotechar="'", quoting=csv.QUOTE_ALL)
        # title write in file
        wr.writerow(header_data)

        cnt = 0
        rec = ['', '', '', '', '', '', '', '', '', '', '', '']
        for item in items[1:-1]:
            td = item.get_text().strip()
            if td != "":
                # needs special chars (, % ...) filtering
                rec[cnt] = td.replace(",", "")
                if cnt == 11:
                    wr.writerow(rec)
                    cnt = 0
                    continue
                cnt += 1

    print(fileName + " 작성 완료...")

def readCsv(fileName):
    with open(fileName + ".csv", "r", encoding="utf-8") as f:
        lines = csv.reader(f)
        for item in lines:
            stock_data.append(item)

def createTable(dbName, tableName):
    dbconn = sqlite3.connect(dbName)
    dbcursor = dbconn.cursor()

    dbcursor.execute("drop table if exists " + tableName)
    dbconn.commit()

    #1.kospi: N    종목명    현재가    전일비    등락률    거래량    거래대금    매수호가    매도호가    시가총액    PER    ROE
    #2.kosdaq: "
    #3.검색순위:'순위','종목명','검색비율','현재가','전일비','등락률','거래량','시가','고가','저가','PER','ROE'
    sql = "create table if not exists " + tableName
    if tableName == "lastsearch":
        sql += " (rank integer, sname text, srate text, cprice integer, ppre integer, udrate text, trea integer, \
                       trprice integer, hprice integer, lprice integer, per text, roe text)"
    else:
        sql += " (rank integer, sname text, cprice integer, ppre integer, udrate text, trea integer, \
               trprice integer, bprice integer, sprice integer, tprice integer, per text, roe text)"

    dbcursor.execute(sql)
    dbconn.commit()
    dbcursor.close()
    dbconn.close()

def insertIntoTable(dbName, fileName):
    dbconn = sqlite3.connect(dbName)
    dbcursor = dbconn.cursor()

    # N    종목명    현재가    전일비    등락률    거래량    거래대금    매수호가    매도호가    시가총액    PER    ROE
    sql = "insert into " + fileName + " values (:rank, :sname, :cprice, :ppre, :rdrate, :trea, \
          + :trprice, :bprice, :sprice, :tprice, :per, :roe)"

    with open(fileName + ".csv", "r", encoding="utf-8") as f:
        lines = csv.reader(f, delimiter=",", quotechar="'")
        flag = True
        for line in lines:
            if flag:
                flag = False
                continue
            #print(line)
            dbcursor.execute(sql, line)
    dbconn.commit()
    print(fileName + " Table 입력 완료 ...")

    dbcursor.close()
    dbconn.close()

def displayFromTable(dbName, fileName):
    dbconn = sqlite3.connect(dbName)
    dbcursor = dbconn.cursor()

    dbcursor.execute("select * from " + fileName)
    recs = dbcursor.fetchall()
    print("="*120)
    if fileName == "lastsearch":
        print("순위  종 목 명                 검색비율        현재가       전일비    등락률    거  래  량   시  가    고  가   저  가     PER     ROE")
        print("=" * 120)
        for rec in recs:
            print(f"{rec[0]:^5} {rec[1]:<20} {rec[2]:<10} {rec[3]:>10,} {rec[4]:>8,} {rec[5]:>8} {rec[6]:>10,} {rec[7]:>8,} {rec[8]:>8,} {rec[9]:>8,} {rec[10]:7} {rec[11]:^7}")
    else:
        print("순위\t 종 목 명\t\t\t 현재가\t 전일비\t 등락률\t 거래량\t 거래대금\t 매수호가\t 매도호가\t 시가총액\t PER\t ROE")
        print("=" * 120)
        for rec in recs:
            print(f"{rec[0]:^5} {rec[1]:<20} {rec[2]:>10,} {rec[3]:>7} {rec[4]:>8} {rec[5]:>10,} {rec[6]:>10,} {rec[7]:>8,} {rec[8]:>8,} {rec[9]:>10,} {rec[10]:^7} {rec[11]:^7}")


    print("="*120)
    dbcursor.close()
    dbconn.close()

def getMenu():
    while True:
        print("1. KOSPI 거래 상위 100 종목 \n2. KOSDAQ 거래 상위 100 종목\n3. 검색 상위 종목\n")
        menu = input(" 메뉴 선택 : ")
        if menu == "1" or menu == "2" or menu == "3":
            return menu
        elif menu == "0":
            break

if __name__ =="__main__":
    header_data = [] # ['','','','','','','','','','','','']
    stock_data = [] # ]
    fileName = "lastsearch"

    menu = getMenu()

    #createTable("stock.db", fileName)

    # 거래 상위 100(kospi, kosdaq : sosok=0/1), 검색 상위 30,
    # url = "https://finance.naver.com/sise/sise_quant.naver?sosok=0"
    # url = 'https://finance.naver.com/sise/lastsearch2.naver'
    if menu == "1" or menu == "2":
        # csv, table 이름 생성
        fileName = "sosok" + menu
        # url 생성 후 BeautifulSoup으로 읽기
        sosok = int(menu) - 1
        url = "https://finance.naver.com/sise/sise_quant.naver?sosok=" + str(sosok)
        soup = readPageWithSoup(url)

        # soup 에서 th tag의 text(column name) 만 읽어 header_data[]에 저장
        table_html = soup.select_one("div.box_type_l")
        readColumnTitle(table_html.find("table", {"class":"type_2"}).find_all("th"))

    elif menu == "3":
        url = 'https://finance.naver.com/sise/lastsearch2.naver'
        soup = readPageWithSoup(url)

        table_html = soup.select_one("div.box_type_l")
        readColumnTitle(table_html.find("tr", {"class":"type1"}).find_all("th"))
    else:
        exit()

    # td tag 로 시작하는 값들 읽어서 처리 후 csv 파일에 저장
    writeCsv(fileName, table_html.find_all("td"))

    # Table DROP & CREATE
    createTable("stock.db", fileName)

    # table에 insert
    insertIntoTable("stock.db", fileName)
    input("\nEnter 키를 누르세요...")
    # db에서 읽어 화면에 표시
    displayFromTable("stock.db", fileName)