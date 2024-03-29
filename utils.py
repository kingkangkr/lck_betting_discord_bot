from datetime import datetime
from create_db import create_connection
from mysql.connector import Error
import os
import random
from texts import bet_date_ranges
from get_odds_of_matches import odds_list
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
        'ㅎㅇ': '안녕하세요. 키타 이쿠요입니다.',
        '하이': '안녕하세요. 키타 이쿠요입니다.'
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


def add_points(connection, discord_id, amount):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT points FROM Users WHERE DiscordID = %s", (discord_id,))
        user_points = cursor.fetchone()[0]

        new_points = user_points + amount
        cursor.execute("UPDATE Users SET points = %s WHERE DiscordID = %s", (new_points, discord_id))
        connection.commit()

        return True, new_points  # Points added successfully
    except Exception as e:
        print(f"An error occurred: {e}")
        return False, None  # Indicate failure


def deduct_points(connection, discord_id, amount):
    cursor = connection.cursor()
    cursor.execute("SELECT points FROM Users WHERE DiscordID = %s", (discord_id,))
    user_points = cursor.fetchone()[0]

    if amount > user_points:
        return False, user_points  # Not enough points

    new_points = user_points - amount
    cursor.execute("UPDATE Users SET points = %s WHERE DiscordID = %s", (new_points, discord_id))
    connection.commit()

    return True, new_points  # Points deducted successfully


def get_user_points(connection, discord_id):
    cursor = connection.cursor()
    cursor.execute("SELECT points FROM Users WHERE DiscordID = %s", (discord_id,))
    user_points = cursor.fetchone()[0]
    return user_points
def get_all_bets_by_week(connection, week):
    cursor = connection.cursor()

    # 주어진 week에 대한 모든 베팅 정보를 id별로 정렬하여 조회
    query = """
    SELECT DiscordID, TeamChoice, BetAmount FROM Bets
    WHERE Week = %s
    ORDER BY DiscordID
    """
    cursor.execute(query, (week,))

    bets = cursor.fetchall()

    bets_dict = {}
    for discord_id, teamchoice, betamount in bets:
        if discord_id not in bets_dict:
            bets_dict[discord_id] = []
        bets_dict[discord_id].append(f"{teamchoice} {betamount}")

    return bets_dict
def calculate_betting_results(match_results, odds_list, bets_dict):
    winnings = {}
    result = {}
    for discord_id, bets in bets_dict.items():
        win_num = 0
        total_winning = 0
        for i, bet in enumerate(bets):
            team_choice, bet_amount = map(int, bet.split())
            if team_choice == match_results[i]:
                # 승리한 팀의 배당률을 찾아 베팅 금액에 곱하기
                odds = odds_list[i][team_choice - 1]
                total_winning += bet_amount * odds

                win_num += 1


        winnings[discord_id] = total_winning
        result[discord_id] = win_num
    return winnings, result
def get_users_ranked_by_points(connection):
    cursor = connection.cursor()
    query = "SELECT Name, points FROM Users ORDER BY points DESC"
    cursor.execute(query)
    return cursor.fetchall()
def get_bet_week_number(date_ranges, test_date=None):
    today = test_date if test_date else datetime.now().date()

    for idx, (start, end) in enumerate(date_ranges, start=1):
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
        if start_date <= today <= end_date:
            return idx

    # Return None if the date is not in any range
    return None

def generate_math_question():

    # Types of operations
    operations = ['+', '-', '*']
    operation = random.choice(operations)

    # Generating two random numbers
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)

    # Creating the question and calculating the answer
    question = f"{num1} {operation} {num2}"
    answer = round(eval(question), 2)

    return question, answer