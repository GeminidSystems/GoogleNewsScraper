# googlenewsscraper

## Getting Started

### Installation

```bash
pip install GoogleNewsScraper
```

# Reference

## Importing

```Python
from GoogleNewsScraper import GoogleNewsScraper
```

## Instantiating Scraper

```Python
GoogleNewsScraper(driver)
```

**Constructor Parameters**

| Name   | Type       | Required |
| ------ | ---------- | -------- |
| driver | web driver | no       |

Possible values:

- `'chrome'`: The driver will default to use this package's chrome driver
- A path to some driver (FireFox, for instance) stored on the user's system

## Methods

**This method is both public and private, though it really should only be used by the class**

```Python
locate_html_element(self, driver, element, selector, wait_seconds)
```

| Name         | Type          | Required | Description                                                          |
| ------------ | ------------- | -------- | -------------------------------------------------------------------- |
| driver       | web driver    | yes      | A web driver (Chrome, FireFox, etc)                                  |
| element      | string        | yes      | Id or class selector of an HTML element                              |
| selector     | Module import | yes      | see below                                                            |
| wait_seconds | int           | no       | Waits a certain number of seconds in order to locate an HTML element |

**To configure the 'selector' param**:

First install selenium

```bash
pip install selenium
```

Then import By

```Python
from selenium.webdriver.common.by import By
```

Possible values:

- `By.ID`
- `By.CLASS_NAME`
- `By.CSS_SELECTOR`
- `By.LINK_TEXT`
- `By.NAME`
- `By.PARTIAL_LINK_TEXT`
- `By.TAG_NAME`
- `By.XPATH`

---

```Python
GoogleNewsScraper(...args).search(search_text, date_range, pages, pagination_pause_per_page, cb) -> list or None
```

| Name                      | Type       | Required | Description                                                                                                                                                   |
| ------------------------- | ---------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| search_text               | str        | yes      | A series of word(s) that will be inputted into the Google search engine                                                                                       |
| date_range                | str        | no       | Filters article by date. Possible values: Past hours, Past 24 hours, Past week, Past month, Past year, Archives                                               |
| pages                     | str or int | no       | Number of pages that should be scraped (defaults to 'max')                                                                                                    |
| pagination_pause_per_page | int        | no       | Waits a certain amount of seconds before a new page is scraped (defaults to 2). Time may have to be increased if Google prevents you from scraping all pages. |
| cb                        | function   | no       | Will return all article data on a single page for every page scraped (defaults to False)                                                                      |

- **Example using 'cb' paramater**:

```Python
def handle_page_data(page_data: list):
  # Do something with page_data

GoogleNewsScraper(...args).search(...args, handle_page_data)
```

**NOTE**:

- If no argument is provided for 'cb,' the scrape method will return a two-dimensional list
- Each list will contain an object of news article data for every news article on that page

**Example of what type of data that a single article-object will contain:**

- `'id'`: A unique id for every article data object
- `'description'`: The preview description of the news article
- `'title'`: The title of the news article
- `'source'`: The source of news article (New York Times, for instance)
- `'image_url'`: The url of the preview news article image
- `'url'`: A link to the news article
- `'date_time'`: A datetime string that represents the date of when the article was published

---
