from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium_recaptcha_solver import RecaptchaSolver
import pickle
import time
from auth_data import user1

# Установив пользовательский агент для имитации мобильных устройств
user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
)


def save_coomies():
    try:
        # запускаем браузер и переходим на страницу авторизации Яндекс.Маркета
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        # options.add_argument("--user-data-dir=chrome-data")
        options.add_argument('- disable-gpu')
        options.add_argument('user-agent=%s' % user_agent)
        driver = webdriver.Chrome(options=options)
        solver = RecaptchaSolver(driver=driver)
        driver.implicitly_wait(5)
        driver.get("https://market.yandex.ru/")
        # находим ссылку на страницу авторизации и кликаем на нее
        login_link = driver.find_element(By.XPATH, "//a[@headernav='HeaderNav']")
        time.sleep(2)
        login_link.click()
        time.sleep(2)
        # заполняем форму авторизации
        # вводим логин
        mail = driver.find_element(By.XPATH, "//button[@class='Button2 Button2_checked Button2_size_l Button2_view_default']")
        mail.click()
        driver.find_element(By.NAME, "login").send_keys(user1["email"] + Keys.ENTER)
        time.sleep(2)
        driver.find_element(By.NAME, "passwd").send_keys(user1["password"] + Keys.ENTER)
        time.sleep(1)
        # cookies
        pickle.dump(driver.get_cookies(), open(f"{user1['email']}_cookies", "wb"))
        print(f"Создан файл {user1['email']}_cookies")

    except Exception as ex:
        print(ex)
    finally:
        # закрываем браузер
        driver.close()
        driver.quit()


if __name__ == '__main__':
    save_coomies()
