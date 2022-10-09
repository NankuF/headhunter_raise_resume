import json
import logging
import os
import random
import shutil
import time

import environs
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

from emails.read_email import get_auth_code


def init_logger(name):
    logger = logging.getLogger(name)
    FORMAT = '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filename='logs/logs.log')
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.INFO)
    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.debug('logger was initialized')


init_logger('app')
logger = logging.getLogger('app.hh_resume_up')


class HHResumeUp:
    SECONDS_IN_HOURS = 3600 * 4.1

    def __init__(self, temp_directory):
        self.env = environs.Env()
        self.env.read_env()
        self.email = self.env.str('USER_EMAIL')
        self.options = uc.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument(f'--user-data-dir={temp_directory}')
        self.driver = uc.Chrome(options=self.options)
        logger.info('Driver with options: OK')
        self.driver.implicitly_wait(30)
        self.driver.set_page_load_timeout(60)
        self.pause = self.SECONDS_IN_HOURS
        self.url = 'https://spb.hh.ru'

    @staticmethod
    def has_cookies():
        if os.path.exists('hh_cookies.json'):
            return True
        return False

    def auth(self):
        self.driver.get('https://spb.hh.ru/account/login?backurl=%2F&hhtmFrom=main')
        self.driver.find_element(By.CSS_SELECTOR, '[name="login"]').send_keys(self.email)
        self.driver.find_elements(By.CSS_SELECTOR, '[type="submit"]')[1].click()

        auth_code = get_auth_code()
        self.driver.find_element(By.CSS_SELECTOR, '[name="otp-code-input"]').send_keys(auth_code)
        self.driver.find_elements(By.CSS_SELECTOR, '[type="submit"]')[1].click()

    def save_cookies(self):
        cookies = self.driver.get_cookies()
        with open('hh_cookies.json', 'w', encoding='utf-8') as file:
            json.dump(cookies, file, indent=4, ensure_ascii=False)

    def has_resume_raised(self):
        if self.driver.find_elements(By.CSS_SELECTOR,
                                     '[data-qa="resume-update-button_actions"]')[0].text == 'Поднимать автоматически':
            return True
        return False

    def click_resume_page(self):
        self.driver.find_element(By.CSS_SELECTOR,
                                 '[href="/applicant/resumes?hhtmFrom=main&hhtmFromLabel=header"]').click()

    def raise_resume(self):
        self.driver.find_elements(By.CSS_SELECTOR, '[data-qa="resume-update-button_actions"]')[0].click()

    def resume_up(self):
        if self.has_resume_raised():
            logger.info('Резюме еще рано поднимать.')
        else:
            self.raise_resume()
            logger.info('Резюме успешно поднято.')

    def main(self):
        self.driver.get(self.url)

        if self.has_cookies():
            with open('hh_cookies.json') as file:
                cookies = json.load(file)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            self.click_resume_page()
            self.resume_up()
        else:
            logger.debug('Отсутствуют куки.')
            self.auth()
            logger.info('Успешно авторизован.')
            self.save_cookies()
            self.click_resume_page()
            self.resume_up()


if __name__ == '__main__':
    while True:
        tmp_dir = '/tmp/uc_selenium'
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)
        logger.info('Временная директория успешно удалена.')
        hh = HHResumeUp(temp_directory=tmp_dir)
        try:
            hh.main()
            logger.debug(f'Следующее поднятие резюме через {hh.pause} секунд.')
            time.sleep(hh.pause)
        except Exception as e:
            logger.info(e)
            logger.info('Что-то пошло не так...повторяем.')
            hh.driver.close()
            hh.driver.quit()
            logger.debug('Ждем от 1 до 2 минут')
            time.sleep(random.randrange(60, 120))

