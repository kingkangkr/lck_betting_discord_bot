# Set options for WebDriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

# Check if the HTML file already exists
file_path = 'week3_odds.html'
if os.path.isfile(file_path):
    # If the file exists, read its content
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
else:
    # If the file doesn't exist, run Selenium to fetch the HTML
    options = Options()
    options.headless = True  # Set to True for headless mode
    driver_path = r'C:\Users\Byung Mu Kang\Downloads\chromedriver_win32\chromedriver.exe'
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # Open the webpage
    url = 'https://www.oddsportal.com/esports/league-of-legends/league-of-legends-lck/'
    driver.get(url)
    time.sleep(5)  # Wait for dynamic content to load

    # Get the HTML content
    html_content = driver.page_source

    # Save the HTML content to a file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

    # Close the Selenium driver
    driver.quit()

# Parse the HTML content with BeautifulSoup
soup_full = BeautifulSoup(html_content, 'html.parser')

# Rest of your code to extract and process data from the HTML content


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
import re

# 배당률을 저장할 리스트 초기화
odds_list = []

# 각 formatted_match에서 배당률 추출
for match in formatted_matches:
    # 정규 표현식을 사용하여 배당률 부분 추출
    odds= re.findall(r"\d+.\d+", match)
    if len(odds) == 2:
    # 추출된 배당률을 숫자로 변환하여 튜플 형태로 저장
        odds_tuple = (float(odds[0]), float(odds[1]))
        odds_list.append(odds_tuple)
