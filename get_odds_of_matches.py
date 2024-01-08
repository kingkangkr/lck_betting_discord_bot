from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
# Set options for WebDriver
options = Options()
#options.headless = False  # Set to True for headless mode
#driver_path = r'C:\Users\Byung Mu Kang\Downloads\chromedriver_win32\chromedriver.exe'

'''service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Open the webpage
url = 'https://www.oddsportal.com/esports/league-of-legends/league-of-legends-lck/'
driver.get(url)
time.sleep(5)  # 동적 콘텐츠 로드를 위해 대기

# HTML 내용 가져오기
html = driver.page_source
driver.quit()

# Parsing the full HTML content with BeautifulSoup
soup_full = BeautifulSoup(html, 'html.parser')
current_directory = os.getcwd()
html_file_name = "saved_html_content.html"

# Create the full path for the file in the current working directory
html_file_path_cwd = os.path.join(current_directory, html_file_name)

# Write the HTML content to the file in the current working directory
with open(html_file_path_cwd, 'w', encoding='utf-8') as file:
    file.write(html)'''
# 저장된 HTML 파일의 경로
file_path = 'saved_html_content.html'  # 여기에 실제 파일 경로 입력

# 파일 열기 및 내용 읽기
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

soup_full = BeautifulSoup(html_content, 'html.parser')

# Using a lambda function to match elements with 'default-odds' in their class attribute in the full HTML content
all_elements_with_default_odds_full = soup_full.find_all(lambda tag: tag.get('class') and 'default-odds' in ' '.join(tag.get('class')))

# Extracting the text from each element in the full HTML content
odds = [element.get_text() for element in all_elements_with_default_odds_full]

all_team_names = soup_full.find_all('p', class_='participant-name')

# 각 요소에서 텍스트 추출
team_names = [element.get_text() for element in all_team_names]

formatted_matches = []
for i in range(0, len(team_names), 2):
    match = f"{team_names[i]} vs {team_names[i+1]} - {team_names[i]} 배당: {odds[i]}, {team_names[i+1]} 배당: {odds[i+1]}"
    formatted_matches.append(match)

print(formatted_matches)