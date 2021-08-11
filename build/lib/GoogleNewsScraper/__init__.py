from datetime import datetime
from datetime import timedelta
import time
import os

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver


def get_chrome_driver():
    driver_path = os.path.abspath(os.path.join(os.path.dirname(
        __file__), 'chromedriver/chromedriver'))

    options = webdriver.ChromeOptions()

    options.add_argument('--headless')

    driver = webdriver.Chrome(driver_path, options=options)

    return driver


class Error(Exception):
    pass


class GoogleNewsScraper:
    def __init__(self, driver='chrome'):
        if driver == 'chrome':
            self.driver = get_chrome_driver()
        else:
            self.driver = driver

    def __validate_automation_options(self, automation_options: list):
        for i, data_type in enumerate([str, str, [int, str], int]):
            if type(data_type) == list:
                if not (type(automation_options[i]) in data_type):
                    raise Error("Argument '{}' must be of types {} or {}".format(
                        automation_options[i], data_type[0], data_type[1]))
            elif type(automation_options[i]) != data_type:
                raise Error("Argument '{}' must be of type {}".format(
                    automation_options[i], data_type))

    def __get_article_date(self, time_published_ago: str):
        time_type = time_published_ago.split(' ')[1]
        time_number = time_published_ago.split(' ')[0]

        if time_type in ('second', 'seconds'):
            return datetime.now() - timedelta(seconds=int(time_number))
        if time_type in ('min', 'mins'):
            return datetime.now() - timedelta(minutes=int(time_number))
        if time_type in ('hour', 'hours'):
            return datetime.now() - timedelta(hours=int(time_number))
        if time_type in ('day', 'days'):
            return datetime.now() - timedelta(days=int(time_number))
        if time_type in ('week', 'weeks'):
            return datetime.now() - timedelta(weeks=int(time_number))
        return datetime.now() - timedelta(weeks=int((int(time_number) * 52)))

    def __create_id(self, date_time_str, source, title):
        try:
            id = str(date_time_str).replace('-', '').split(' ')[0]
            id += source.upper().replace('HTTPS://', '').replace('WWW.',
                                                                 '').replace('THE', '').replace(' ', '')[:3]

            for word in title.split(' '):
                if word[0].isalnum():
                    id += word[0]
            return id
        except:
            return None

    def __get_article_data(self, driver, i: int):
        date_time = self.__get_article_date(driver.find_elements_by_xpath(
            ".//span[@class='WG9SHc']")[i].text)
        source = driver.find_elements_by_class_name('XTjFC')[i].text
        title = driver.find_elements_by_class_name('JheGif')[i].text

        return {
            'id': self.__create_id(date_time, source, title),
            'description': driver.find_elements_by_class_name('Y3v8qd')[i].text,
            'title': title,
            'source': source,
            'image_url': driver.find_elements_by_class_name('rISBZc')[i].get_attribute('src'),
            'url': driver.find_elements_by_xpath(
                ".//div[@class='dbsr']/a")[i].get_attribute('href'),
            'date_time': date_time
        }

    def __get_next_page_btn(self, driver):
        btn = self.locate_html_element(driver, 'pnnext', By.ID)

        if not btn:
            raise Error(
                "Cannot get next page! Element 'pnnext' could not be located. Try increasing the 'pagination_pause_per_page' param")
        return btn

    def __set_date_range(self, driver):
        driver.execute_script("""
        const menu = document.getElementById('hdtbMenus');
        menu.classList.remove('p4DDCd');
        menu.classList.add('yyoM4d');
        """)

        recent_dropdown = self.locate_html_element(
            driver, 'KTBKoe', By.CLASS_NAME)

        if not recent_dropdown:
            raise Error(
                "Cannot set date range! Element 'KTBKoe' could not be located")
        else:
            recent_dropdown.click()

        # Will click on a new URL and automation will begin from there
        driver.find_element_by_link_text(self.date_range).click()

    def __paginate(self, driver, cb):
        self.__set_date_range(driver)

        page_count = 0
        page_data = []

        # __get_next_page_btn is called multiple times here because the button, even though its id is the same for every page,
        # must be re-initialized for every new page; otherwise, it will not exist and selenium will throw an error
        while self.__get_next_page_btn(driver) and (True if page_count == 'max' else page_count != self.pages):
            page = []

            for i in range(0, len(driver.find_elements_by_class_name('JheGif'))):
                page.append(self.__get_article_data(driver, i))
            cb(page) if cb else page_data.append(page)
            page_count += 1

            time.sleep(self.pagination_pause_per_page)
            self.__get_next_page_btn(driver).click()

        if not cb:
            return page_data

    def locate_html_element(self, driver, element: str, selector: By, wait_seconds=30):
        try:
            element = WebDriverWait(driver, wait_seconds).until(
                EC.presence_of_element_located(
                    (selector, element))
            )
        except:
            raise Error(
                "WebDriverWait could not locate element '{}'. Increase the wait_seconds param; if the element is still unable to be found, then it may not exist on the page".format(element))
        return element

    def search(self, search_text: str, date_range: str = 'Past 24 hours', pages: int or str = 'max', pagination_pause_per_page: int = 2, cb=False):
        self.__validate_automation_options([
            search_text, date_range, pages, pagination_pause_per_page])

        self.date_range = date_range
        self.pages = pages
        self.pagination_pause_per_page = pagination_pause_per_page

        if str(type(cb)) != "<class 'function'>" and cb:
            raise Error("Parameter 'cb' must be of type function or False")

        self.driver.get(
            'https://www.google.com/search?q=' + search_text.replace(' ', '+') + '&source=lnms&tbm=nws')

        data = self.__paginate(self.driver, cb if cb else False)

        self.driver.quit()

        if not cb:
            return data
