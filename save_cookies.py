from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium_recaptcha_solver import RecaptchaSolver
import pickle
import time
from auth_data import user

# Установив пользовательский агент для имитации мобильных устройств
user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
)


def save_coomies():
    try:
        # запускаем браузер и переходим на страницу авторизации
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument('user-agent=%s' % user_agent)
        driver = webdriver.Chrome(options=options)
        # solver = RecaptchaSolver(driver=driver)
        driver.implicitly_wait(5)
        time.sleep(2)
        driver.get("https://pocket-link.co/ru/login")
        # заполняем форму авторизации
        # вводим логин

        driver.find_element(By.NAME, "email").send_keys(user[0]["email"] + Keys.ENTER)
        time.sleep(2)
        driver.find_element(By.NAME, "password").send_keys(user[0]["password"] + Keys.ENTER)
        time.sleep(1)
        # cookies
        pickle.dump(driver.get_cookies(), open(f"{user[0]['email']}_cookies", "wb"))
        print(f"Создан файл {user[0]['email']}_cookies")

    except Exception as ex:
        print(ex)
    finally:
        # закрываем браузер
        driver.close()
        driver.quit()


if __name__ == '__main__':
    save_coomies()
