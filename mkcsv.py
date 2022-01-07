import csv

f = open("output.csv", "w", encoding="utf-8", newline="")

#quotechar = '"' : 데이터를 묶을 문자
#csv.QUOTE_ALL : 모두 사용
wr = csv.writer(f, delimiter=",", quotechar='"') #, quoting=csv.QUOTE_ALL)
wr.writerow((1, "이기자", False))
wr.writerow([2, "김기자", True])

f.close()