# NOTE: HTML selectors must be updated every 6 weeks in order to encapsulate Chrome's version updates

from datetime import datetime
from datetime import timedelta
import time
import os

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def get_chrome_driver() -> WebDriver:
    driver_path = os.path.abspath(os.path.join(os.path.dirname(
        __file__), 'chromedriver/chromedriver'))

    options = webdriver.ChromeOptions()

    options.add_argument('--headless')

    #driver = webdriver.Chrome(driver_path, options=options)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    return driver


class Error(Exception):
    pass


class GoogleNewsScraper:
    def __init__(self, driver='chrome'):
        self.driver = get_chrome_driver() if driver == 'chrome' else driver

    def __get_article_date(self, time_published_ago: str) -> datetime:
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

    def __create_id(self, date_time_str: datetime, source: str, title: str) -> str or None:
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

    def __get_article_data(self, driver, i: int) -> dict:
        date_time = self.__get_article_date(driver.find_elements_by_xpath(
            '//div[@id="rso"]/div/g-card[1]/div/div/a/div/div[2]/div[4]/span')[i].text)
        source = driver.find_elements_by_xpath(
            '//div[@id="rso"]/div/g-card[1]/div/div/a/div/div[2]/div[1]/span')[i].text
        title = driver.find_elements_by_xpath('//div[@id="rso"]/div/g-card[1]/div/div/a/div/div[2]/div[2]')[i].text
        return {
            'id': self.__create_id(date_time, source, title),
            'description': driver.find_elements_by_xpath('//div[@id="rso"]/div/g-card[1]/div/div/a/div/div[2]/div[3]')[i].text,
            'title': title,
            'source': source,
            'image_url': driver.find_elements_by_xpath('//div[@id="rso"]/div/g-card[1]/div/div/a/div/div[1]/div/g-img/img')[i].get_attribute('src'),
            'url': driver.find_elements_by_xpath('//div[@id="rso"]/div/g-card[1]/div/div/a')[i].get_attribute('href'),
            'date_time': date_time
        }

    def __get_next_page_btn(self, driver):
        btn = self.locate_html_element(driver, 'pnnext', By.ID)

        if not btn:
            raise Error(
                "Cannot get next page! Element 'pnnext' could not be located. Try increasing the 'pagination_pause_per_page' argument")
        return btn

    def __set_date_range(self, driver) -> None:
        driver.execute_script("""
        const menu = document.getElementById('hdtbMenus');
        menu.classList.remove('p4DDCd');
        menu.classList.add('yyoM4d');
        """)

        recent_dropdown = self.locate_html_element(
            driver, '//div[@id="hdtbMenus"]/div[@id="tn_1"]/span[1]/g-popup/div[1]/div/div', By.XPATH)

        if not recent_dropdown:
            raise Error(
                "Cannot set date range! Element 'KTBKoe' could not be located")
        else:
            recent_dropdown.click()

        # Will click on a new URL and automation will begin from there
        driver.find_element_by_link_text(self.date_range).click()

    def __paginate(self, driver, cb) -> None:
        self.__set_date_range(driver)

        page_count = 0
        page_data = []

        # __get_next_page_btn is called multiple times here because the button, even though its id is the same for every page,
        # must be re-initialized for every new page; otherwise, it will not exist and selenium will throw an error
        while self.__get_next_page_btn(driver) and (True if page_count == 'max' else page_count != self.pages):
            page = []

            for i in range(0, len(driver.find_elements_by_xpath('//div[@id="rso"]/div/g-card[1]/div/div/a/div/div[2]/div[2]'))):
                page.append(self.__get_article_data(driver, i))

            cb(page) if cb else page_data.append(page)
            page_count += 1

            time.sleep(self.pagination_pause_per_page)
            self.__get_next_page_btn(driver).click()

        if not cb:
            return page_data

    def __validate_automation_options(self, cb, pages):
        if str(type(cb)) != "<class 'function'>" and cb:
            raise Error("Parameter 'cb' must be of type function or False")

        if (type(pages) == str and pages != 'max'):
            raise Error(
                "Parameter 'pages' must be of type int or the str 'max'")

    def locate_html_element(self, driver, element: str, selector: By, wait_seconds=30):
        try:
            element = WebDriverWait(driver, wait_seconds).until(
                EC.presence_of_element_located(
                    (selector, element))
            )
        except:
            raise Error(
                "WebDriverWait could not locate element '{}'. Increase the 'pagination_pause_per_page argument'; if the element is still unable to be found, then it may not exist on the page".format(element))
        return element

    def search(self, search_text: str, date_range: str = 'Past 24 hours', pages: int or str = 'max', pagination_pause_per_page: int = 2, cb=False) -> list or None:
        self.__validate_automation_options(cb, pages)
        
        self.pagination_pause_per_page = pagination_pause_per_page
        self.date_range = date_range
        self.pages = pages

        self.driver.get(
            'https://www.google.com/search?q=' + search_text.replace(' ', '+') + '&source=lnms&tbm=nws')

        data = self.__paginate(self.driver, cb if cb else False)

        self.driver.quit()

        if not cb:
            return data
