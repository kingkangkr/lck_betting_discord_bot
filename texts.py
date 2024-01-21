video_links = {}
video_links['1주차'] = 'https://www.youtube.com/watch?v=sqDQpN8yjOE'
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
bet_date_ranges = [
    ("2024-01-10", "2024-01-16"),  # Week 1
    ("2024-01-17", "2024-01-23"),  # Week 2
    ("2024-01-24", "2024-01-30"),  # Week 3
    # One week break
    ("2024-02-07", "2024-02-13"),  # Week 4
    ("2024-02-14", "2024-02-20"),  # Week 5
    ("2024-02-21", "2024-02-27"),  # Week 6
    ("2024-02-28", "2024-03-05"),  # Week 7
    ("2024-03-06", "2024-03-12"),  # Week 8
    ("2024-03-13", "2024-03-19"),  # Week 9
    ("2024-03-20", "2024-03-26"),  # Week 10
    # Additional weeks can be added in the same pattern
]
commands_info = (""""!명령어' 또는 '!ㅁㄹㅇ': 모든 명령어를 보여줍니다. 
'!전체경기' 또는 '!ㅈㅊㄱㄱ': 현재 모든 경기 정보를 표시합니다. 
'!경기' 또는 '!ㄱㄱ': 현재 주의 경기 정보를 표시합니다. 
'!베팅' 또는 '!ㅂㅌ': 현재 베팅 예측 정보를 표시합니다. 
'!포인트' 또는 '!ㅍㅇㅌ': 현재 보유 중인 포인트를 조회합니다. 
'!출석체크' 또는 '!ㅊㅊ' 또는 '!cc': 출석체크를 하고 포인트를 추가합니다. 
'!순위' 또는 '!ㅅㅇ': 사용자 순위를 표시합니다. 
'!하이라이트' 또는 '!ㅎㅇㄹㅇㅌ': 방장이 추천하는 LCK 하이라이트 영상을 표시합니다. 
'!ㅂㄹㅈ' 또는 '!블랙잭' : 포인트를 건 블랙잭을 합니다. 
        """)
announcement = """LCK 베팅 포인트 관리 봇입니다.
1주차~9주차 경기 베팅이 가능하고, 그 주 베팅을 하기 위해서는 그 전주 수요일부터 그 주 화요일까지 베팅이 가능합니다.
(Ex. 2주차는 1월 24일부터 1월 28일. 2주차 베팅 가능 기간은 1월 17일부터 1월 23일)
버그 문의나 기능 제안은 디스코드 채팅으로 해주세요.
<사용자 등록하는 법> '!register' 또는 '!등록' 또는 '!ㄷㄹ' 을 한 후 방장이 디코 봇을 껐다 켜야지 등록이 됩니다. 사용자는 등록을 한번만 하면 됩니다."""