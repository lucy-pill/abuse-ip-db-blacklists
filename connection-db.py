import mysql.connector
import json

def init():
  #MySQL Connection 연결
  db = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "Dkdldhs*#20",
  database = "blacklists"
  )

  mycursor = db.cursor(prepared=True)

  # 현재 No(INDEX) 최대 값 가져오기
  sql_select = "SELECT max(No) FROM abuse"

  # Column 값을 대치할 때 사용한는 Parameter Placeholder는 %s
  sql_insert = "INSERT INTO abuse (No, ConfidenceScore, CountryCode, Address, LastReportedAt) VALUES (%s, %s, %s, %s, %s)"

  with open("C:\\Users\\KSCLOUD\\Desktop\\BOX\\abuse-ip-db-blacklist\\result.json", "r") as outfile:
    data = json.load(outfile)

  mycursor.execute(sql_select)
  result = mycursor.fetchall()[0][0]

  # Index 값 가져오기
  if result == None:
    id = 1
  else:
    id = result + 1

  # 파싱한 JSON data를 튜플 단위로 리스트에 append
  values = []

  for record in data["data"]:
    values.append((id, record["abuseConfidenceScore"], record["countryCode"], record["ipAddress"], record["lastReportedAt"]))
    id += 1

  # Query execute & commit
  mycursor.executemany(sql_insert, values);
  db.commit()
  print(mycursor.rowcount, "was inserted")

init()