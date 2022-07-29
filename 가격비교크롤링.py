import time
import math
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

# 크롬드라이버 열기
def chromeWebdriver():
    chrome_service = Service(executable_path=ChromeDriverManager().install())
    options =Options()
    options.add_experimental_option('detach',True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=chrome_service,options=options)
    return driver

# 문자열 정리 함수
def cleaner(string):
    temp = string.replace('\n', '')
    temp = temp.replace('\r', '')
    temp = temp.replace('\t', '')
    return temp

JUMP = 0.5                                                                                              # sleep 시간 

# 키워드 입력받기

#keyword = input('키워드를 입력하세요:')
keyword = '뭉티기'

# 웹사이트 열기
browser = chromeWebdriver()
browser.get('https://shopping.naver.com/home/p/index.naver')                                            # 네이버 쇼핑 페이지
browser.implicitly_wait(5)                                                                              # 로딩이 끝날 때까지 10초까지는 기다려줌

#검색창 클릭
search = browser.find_element(By.CSS_SELECTOR,'input._searchInput_search_input_QXUFf')
search.click()

#검색어 입력
search.send_keys(keyword)
search.send_keys(Keys.ENTER)

# 80개씩 보기 클릭
eighty_btn = browser.find_element(By.CSS_SELECTOR, 'a.subFilter_btn_select__K6F79')
browser.execute_script("arguments[0].click();",recent_btn)

# 광고 거르기


