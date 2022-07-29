import time
import math
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

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
contents,dates,stars,rebuy,month,bests=[],[],[],[],[],[]                                                # 각 컬럼을 구성할 리스트 rebuy : 재구매 확인, month : 한달사용기 확인, bests : 베스트 리뷰 확인

# 웹사이트 열기
browser = chromeWebdriver()
browser.get('https://smartstore.naver.com/chosunfnbmall/products/6140087642')
browser.implicitly_wait(5)                 # 로딩이 끝날 때까지 10초까지는 기다려줌

# 리뷰 단락으로 이동
review_btn = browser.find_element(By.CSS_SELECTOR, '#_productTabContainer > div > div._27jmWaPaKy._1dDHKD1iiX > ul > li:nth-child(2) > a')
browser.execute_script("arguments[0].click();",review_btn)

# 최신순 버튼 클릭
recent_btn = browser.find_element(By.CSS_SELECTOR, '#REVIEW > div > div._2y6yIawL6t > div > div._1jXgNbFhaN > div.WiSiiSdHv3 > ul > li:nth-child(2) > a')
browser.execute_script("arguments[0].click();",recent_btn)

# 총 리뷰수로 몇 페이지인지 계산 (한 페이지에 리뷰 20개, 10페이지 넘으면 다음 눌러줘야함)
pages = int(review_btn.find_element(By.TAG_NAME,'span').text)/ (20*10)
pages = math.ceil(pages)

