import mysql.connector
import json
import datetime

def main():
  mydate = datetime.datetime.now()
  month = str(mydate.strftime("%B"))

  db = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "Dkdldhs*#20",
  database = "blacklists"
  )

  mycursor = db.cursor(prepared=True)

  sql_select = "SELECT * FROM abuse_months"
  
  mycursor.execute(sql_select)
  result = mycursor.fetchall()

  jsonDB = {month : []}

  for data in result:
    jsonDB[month].append({'CountryCode ' : data[1], 'Address' : data[2], 'LastReportedAt' : data[3], 'ReportedCount' : data[4]})

  with open("C:\\Users\\KSCLOUD\\Desktop\\BOX\\abuse-ip-db-blacklist\\abuse_ip_db_%s.json" % (mydate.strftime('%Y%m')), "w") as outfile:
    json.dump(jsonDB, outfile)

if __name__ == "__main__":
  main()