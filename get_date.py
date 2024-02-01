from datetime import datetime
from texts import matches


def get_current_week(test_date=None):
    date_ranges = [
        ("2024-01-15", "2024-01-21"),  # 1주차
        ("2024-01-22", "2024-01-28"),  # 2주차
        ("2024-01-29", "2024-02-04"),  # 3주차
        ("2024-02-12", "2024-02-18"),  # 4주차
        ("2024-02-19", "2024-02-25"),  # 5주차 (R1 결산)
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


current_week = get_current_week()
if current_week is None:
    print("현재 진행 중인 경기가 없습니다.")
else:
    current_week_matches = get_matches_for_current_week(current_week, matches)
    print(f"현재 주차: {current_week}주차")
    print("이번 주 경기:")
    for match in current_week_matches:
        print(f"{match[0]} vs {match[1]}")
