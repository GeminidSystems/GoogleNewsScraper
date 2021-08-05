from datetime import datetime
from datetime import timedelta
import time
import os

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver


def get_chrome_driver(arguments: list):
    driver_path = os.path.abspath(os.path.join(os.path.dirname(
        __file__), 'chromedriver/chromedriver'))

    options = webdriver.ChromeOptions()

    for arg in arguments:
        options.add_argument(arg)

    driver = webdriver.Chrome(driver_path, options=options)

    return driver


class Error(Exception):
    pass


class GoogleNewsScraper:
    def __init__(self, driver, automation_options={}, chrome_driver_arguments=[]):
        if driver == 'chrome':
            self.driver = get_chrome_driver(chrome_driver_arguments)
        else:
            self.driver = driver

        default_automation_options = self.__validate_automation_options(
            automation_options)

        self.keywords = default_automation_options['keywords']
        self.date_range = default_automation_options['date_range']
        self.pages = default_automation_options['pages']
        self.pagination_pause_per_page = default_automation_options['pagination_pause_per_page']

    def __validate_automation_options(self, automation_options: dict):
        default_automation_options = {
            'keywords': None,
            'date_range': 'Past 24 hours',
            'pages': 'max',
            'pagination_pause_per_page': 2
        }

        default_automation_options.update(automation_options)

        if not default_automation_options['keywords']:
            raise Error("Property 'keywords' is required")

        for key in automation_options:
            if not key in default_automation_options:
                raise Error(
                    'Invalid property: {}'.format(key))

        values = list(default_automation_options.values())
        keys = list(default_automation_options.keys())

        for i, t in enumerate([str, str, [int, str], int]):
            val = type(values[i])

            if type(t) == list:
                if(val not in t):
                    raise Error(
                        "Key '{}' type must be of either the following: {}".format(keys[i], t))
            elif val != t:
                raise Error(
                    "Key '{}' must be of type '{}'".format(keys[i], t))

        return default_automation_options

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

    def __get_article_data(self, driver, i: int):
        return {
            'description': driver.find_elements_by_class_name('Y3v8qd')[i].text,
            'title': driver.find_elements_by_class_name('JheGif')[i].text,
            'source': driver.find_elements_by_class_name('XTjFC')[i].text,
            'image_url': driver.find_elements_by_class_name('rISBZc')[i].get_attribute('src'),
            'article_link': driver.find_elements_by_xpath(
                ".//div[@class='dbsr']/a")[i].get_attribute('href'),
            'time_published_ago': self.__get_article_date(driver.find_elements_by_xpath(
                ".//span[@class='WG9SHc']")[i].text)
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

    def __paginate(self, driver):
        self.__set_date_range(driver)

        pages = []
        page_count = 0

        # __get_next_page_btn is called multiple times here because the button, even though its id is the same for every page,
        # must be re-initialized for every new page; otherwise it will not exist and selenium will throw an error
        while self.__get_next_page_btn(driver) and (True if page_count == 'max' else page_count != self.pages):
            page = []

            for i in range(0, len(driver.find_elements_by_class_name('JheGif'))):
                page.append(self.__get_article_data(driver, i))
            pages.append(page)
            page_count += 1

            time.sleep(self.pagination_pause_per_page)
            self.__get_next_page_btn(driver).click()

        return pages

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

    def scrape(self):
        self.driver.get(
            'https://www.google.com/search?q=' + self.keywords.replace(' ', '+') + '&source=lnms&tbm=nws')

        data = self.__paginate(self.driver)

        self.driver.quit()

        return data
