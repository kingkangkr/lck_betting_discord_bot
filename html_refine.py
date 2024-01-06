import requests
from bs4 import BeautifulSoup
def fetch_html(url):
    try:
        # Requesting the web page
        response = requests.get(url)

        # Check if the request was successful
        response.raise_for_status()

        # Extracting HTML content
        html_content = response.text

        return html_content
    except requests.RequestException as e:
        # Handling any errors that occur during the request
        return f"Error occurred: {e}"
def extract_match_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Finding all <span> tags with 'id' that contains "경기"
    repeating_spans = soup.find_all('span', id=lambda value: "경기" in value if value else False)

    # Extracting text from each <span> tag
    match_info = [span.get_text(separator=" ", strip=True).split(" [")[0] for span in repeating_spans]

    return match_info







# Extract and display the match information
# 주차별 URL 리스트 생성
base_url = "https://namu.wiki/w/2024%20LoL%20Champions%20Korea%20Spring/"
weeks = ["1주차", "2주차", "3주차", "4주차", ["5주차(1라운드)", "5주차(2라운드)"], "6주차", "7주차", "8주차", "9주차"]
week_urls = []

matches_by_week = {}

for week in weeks:
    # 주차별 URL 처리
    week_urls = []
    if isinstance(week, list):
        for sub_week in week:
            week_urls.append(base_url + sub_week)
    else:
        week_urls.append(base_url + week)

    # 각 URL에 대한 경기 정보 추출 및 저장
    week_matches = []
    for url in week_urls:
        html_content = fetch_html(url)
        match_info_list = extract_match_info(html_content)
        week_matches.extend(match_info_list)

    # 주차 이름 결정 (5주차는 특별 처리)
    week_name = week[0] if isinstance(week, list) else week
    week_name = week_name.split("(")[0]  # '5주차(1라운드)' -> '5주차'

    # 주차별 경기 정보 저장
    matches_by_week[week_name] = week_matches

# 결과 출력 (각 주차별 경기 정보)
for week, matches in matches_by_week.items():
    print(f"{week} 경기:")
    for match in matches:
        print(match)
    print()  # 줄바꿈으로 주차별 구분
