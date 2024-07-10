from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import urllib.request
import os

import selenium
print(selenium.__version__)

# Chrome 옵션 설정
chrome_options = webdriver.ChromeOptions()

#chrome_options.add_argument("--headless")  # headless 모드로 실행

# Chrome 드라이버 객체 생성

driver = webdriver.Chrome(options=chrome_options)



# 크롤링할 웹사이트 URL
website_to_scrape = 'https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl'

# 웹사이트 열기
driver.get(website_to_scrape)

current_path = os.getcwd() # 저장경로

words = ["baseball hitter"]

for search_words in words:
    elem = driver.find_element(By.NAME, "q") #검색엔진 찾음
    elem.clear()
    elem.send_keys(search_words) # 검색창 검색어 입력
    elem.send_keys(Keys.RETURN)
    SCROLL_PAUSE_TIME = 3
    #화면 내리기
    SCROLL_PAUSE_TIME = 3

    last_height = driver.execute_script("return document.body.scrollHeight")


    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        #로딩 기다리기
        time.sleep(SCROLL_PAUSE_TIME)

        #더보기 클릭
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element_by_css_selector(
                    ".mye4qd").click()
            except:
                break
        last_height = new_height
                
    #작은 이미지 클릭
    small_imgs = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")

    folder_name = search_words

 

    # 이미지 저장
    if not os.path.isdir(folder_name):  # 없으면 새로 생성하는 조건문
        os.mkdir(folder_name)

    count = 1 
    for image in small_imgs:
        if count > 300:
            break
        try:
            image.click()
            time.sleep(3)
            imgUrl = image.get_attribute("src")
            urllib.request.urlretrieve(
                imgUrl,
                folder_name + "/" + search_words + "." + str(count) + ".jpg")
            count = count + 1
        except:
            pass
    driver.back()


#드라이버 종료
driver.quit()
