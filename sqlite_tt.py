import sqlite3
import sungjuk

def display_menu():
      print("1. 성적 입력")
      print("2. 성적 출력")
      print("3. 성적 조회")
      print("4. 성적 수정")
      print("5. 성적 삭제")
      print("6. 프로그램 종료")

def execute_query(sql, flds):
      dbconn =sqlite3.connect("tel.db")
      dbcursor = dbconn.cursor()

      #sql = "insert into sungjuk values(?, ?, ?, ?, ?, ?, ?, ?)"
      dbcursor.execute(sql, (flds,))

      dbconn.commit()

      dbcursor.close()
      dbconn.close()

def student_input():
      data = sungjuk.Sungjuk()

      print()
      data.input_student()
      data.input_sungjuk()
      data.process_sungjuk()

      dbconn =sqlite3.connect("tel.db")
      dbcursor = dbconn.cursor()

      #execute_query(sql, data)
      sql = "insert into sungjuk values(?, ?, ?, ?, ?, ?, ?, ?)"
      dbcursor.execute(sql, (data.hakbun, data.irum, data.kor, data.eng, data.math, data.tot, data.avg, data.grade))

      dbconn.commit()

      dbcursor.close()
      dbconn.close()

def student_search():
      s_num = input("조회할 학번 : ")

      dbconn =sqlite3.connect("tel.db")
      dbcursor = dbconn.cursor()

      #execute_query(sql, data)
      sql = "select * from sungjuk where hakbun=?"
      dbcursor.execute(sql, (s_num,))
      row = dbcursor.fetchone()
      if row:
            print("\n\t\t\t *** 성적표 ***")
            print("학번  이름   국어 영어 수학  총점   평균  등급")
            print("========================================")

            print("%4s %3s %4d %4d %4d %4d %5.2f %3s" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            print("========================================")
      else:
            print(s_num + "은 없는 학번입니다.")

      dbcursor.close()
      dbconn.close()


def student_modify():
      data = sungjuk.Sungjuk()
      s_num = input("수정할 학번 : ")

      dbconn =sqlite3.connect("tel.db")
      dbcursor = dbconn.cursor()

      dbcursor.execute("select count(hakbun) from sungjuk where hakbun=?", (s_num,))
      res = dbcursor.fetchone()
      if res[0] > 0:
            #data.input_student()
            data.input_sungjuk()
            data.process_sungjuk()

            sql = "update sungjuk set kor=?, eng=?, math=?, tot=?, avg=?, grade=? where hakbun=?"
            dbcursor.execute(sql, (data.kor, data.eng, data.math, data.tot, data.avg, data.grade, s_num))
            dbconn.commit()
      else:
            print("수정할 학번이 존재하지 않습니다.")

      dbcursor.close()
      dbconn.close()

def student_delete():

      dbconn =sqlite3.connect("tel.db")
      dbcursor = dbconn.cursor()

      s_num = input("삭제할 학번 : ")
      dbcursor.execute("select * from sungjuk where hakbun=?", (s_num,))
      row = dbcursor.fetchone()

      if row:
            dbcursor.execute("delete from sungjuk where hakbun=?", (s_num,))
            dbconn.commit()
            print(s_num + "학번 학생 정보 삭제 성공")
      else:
            print("삭제할 학번이 없습니다.")

      dbcursor.close()
      dbconn.close()

def student_display():
      t_avg = 0

      print("\n\t\t\t *** 성적표 ***")
      print("학번  이름   국어 영어 수학  총점   평균  등급")
      print("========================================")

      dbconn = sqlite3.connect("tel.db")
      dbcursor = dbconn.cursor()

      dbcursor.execute("select * from sungjuk order by hakbun")
      res = dbcursor.fetchall()

      for row in res:
            t_avg += row[6]
            #data.output_sungjuk()
            print("%4s %3s %4d %4d %4d %4d %5.2f %3s" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

      print("========================================")
      print("\t총 학생수 : [%d]\t 평균 : %5.2f" % (len(res), t_avg / len(res)))
      dbcursor.close()
      dbconn.close()

def create_table():
      dbconn = sqlite3.connect("tel.db")
      dbcursor = dbconn.cursor()

      # Create Table
      sql = "create table if not exists sungjuk (hakbun text primary key, irum text, kor integer, eng integer, math integer," \
            " tot integer, avg real, grade text);"
      dbcursor.execute(sql)
      dbconn.commit()

      # 연결한 cursor, db 연결 객체 반환
      dbcursor.close()
      dbconn.close()

if __name__ == "__main__":
      data = sungjuk.Sungjuk()

      create_table()
      display_menu()

      while True:
            try:
                  menu = int(input("\n메뉴를 입력하세요 : "))
            except:
                  print("\n메뉴를 다시 입력하세요(숫자 오류)")
                  display_menu()
                  continue

            if menu == 1:
                  student_input()
            elif menu == 2:
                  student_display()
            elif menu == 3:
                  student_search()
            elif menu == 4:
                  student_modify()
            elif menu == 5:
                  student_delete()
            elif menu == 6:
                  break
            else:
                  print("메뉴는 1~6사이의 숫자 입니다.")

            print("")
            display_menu()
