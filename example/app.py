from GoogleNewsScraper import GoogleNewsScraper


def get_article_data_without_cb():
    print(GoogleNewsScraper).search(search_text='climate change', pages=5)


def get_article_data_with_cb():
    def handle_page_data(page_data):
        print(page_data)

    GoogleNewsScraper().search(search_text='climate change', pages=5, cb=handle_page_data)


get_article_data_without_cb()
get_article_data_with_cb()
