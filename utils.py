from datetime import datetime

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
