import json

JSON_FILE = "./test.json"
JSON_DATA = {}

def read_json(filename):
    # f = open(filename, "rt")
    # #f = open(filename, "rt", encoding="utf-8")
    # js = json.loads(f.read())
    # f.close()

    # loads(), load() : [json 문자열, json] 파일 을 파이썬 dict형식으로
    # dumps(), dump()  "
    with open(filename, "rt") as f:
        js = json.load(f)
    return js

def proc_json():
    global JSON_FILE
    global JSON_DATA

    JSON_DATA = read_json(JSON_FILE)

    for data in JSON_DATA:
        print(data)
        for item in JSON_DATA[data]:
            print("\t%s:%s" % (item, JSON_DATA[data][item]))
        print()

if __name__ == "__main__":

    proc_json()
