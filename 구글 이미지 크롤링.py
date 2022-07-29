import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import urllib.request

def chromeWebdriver():
    chrome_service = Service(executable_path=ChromeDriverManager().install())
    options =Options()
    options.add_experimental_option('detach',True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=chrome_service,options=options)
    return driver

# 웹사이트 열기
browser = chromeWebdriver()
browser.get('https://www.google.co.kr/?&bih=938&biw=1874&hl=ko')
search = browser.find_element(By.NAME,'q')
search.send_keys('여성 썬캡')
search.send_keys(Keys.ENTER)

# 이미지 페이지로 이동
browser.find_element(By.XPATH,'/html/body/div[7]/div/div[4]/div/div[1]/div/div[1]/div/div[2]/a').click()

SCROLL_PAUSE_TIME = 1

last_h = browser.execute_script('return document.body.scrollHeight')

while True:
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    time.sleep(SCROLL_PAUSE_TIME)

    new_h = browser.execute_script('return document.body.scrollHeight')
    if new_h == last_h:
        try:
            browser.find_element(By.CSS_SELECTOR,'.mye4qd').click()
        except:
            break
    last_h = new_h



images = browser.find_elements(By.CSS_SELECTOR,'.rg_i.Q4LuWd')
count =1

for image in images:
    try:
        image.click()
        time.sleep(2)
        imgUrl = browser.find_element(By.CSS_SELECTOR,'img.n3VNCb.KAlRDb').get_attribute('src')
        urllib.request.urlretrieve(imgUrl,"C:/Users/ys050/Dropbox/내 PC (LAPTOP-60DNJ58Q)/Desktop/문서/대학생활/자습/셀리니움 사용/"+str(count) +".jpg")
        count +=1
        print (count + "성공")
    except:
        pass