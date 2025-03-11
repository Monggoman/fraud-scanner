from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime, timedelta
import re
import easyocr
from config import *
import csv

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/gmail.send']


GECKODRIVER_PATH = r"C:\WebDrivers\geckodriver.exe"
FIREFOX_PROFILE_PATH = r"C:\Users\patrick.fetizanan_gs\AppData\Roaming\Mozilla\Firefox\Profiles\120saxdk.default-release"
SEARCH_TERM = "SMART POSTPAID PLAN"
MAX_POST_AGE_DAYS = 30
FIREFOX_BINARY_PATH = r"C:\Users\patrick.fetizanan_gs\AppData\Local\Mozilla Firefox\firefox.exe"

firefox_options = Options()
firefox_options.binary_location = FIREFOX_BINARY_PATH
firefox_options.add_argument(f"-profile {FIREFOX_PROFILE_PATH}")
service = Service(GECKODRIVER_PATH)
driver = webdriver.Firefox(service=service, options=firefox_options)

driver.get("https://www.facebook.com")
time.sleep(10)
#print(driver.page_source)

column_name = ["", "Email", "Age"]

# 🔹 Search for term
search_box = driver.find_element(By.XPATH, "//input[@aria-label='Search Facebook']")
search_box.send_keys(SEARCH_TERM)
search_box.send_keys(Keys.RETURN)
time.sleep(10)

try:
    posts_tab = driver.find_element(By.XPATH, "//span[contains(text(), 'Posts')]")
    posts_tab.click()
    time.sleep(10)
except Exception as e:
    print("Error: Cannot find 'Posts' tab", e)
    driver.quit()
    exit()

try:
    posts_recent = driver.find_element(By.XPATH, "//input[@aria-label='Recent Posts']")
    posts_recent.click()
    time.sleep(10)
except Exception as e:
    print("Error: Cannot find 'Posts' tab", e)
    driver.quit()
    exit()


for _ in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

posts = driver.find_elements(By.XPATH, "//div[contains(@class, 'x1yztbdb')]")
print(f"Found {len(posts)} posts.")

if len(posts) == 0:
    print("No posts found. Try adjusting the XPath or waiting longer.")
    driver.quit()
    exit()

today = datetime.today()
#with open("files/page_source.txt", "w", encoding="utf-8") as file:
    #file.write(driver.page_source)


num = 0
check_reels = "reels"
for post in posts:
    post_content = post.text
    if check_reels in post_content.lower():
        continue
    try:
        #post_seemore = post.find_element(By.XPATH, "//div[contains(text(), 'See more')]")
        #post_seemore.click()

        post_url_element_hover = post.find_element(By.XPATH, ".//a[contains(@class, 'x1i10hfl') and contains(@class, 'xi81zsa')]")

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", post_url_element_hover)
        actions = ActionChains(driver)
        actions.move_to_element(post_url_element_hover).perform()
        time.sleep(3)


        post_tooltip = driver.find_element(By.XPATH, "//div[contains(@role, 'tooltip')]")

        date_ss = post_tooltip.text

        print(f"DATE:{date_ss}\n")


    except Exception as e:
        print("Error: Cannot find date", e)
        driver.quit()
        exit()
    try:
        #timestamp_element = post.find_element(By.XPATH, ".//abbr")
        #post_time = timestamp_element.get_attribute("title")
        #post_date = datetime.strptime(post_time, "%B %d, %Y")

        #if (today - post_date).days > MAX_POST_AGE_DAYS:
        #    print(f"Skipping old post from {post_date.strftime('%Y-%m-%d')}")
        #    continue

        post_url_element = post.find_element(By.XPATH, ".//a[contains(@class, 'x1i10hfl') and contains(@class, 'xi81zsa')]")

        post_url = post_url_element.get_attribute("href")


        post_content = re.sub(r"\n\n", "", post_content)
        post_content = re.sub(r"(?m)^\w\n", "", post_content)

        if SEARCH_TERM.lower() in post_content.lower():
            print(f"\n New Post Found {num}:")
            print(f"Date: {date_ss}")
            print(f"URL: {post_url}")
            print(f"Content: {post_content}\n")

        time.sleep(7)

    except Exception as e:
        print("Error extracting post details:", e)


driver.quit()