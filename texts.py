video_links= {}
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

