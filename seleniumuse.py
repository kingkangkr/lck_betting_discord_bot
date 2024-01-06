from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
# Set options for WebDriver
options = Options()
options.headless = False  # Set to True for headless mode
driver_path = r'C:\Users\Byung Mu Kang\Downloads\chromedriver_win32\chromedriver.exe'

service = Service(executable_path=driver_path)
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

# Using a lambda function to match elements with 'default-odds' in their class attribute in the full HTML content
all_elements_with_default_odds_full = soup_full.find_all(lambda tag: tag.get('class') and 'default-odds' in ' '.join(tag.get('class')))

# Extracting the text from each element in the full HTML content
extracted_elements_text_full = [element.get_text() for element in all_elements_with_default_odds_full]

print(extracted_elements_text_full)  # Displaying the first 10 elements for brevity


