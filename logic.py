import time
import pyperclip
import random
import logging

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def search_in_blog(driver, search_keyword, neighbor_request_message):
    driver.get("https://section.blog.naver.com/")
    rand_sleep()

    pyperclip.copy(search_keyword)
    driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div/div[2]/form/fieldset/div/input').send_keys(
        Keys.COMMAND + 'v')
    rand_sleep()

    driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div/div[2]/form/fieldset/a[1]').click()
    rand_sleep()

    while True:
        for i in range(0, len(driver.find_elements(By.CSS_SELECTOR, ".pagination span a"))):
            for author in driver.find_elements(By.CSS_SELECTOR, ".writer_info .author"):
                # 새창 띄워서 작업해야함
                blog_url = "https://m.blog.naver.com/" + author.get_attribute("href").split("/")[3]

                driver.execute_script(f'window.open();')
                rand_sleep()
                driver.switch_to.window(driver.window_handles[-1])
                driver.get(blog_url)
                rand_sleep()

                driver.find_element(By.CLASS_NAME, "add_buddy_btn__oGR_B").click()
                rand_sleep()

                try:
                    both_buddy_radio = driver.find_element(By.ID, "bothBuddyRadio")

                    # 만약 서이추가 가능한 사람일 경우
                    if both_buddy_radio.get_attribute("ng-disabled") == "false":
                        # 서이추 버튼 클릭
                        both_buddy_radio.click()
                        rand_sleep()
                        # 서이추 메세지 입력
                        driver.find_element(By.CSS_SELECTOR, ".add_msg textarea").clear()
                        rand_sleep()

                        pyperclip.copy(neighbor_request_message)
                        driver.find_element(By.CSS_SELECTOR, ".add_msg textarea").send_keys(Keys.COMMAND + 'v')
                        rand_sleep()

                        driver.find_element(By.CLASS_NAME, "btn_ok").click()
                        rand_sleep()
                except NoSuchElementException as e:
                    # 이경우는 이미 서이추가 되어있는 사람이라서 그냥 넘어가는 것으로..
                    pass

                # 이제 열었던 창을 닫아야 함.
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])

            if i != len(driver.find_elements(By.CSS_SELECTOR, ".pagination span a")):
                driver.find_elements(By.CSS_SELECTOR, ".pagination span a")[i + 1].click()
                rand_sleep()

        try:
            driver.find_element(By.CSS_SELECTOR, ".pagination .button_next").click()
            rand_sleep()
        except NoSuchElementException as e:
            logging.getLogger("main").info("블로그의 모든 글을 탐색했습니다.")
            break


def naver_login(driver, username, password):
    login_url = "https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/"
    driver.get(login_url)
    rand_sleep()

    driver.find_element(By.CSS_SELECTOR, '#id')  # 예외처리에 필요 이 구문이 없으면 아이디가 클립보드에 계속 복사됨
    rand_sleep()

    pyperclip.copy(username)
    driver.find_element(By.CSS_SELECTOR, '#id').send_keys(Keys.COMMAND + 'v')
    rand_sleep()

    pyperclip.copy(password)
    driver.find_element(By.CSS_SELECTOR, '#pw').send_keys(Keys.COMMAND + 'v')

    rand_sleep()

    driver.find_element(By.XPATH, '//*[@id="log.login"]').click()
    rand_sleep()


def dev_naver_login(driver):
    login_url = "https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/"
    driver.get(login_url)
    rand_sleep()

    driver.find_element(By.CSS_SELECTOR, '#id')  # 예외처리에 필요 이 구문이 없으면 아이디가 클립보드에 계속 복사됨
    rand_sleep()

    pyperclip.copy("fuhafuha9")
    driver.find_element(By.CSS_SELECTOR, '#id').send_keys(Keys.COMMAND + 'v')
    rand_sleep()

    pyperclip.copy("tofhdl19!")
    driver.find_element(By.CSS_SELECTOR, '#pw').send_keys(Keys.COMMAND + 'v')

    rand_sleep()

    driver.find_element(By.XPATH, '//*[@id="log.login"]').click()
    rand_sleep()


def get_driver():
    options = Options()
    options.add_experimental_option("detach", True)
    chrome_driver = webdriver.Chrome(options=options)
    return chrome_driver


def rand_sleep():
    time.sleep(random.uniform(1.5, 2.5))


def empty(s: str):
    return True if len(s) == 0 else False
