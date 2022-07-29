import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


def chromeWebdriver():
    chrome_service = Service(executable_path=ChromeDriverManager().install())
    options =Options()
    options.add_experimental_option('detach',True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=chrome_service,options=options)
    return driver

# 웹사이트 열기
browser = chromeWebdriver()
browser.get('https://www.naver.com')
browser.implicitly_wait(10)                 # 로딩이 끝날 때까지 10초까지는 기다려줌

# 쇼핑 메뉴 클릭
browser.find_element(By.CSS_SELECTOR,'a.nav.shop').click()
browser.implicitly_wait(10)
time.sleep(1)

#검색창 클릭
search = browser.find_element(By.CSS_SELECTOR,'input._searchInput_search_input_QXUFf')
search.click()

#검색어 입력
search.send_keys('아이폰 12')
search.send_keys(Keys.ENTER)

before_h = browser.execute_script("return window.scrollY")                  # 0으로 초기화하기

#무한 스크롤
while True:
    # 맨 아래로 스크롤을 내린다
    browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)

    #스크롤 사이 페이지 로딩 시간
    time.sleep(1)

    #스크롤 후 높이
    after_h = browser.execute_script('return window.scrollY')

    if after_h == before_h:
        break
    before_h = after_h

# 파일 생성
f = open (r'C:\Users\ys050\Dropbox\내 PC (LAPTOP-60DNJ58Q)\Desktop\문서\대학생활\자습\셀리니움 사용\data_example.csv','w',encoding='CP949',newline='')
csvWriter = csv.writer(f)

# 상품 정보 div
items = browser.find_elements(By.CSS_SELECTOR,'.basicList_info_area__17Xyo')

for item in items:
    # 상품 이름 가져오기
    name = item.find_element(By.CSS_SELECTOR,'.basicList_title__3P9Q7').text
    
    # 상품 가격 가져오기 (가격 없는 것 예외처리)
    try :
        price = item.find_element(By.CSS_SELECTOR,'.price_num__2WUXn').text
    except:
        price = "판매중단"

    # 상품 링크 가져오기
    link = item.find_element(By.CSS_SELECTOR,'.basicList_title__3P9Q7 > a').get_attribute('href')
    
    # csv 파일에 쓰기
    csvWriter.writerow([name,price,link])

# 파일 닫기
f.close()


