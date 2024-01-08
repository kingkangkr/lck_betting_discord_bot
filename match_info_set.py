import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import os
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

# 경기 정보 (팀 이름)
matches = [
    # 1주차 경기
    ("DRX", "NS"), ("GEN", "T1"), ("BRO", "DK"), ("KT", "FOX"), ("HLE", "DRX"),
    ("T1", "KDF"), ("BRO", "FOX"), ("NS", "GEN"), ("KDF", "HLE"), ("DK", "KT"),
    # 2주차 경기
    ("FOX", "HLE"), ("KDF", "KT"), ("DK", "NS"), ("BRO", "GEN"), ("KT", "T1"),
    ("DRX", "FOX"), ("GEN", "DK"), ("NS", "KDF"), ("DRX", "BRO"), ("HLE", "T1"),
    # 3주차 경기
    ("KDF", "DK"), ("KT", "BRO"), ("T1", "DRX"), ("FOX", "NS"), ("GEN", "KDF"),
    ("DK", "HLE"), ("DRX", "KT"), ("BRO", "T1"), ("NS", "HLE"), ("FOX", "GEN"),
    # 4주차 경기
    ("KT", "GEN"), ("DRX", "KDF"), ("T1", "DK"), ("HLE", "BRO"), ("NS", "KT"),
    ("KDF", "FOX"), ("GEN", "HLE"), ("DK", "DRX"), ("FOX", "T1"), ("NS", "BRO"),
    # 5주차 경기
    ("T1", "NS"), ("HLE", "KT"), ("DK", "FOX"), ("GEN", "DRX"), ("KDF", "BRO"),
    ("HLE", "NS"), ("T1", "KT"), ("GEN", "FOX"), ("DRX", "DK"), ("BRO", "KDF"),
    # 6주차 경기
    ("KDF", "GEN"), ("T1", "FOX"), ("DK", "BRO"), ("NS", "DRX"), ("HLE", "FOX"),
    ("GEN", "KT"), ("KDF", "NS"), ("T1", "BRO"), ("KT", "DK"), ("DRX", "HLE"),
    # 7주차 경기
    ("BRO", "DRX"), ("HLE", "GEN"), ("KDF", "T1"), ("FOX", "KT"), ("BRO", "HLE"),
    ("NS", "DK"), ("T1", "GEN"), ("KDF", "DRX"), ("KT", "NS"), ("FOX", "DK"),
    # 8주차 경기
    ("HLE", "KDF"), ("DK", "T1"), ("FOX", "DRX"), ("BRO", "KT"), ("GEN", "NS"),
    ("T1", "HLE"), ("FOX", "KDF"), ("KT", "DRX"), ("BRO", "NS"), ("DK", "GEN"),
    # 9주차 경기
    ("DRX", "GEN"), ("NS", "T1"), ("KT", "HLE"), ("DK", "KDF"), ("GEN", "BRO"),
    ("NS", "FOX"), ("HLE", "DK"), ("DRX", "T1"), ("FOX", "BRO"), ("KT", "KDF")
]
temp=[]
for week in range(1, 10):  # 9주 동안
    if week == 4:  # 4주차 시작 날짜 조정
        start_date = datetime(2024, 2, 14)

    week_matches = matches[(week-1)*10 : week*10]  # 해당 주의 경기 선택
    for day in range(5):  # 각 주의 5일 동안
        # 이날의 두 경기를 삽입
        for game in range(2):
            team1, team2 = week_matches[day*2 + game]
            match_date = start_date + timedelta(days=day)
            temp.append([team1, team2, match_date.strftime("%Y-%m-%d")])
            insert_match(connection, match_id, team1, team2, match_date.strftime("%Y-%m-%d"))
            # 이곳에 insert_match 함수 호출 로직
            match_id += 1

    start_date += timedelta(weeks=1)  # 다음 주로 이동
    if week == 3:  # 3주차 이후에 추가 날짜 조정
        start_date += timedelta(days=7)  # 설날 휴일을 고려하여 추가 일주일 증가
print(temp)
print(db_password)