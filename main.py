import pickle

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import random
import time

# Установив пользовательский агент для имитации мобильных устройств
user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
)

# запускаем браузер и переходим на страницу авторизации Яндекс.Маркета
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
# options.add_argument("--user-data-dir=chrome-data")
options.add_argument('- disable-gpu')
options.add_argument('user-agent=%s' % user_agent)
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)
driver.get("https://pocket-link.co/ru/cabinet/")


def print_hi():
    try:

        if driver.current_url == 'https://pocket-link.co/ru/login':
            for cookie in pickle.load(open(f"dima-skorp@mail.ru_cookies", "rb")):
                driver.add_cookie(cookie)
            driver.refresh()
            time.sleep(1)
            # находим поле поиска и вводим случайный запрос
            tool_open = driver.find_element(By.CLASS_NAME, "pair-number-wrap")
            tool_open.click()
            time.sleep(1)
            search = driver.find_element(By.CLASS_NAME, "search__field").send_keys("chfjpy")

            tool_click = driver.find_element(By.XPATH, "//li[contains(@class,'alist__item')][2]")
            payment = int(driver.find_element(By.XPATH, "//li[contains(@class,'alist__item')][2]/a/span[@class='alist__payout']/span").text[:-1])

            if payment >= 50:
                tool_click.click()

                # title_expiration = driver.find_element(By.XPATH, "//div[@class='block block--expiration-inputs']/div[@class='block__title']").text
                # if driver.find_element(By.XPATH, "//i[@class='fa fa-flag-checkered']"):
                #
                #     expiration = driver.find_element(By.XPATH, "//div[@class='control__buttons buttons'][1]/a/i")
                #     driver.execute_script("arguments[0].click();",  expiration)
                #     # expiration.click()
                set_time = driver.find_element(By.XPATH, "//div[@class='block block--expiration-inputs']/div[@class='block__control control']/div[@class='control__value value value--several-items']")
                driver.execute_script("arguments[0].click();",  set_time)
                modal_time = int(driver.find_element(By.XPATH, "//div[@class='trading-panel-modal__in']/div[@class='rw'][2]/div[@class='input-field-wrapper']/input").get_attribute('value'))
                if modal_time == 5:
                    if g == "ВВЕРХ":
                        btn_call = driver.find_element(By.CLASS_NAME, "btn btn-call").click()
                    elif g == "ВНИЗ":
                        btn_put = driver.find_element(By.CLASS_NAME, "btn btn-put").click()

                else:
                    rez = 5-modal_time
                    minus = driver.find_element(By.XPATH, "//div[@class='trading-panel-modal__in']/div[@class='rw'][2]/a[@class='btn-minus']")
                    driver.execute_script("arguments[0].click();", minus)
                print('')

            else:
                print("Меньше 80%")
                driver.close()
            # ждем загрузки страницы с результатами и выбираем случайный товар
            time.sleep(5)
            results_popular = driver.find_elements(By.XPATH, "//div[@data-auto='item']")
            if len(results_popular) > 0:
                random_product = random.choice(results_popular)
                product_name_link = random_product.find_elements(By.XPATH, "//a[@target='_blank']")
                product_name_link[random.choice(results_popular)].click()
                # ждем загрузки страницы с описанием товара нажимаем подробнее
                time.sleep(2)
                detailed()
                # ждем 5 сек нажимаем подробнее
                time.sleep(5)

            else:
                print("Популярных предложений нет")
                RE_INT = re.search(r'\d')
                results = driver.find_elements(By.XPATH, f"//div[@data-index='{RE_INT}']")
                random_product = random.choice(results)
                product_name_link = random_product.find_elements(By.XPATH, "//a[@target='_blank']")
                product_name_link[random.choice(results_popular)].click()
        else:
            print("Проверка капча")

    except Exception as ex:
        print(ex)


# finally:
#     # закрываем браузер
#     # driver.close()
#     driver.quit()





if __name__ == '__main__':
    print_hi()