for pg in range(pages):
    try:
        for i in range(2,12):                                                                                                   # 다음 누르기 전까지 10페이지 있는데 css_selector 확인해보면 0~9가 아닌 2~12로 나와있어서 이렇게 설정
            try: 
                browser.find_element(By.CSS_SELECTOR,f'#REVIEW > div > div._2y6yIawL6t > div > div.cv6id6JEkg > div > div > a:nth-child({i})').click()
                time.sleep(JUMP)
                boxes = browser.find_elements(By.CLASS_NAME,'_2389dRohZq')                                                      # 리뷰 한 개에 대한 정보 담고 있는 클래스
                browser.implicitly_wait(JUMP)                                                                                   # 브라우저 빠르게 돌리면 오류떠서 써줘야함
                for box in boxes:
                    best = ''
                    # 유형 1 : 재구매, 한달사용기인 경우
                    try: 
                        info = box.find_elements(By.CLASS_NAME,'_1eidska71d')                                                   # 재구매, 한달사용기 키워드가 있을 때만 이 클래스가 생김, 키워드가 두 개 있을때는 괜찮은데 한 개 있을 땐 index 오류뜨니까 except로 처리
                        browser.implicitly_wait(JUMP)
                        info1 = info[0].text
                        info2 = info[1].text
                        # 유형 1-1 : BEST 리뷰인 경우
                        try:                                                                                                    # BEST 키워드는 따로 처리해줘야함
                            best = box.find_element(By.CLASS_NAME ,'_2knN9RObah').text                          
                            browser.implicitly_wait(JUMP)
                            bests.append(1)                                                                         
                            content = cleaner(box.find_element(By.CLASS_NAME,'YEtwtZFLDz').text[12:])                           # 클래스 이름 _3QDEeS6NLn에 리뷰도 들어있는데 클래스 이름 겹쳐서 상위 클래스인 YEtwtZFLDz를 가져와서 파싱, '재구매BEST한달사용기'여서 12글자
                            browser.implicitly_wait(JUMP)
                        # 유형 1-2 : BEST 아닌 경우
                        except NoSuchElementException:
                            browser.implicitly_wait(JUMP)
                            bests.append(0)
                            content = cleaner(box.find_element(By.CLASS_NAME,'YEtwtZFLDz').text[8:])
                            browser.implicitly_wait(JUMP)
                        
                        date = box.find_elements(By.CLASS_NAME,'_3QDEeS6NLn')[1].text                                           # _3QDEeS6NLn 클래스 다른 종류로 여러개 있어서 다 가져온 다음 index로 처리
                        browser.implicitly_wait(JUMP)
                        star = int(box.find_element(By.CLASS_NAME,'_15NU42F3kT').text)
                        browser.implicitly_wait(JUMP)

                        contents.append(content)
                        dates.append(date)
                        stars.append(star)
                        rebuy.append(1)
                        month.append(1)
                        print('유형 1 : ',content,date,star,info1, info2,best)
                    # 유형 2 : 재구매 또는 한달사용기인 경우 
                    except IndexError:
                        try:
                            info = box.find_element(By.CLASS_NAME,'_1eidska71d').text                                           # 둘 중 하나만 해당하므로 find_elements가 아닌 element
                            browser.implicitly_wait(JUMP)
                            if info == '재구매':
                                rebuy.append(1)
                                month.append(0)
                                # 유형 2-1 : 재구매이면서 BEST인 경우 
                                try:
                                    best = box.find_element(By.CLASS_NAME ,'_2knN9RObah').text
                                    browser.implicitly_wait(JUMP)
                                    bests.append(1)
                                    content = cleaner(box.find_element(By.CLASS_NAME,'YEtwtZFLDz').text[7:])
                                    browser.implicitly_wait(JUMP)
                                # 유형 2-2 : 재구매이면서 BEST가 아닌 경우
                                except NoSuchElementException:
                                    browser.implicitly_wait(JUMP)
                                    bests.append(0)
                                    content = cleaner(box.find_element(By.CLASS_NAME,'YEtwtZFLDz').text[3:])
                                    browser.implicitly_wait(JUMP)

                            elif info == '한달사용기':
                                rebuy.append(0)
                                month.append(1)
                                #유형 2-3 : 한달사용기이면서 BEST인 경우
                                try:
                                    best = box.find_element(By.CLASS_NAME ,'_2knN9RObah').text
                                    browser.implicitly_wait(JUMP)
                                    bests.append(1)
                                    content = cleaner(box.find_element(By.CLASS_NAME,'YEtwtZFLDz').text[9:])
                                    browser.implicitly_wait(JUMP)
                                #유형 2-4 : 한달사용기이면서 BEST가 아닌 경우
                                except NoSuchElementException:
                                    browser.implicitly_wait(JUMP)
                                    bests.append(0)
                                    content = cleaner(box.find_element(By.CLASS_NAME,'YEtwtZFLDz').text[5:])
                                    browser.implicitly_wait(JUMP)

                            date = box.find_elements(By.CLASS_NAME,'_3QDEeS6NLn')[1].text
                            browser.implicitly_wait(JUMP)
                            star = int(box.find_element(By.CLASS_NAME,'_15NU42F3kT').text)
                            browser.implicitly_wait(JUMP)
                            contents.append(content)
                            dates.append(date)
                            stars.append(star)
                            print('유형 2: ',content,date,star,info,best)
                        
                        # 유형 3 : 재구매, 한달사용기 아닐 경우
                        except NoSuchElementException:
                            # 유형 3-1 : BEST일 경우
                            try:
                                best = box.find_element(By.CLASS_NAME ,'_2knN9RObah').text
                                browser.implicitly_wait(JUMP)
                                bests.append(1)
                                content = cleaner(box.find_element(By.CLASS_NAME,'YEtwtZFLDz').text[4:])
                                browser.implicitly_wait(JUMP)
                            # 유형 3-2 : BEST 아닐 경우
                            except NoSuchElementException:
                                browser.implicitly_wait(JUMP)
                                bests.append(0)
                                content = cleaner(box.find_element(By.CLASS_NAME,'YEtwtZFLDz').text)
                                browser.implicitly_wait(JUMP)
                            
                            date = box.find_elements(By.CLASS_NAME,'_3QDEeS6NLn')[1].text
                            browser.implicitly_wait(JUMP)
                            star = int(box.find_element(By.CLASS_NAME,'_15NU42F3kT').text)
                            browser.implicitly_wait(JUMP)
                            contents.append(content)
                            dates.append(date)
                            stars.append(star)
                            rebuy.append(0)
                            month.append(0)
                            print('유형 3: ',content,date,star,best)
                
            except Exception as e:
                print (e)
                pass
        # 10페이지 다 돌고나서 다음 버튼 클릭
        browser.find_element(By.CSS_SELECTOR,'#REVIEW > div > div._2y6yIawL6t > div > div.cv6id6JEkg > div > div > a.fAUKm1ewwo._2Ar8-aEUTq').click()
        browser.implicitly_wait(JUMP)
    except:
        pass
    
df = pd.DataFrame({'본문': contents,'날짜':dates,'평점':stars,'재구매여부':rebuy,'한달사용기 여부':month,'BEST상품':bests})
df = df.drop_duplicates()                                                                                                       # 중복제거
df.index +=1                                                                                                                    # dataframe 인덱스 정리
df['날짜'] = pd.to_datetime(df['날짜'],format ='%y.%m.%d.')                                                                      # 날짜 형식 맞추기
df['날짜'] = df['날짜'].dt.strftime('%Y-%m-%d')
df.to_csv('./크롤링.csv',encoding='utf-8-sig')                                                                                   # csv 파일로 저장

