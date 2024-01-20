import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import os
from texts import matches

db_password = os.getenv('db_password')


# 데이터베이스 연결 설정
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


# 경기 정보 삽입 함수
def insert_match(connection, match_id, team1, team2, match_date):
    query = """
    INSERT INTO Matches (MatchID, Team1, Team2, MatchDateTime)
    VALUES (%s, %s, %s, %s);
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query, (match_id, team1, team2, match_date))
        connection.commit()
        print(f"Match {match_id} inserted successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# 연결 생성
connection = create_connection("127.0.0.1", "root", db_password, "lck_betting_db")

# 경기 정보 삽입
start_date = datetime(2023, 1, 17)  # 첫 번째 경기의 날짜
match_id = 1

temp = []
for week in range(1, 10):  # 9주 동안
    if week == 4:  # 4주차 시작 날짜 조정
        start_date = datetime(2024, 2, 14)

    week_matches = matches[(week - 1) * 10: week * 10]  # 해당 주의 경기 선택
    for day in range(5):  # 각 주의 5일 동안
        # 이날의 두 경기를 삽입
        for game in range(2):
            team1, team2 = week_matches[day * 2 + game]
            match_date = start_date + timedelta(days=day)
            temp.append([team1, team2, match_date.strftime("%Y-%m-%d")])
            insert_match(connection, match_id, team1, team2, match_date.strftime("%Y-%m-%d"))
            # 이곳에 insert_match 함수 호출 로직
            match_id += 1

    start_date += timedelta(weeks=1)  # 다음 주로 이동
    if week == 3:  # 3주차 이후에 추가 날짜 조정
        start_date += timedelta(days=7)  # 설날 휴일을 고려하여 추가 일주일 증가
