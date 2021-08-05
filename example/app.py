from GoogleNewsScraper import GoogleNewsScraper


def get_article_data_without_cb():
    print(GoogleNewsScraper(driver='chrome', keywords='climate change',  # To see a list of all possible arguments and values, please refer to the documentation
                            pages=5, driver_options=['--headless']).scrape())


def get_article_data_with_cb():
    def handle_page_data(page_data):
        print(page_data)

    GoogleNewsScraper(driver='chrome', keywords='climate change',
                             pages=5, driver_options=['--headless']).scrape(handle_page_data)


get_article_data_with_cb()
get_article_data_with_cb()
