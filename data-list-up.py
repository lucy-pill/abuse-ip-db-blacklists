import mysql.connector
import json
import datetime

def main():
    # 날짜 정보 확인 및 저장
    mydate = datetime.datetime.now()
    p_time = mydate.strftime('%Y%m%d')
    p_year = mydate.strftime('%Y')
    p_month = mydate.strftime('%m')
    p_day = mydate.strftime('%d')

    #MySQL Connection 연결
    db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Dkdldhs*#20",
    database = "blacklists"
    )

    mycursor = db.cursor(prepared=True)

    # Column 값을 대치할 때 사용한는 Parameter Placeholder는 %s
    sql_insert_months = "INSERT INTO abuse_months (CountryCode, Address, LastReportedAt) VALUES (%s, %s, %s)"
    sql_insert_years = "INSERT INTO abuse_years (CountryCode, Address, LastReportedAt) VALUES (%s, %s, %s)"

    with open("C:\\Users\\KSCLOUD\\Desktop\\BOX\\abuse-ip-db-blacklist\\result_%s%s%s.json" % (p_year, p_month, p_day), "r") as outfile:
        data = json.load(outfile)

    # 파싱한 JSON data를 튜플 단위로 리스트에 append
    values_months = []
    values_years = []

    for record in data["data"]:
        # 중복 체크 쿼리
        month_overlap_check_query = "SELECT EXISTS (SELECT * FROM `abuse_months` WHERE Address = '" + record["ipAddress"] + "')"
        year_overlap_check_query = "SELECT EXISTS (SELECT * FROM `abuse_years` WHERE Address = '" + record["ipAddress"] + "')"

        # month 테이블 중복 체크 후 값 저장
        mycursor.execute(month_overlap_check_query)
        month_overlap_check_results = mycursor.fetchall()

        month_overlap_check_temp = month_overlap_check_results[0]

        month_overlap_check_result = month_overlap_check_temp[0]

        # year 테이블 중복 체크 후 값 저장
        mycursor.execute(year_overlap_check_query)
        year_overlap_check_results = mycursor.fetchall()

        year_overlap_check_temp = year_overlap_check_results[0]

        year_overlap_check_result = year_overlap_check_temp[0]

        
        # month 테이블 데이터 삽입
        if month_overlap_check_result == 0:
            values_months.append((record["countryCode"], record["ipAddress"], p_year + "-" + p_month + "-" + p_day))

        elif month_overlap_check_result == 1:
            month_count_check_query = "SELECT ReportedCount FROM `abuse_months` WHERE Address = '" + record["ipAddress"] + "'"
            mycursor.execute(month_count_check_query)
            month_count_check_query_results = mycursor.fetchall()

            month_count_temp = month_count_check_query_results[0]

            month_count = month_count_temp[0]
            month_count = month_count + 1

            month_update_query = "UPDATE `abuse_months` SET ReportedCount = " + str(month_count) + ", LastReportedAt = '" + p_time + "' WHERE Address = '" + record["ipAddress"] + "'"
            mycursor.execute(month_update_query)
            db.commit()

        # year 테이블 데이터 삽입
        if year_overlap_check_result == 0:
            values_years.append((record["countryCode"], record["ipAddress"], p_year + "-" + p_year + "-" + p_day))

        elif year_overlap_check_result == 1:
            year_count_check_query = "SELECT ReportedCount FROM `abuse_years` WHERE Address = '" + record["ipAddress"] + "'"
            mycursor.execute(year_count_check_query)
            year_count_check_query_results = mycursor.fetchall()

            year_count_temp = year_count_check_query_results[0]

            year_count = year_count_temp[0]
            year_count = year_count + 1

            year_update_query = "UPDATE `abuse_years` SET ReportedCount = " + str(year_count) + ", LastReportedAt = '" + p_time + "' WHERE Address = '" + record["ipAddress"] + "'"
            mycursor.execute(year_update_query)
            db.commit()

    # Query execute & commit
    mycursor.executemany(sql_insert_months, values_months)
    print(abs(mycursor.rowcount), "IP was inserted into abuse_months DB.")
    mycursor.executemany(sql_insert_years, values_years)
    print(abs(mycursor.rowcount), "IP was inserted into abuse_years DB.")
    db.commit()

if __name__ == "__main__":
  main()