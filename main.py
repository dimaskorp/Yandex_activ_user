from selenium import webdriver
from faker import Faker
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
from auth_data import user1
import pickle
import random
import time

# Установив пользовательский агент для имитации мобильных устройств
user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
)

fake = Faker(locale="ru_RU")
# запускаем браузер и переходим на страницу авторизации Яндекс.Маркета
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
# options.add_argument("--user-data-dir=chrome-data")
options.add_argument('- disable-gpu')
options.add_argument('user-agent=%s' % user_agent)
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)
driver.get("https://market.yandex.ru/")


def print_hi():
    try:
        # выбираем случайного пользователя
        user = random.choice(user1)
        if driver.current_url == 'https://market.yandex.ru/':
            for cookie in pickle.load(open(f"{user['email']}_cookies", "rb")):
                driver.add_cookie(cookie)
            driver.refresh()
            time.sleep(2)

            # находим поле поиска и вводим случайный запрос
            search_input = driver.find_element(By.ID, "header-search")
            search_query = fake.word()

            search_input.send_keys(search_query)
            search_input.send_keys(Keys.ENTER)

            # ждем загрузки страницы с результатами и выбираем случайный товар
            time.sleep(5)
            results_popular = driver.find_elements(By.XPATH, "//div[@data-auto='item']")
            if len(results_popular) > 0:
                random_product = random.choice(results_popular)
                product_name_link = random_product.find_elements(By.XPATH, "//a[@target='_blank']")
                product_name_link.click()
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
                product_name_link.click()
        else:
            print("Проверка капча")
    except Exception as ex:
        print(ex)
    # finally:
    #     # закрываем браузер
    #     # driver.close()
    #     driver.quit()


def detailed():  # нажимаем подробнее
    detail = driver.find_elements(By.XPATH, "//span[@class='_2qvOO _19m_j _2AJHX'][@role='button']")
    detail.click()
    return


def to_favorites():  # нажимаем в избранное
    favorite = driver.find_elements(By.XPATH, "//button[@class='_1KpjX Wbmen _2hbFS AybJQ _113KO']")
    favorite.click()
    return


def specifications():  # нажимаем характеристики
    specifical = driver.find_elements(By.XPATH, "//div[@data-baobab-name='specsLink']/a")
    specifical.click()
    return


def evaluations():  # нажимаем оценки
    evaluation = driver.find_elements(By.XPATH, "//div[@class='_1o1QM']/a")
    evaluation.click()
    return


def into_basket():  # нажимаем Добавить в карзину
    basket = driver.find_elements(By.XPATH, "//button[@variant='action'][@target='_self']")
    basket.click()
    return


if __name__ == '__main__':
    print_hi()
