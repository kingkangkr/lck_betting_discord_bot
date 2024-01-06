from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Set options for WebDriver
options = Options()
options.headless = False  # Set to True for headless mode
driver_path = r'C:\Users\Byung Mu Kang\Downloads\chromedriver_win32\chromedriver.exe'
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Open the webpage
url = 'https://www.oddsportal.com/esports/league-of-legends/league-of-legends-lck/'
driver.get(url)

# Wait for the page to load
time.sleep(3)

# Get the HTML content of the page
html_content = driver.page_source

# Save the HTML content to a file
with open('page_source.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

# Close the WebDriver
driver.quit()
