from datetime import datetime
from create_db import create_connection
from mysql.connector import Error
import os

db_password = os.getenv('db_password')
def get_day_of_week():
    weekday_list = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    weekday = weekday_list[datetime.today().weekday()]
    date = datetime.today().strftime("%Y년 %m월 %d일")
    return f'{date}({weekday})'

def get_time():
    return datetime.today().strftime("%H시 %M분 %S초")

def get_answer(text):
    trim_text = text.replace(" ", "")
    answer_dict = {
        '안녕': '안녕하세요. 키타 이쿠요입니다.',
        '요일': f':calendar: 오늘은 {get_day_of_week()}입니다',
        '시간': f':clock9: 현재 시간은 {get_time()}입니다.',
    }

    if not trim_text:
        return None
    return answer_dict.get(trim_text, None)
def is_user_registered(discord_id):
    connection = create_connection("127.0.0.1", "root", db_password, "lck_betting_db")
    cursor = connection.cursor()

    try:
        # Check if the user exists in the Users table
        query = f"SELECT COUNT(1) FROM Users WHERE DiscordID = {discord_id}"
        cursor.execute(query)
        result = cursor.fetchone()

        # If the count is 0, the user is not registered
        return result[0] > 0

    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        connection.close()
def register_new_user(discord_id, name):
    connection = create_connection("127.0.0.1", "root", db_password, "lck_betting_db")
    cursor = connection.cursor()

    try:
        # 새 사용자를 Users 테이블에 추가하는 쿼리
        # Name 열을 포함하여 업데이트
        query = f"INSERT INTO Users (DiscordID, Name, Points) VALUES ({discord_id}, '{name}', 0)"  # 0은 초기 포인트 값
        cursor.execute(query)
        connection.commit()
        print(f"{discord_id} ({name}) 등록되었습니다.")

    except Error as e:
        print(f"The error '{e}' occurred")
        # 이미 존재하는 사용자일 경우 등의 다른 예외 처리를 추가할 수 있습니다.

    finally:
        cursor.close()
        connection.close()

def get_current_week(test_date=None):
    date_ranges = [
        ("2024-01-15", "2024-01-21"),  # 1주차
        ("2024-01-22", "2024-01-28"),  # 2주차
        ("2024-01-29", "2024-02-04"),  # 3주차
        ("2024-02-12", "2024-02-18"),  # 4주차
        ("2024-02-19", "2024-02-25"),  # 5주차 (R1 결산)
        ("2024-02-19", "2024-02-25"),  # 5주차 (R2)
        ("2024-02-26", "2024-03-03"),  # 6주차
        ("2024-03-04", "2024-03-10"),  # 7주차
        ("2024-03-11", "2024-03-17"),  # 8주차
        ("2024-03-18", "2024-03-24"),  # 9주차
    ]
    today = test_date if test_date else datetime.today().date()
    for idx, (start_date, end_date) in enumerate(date_ranges):
        if datetime.strptime(start_date, "%Y-%m-%d").date() <= today <= datetime.strptime(end_date, "%Y-%m-%d").date():
            return idx + 1  # 주차 반환 (1부터 시작)

    return None  # 해당되는 주차가 없는 경우

def get_matches_for_current_week(week, matches):
    if week is None:
        return "현재 진행 중인 경기가 없습니다."

    start_idx = (week - 1) * 10  # 각 주차별 경기는 10개씩
    end_idx = start_idx + 10
    weekly_matches = matches[start_idx:end_idx]
    if not weekly_matches:  # 해당 주차에 경기가 없는 경우
        return "이번 주는 경기가 없습니다."

    return weekly_matches
def format_matches_by_week(matches, games_per_week=10):
    response = ""
    for week in range(0, len(matches), games_per_week):
        week_number = week // games_per_week + 1
        response += f"{week_number}주차 경기:\n"
        for i in range(week, week + games_per_week):
            match = matches[i]
            response += f"{match[0]} vs {match[1]}\n"
        response += "\n"  # 주차별 경기 사이에 공백 추가
    return response
def is_user_registered(connection, discord_id):
    cursor = connection.cursor()
    # Discord ID를 문자열로 취급하여 쿼리에 적용
    query = f"SELECT * FROM Users WHERE DiscordID = '{discord_id}'"
    cursor.execute(query)
    user = cursor.fetchone()
    return user is not None
def save_bet(discord_id, week, match_id, team_choice, bet_amount, connection):
    try:
        cursor = connection.cursor()
        bet_time = datetime.now()
        query = "INSERT INTO Bets (DiscordID, Week, MatchID, TeamChoice, BetAmount, BetTime) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (discord_id, week, match_id, team_choice, bet_amount, bet_time)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


