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
GoogleNewsScraper(driver, date_range, pages, pagination_pause_per_page, driver_options)
```

**Constructor Parameters**

| Name   | Type       | Required |
| ------ | ---------- | -------- |
| driver | web driver | no       |

Possible values:

- `'chrome'`: The driver will default to use this package's chrome driver
- A path to some driver (FireFox, for instance) stored on the user's system

---

| Name       | Type | Required |
| ---------- | ---- | -------- |
| date_range | str  | no       |

**Description**: Filters how recent data should be. Can be any of the following (defaults to 'Past 24 hours'):

Possible values:

- Past hours
- Past 24 hours
- Past week
- Past month
- Past year
- Archives

---

| Name  | Type       | Required |
| ----- | ---------- | -------- |
| pages | str or int | no       |

**Descrption**: Number of pages that should be scraped (defaults to 'max').

---

| Name                      | Type | Required |
| ------------------------- | ---- | -------- |
| pagination_pause_per_page | int  | no       |

**Descrption**: Waits a certain amount of seconds before a new page is scraped (defaults to 2). Time may have to be increased if Google prevents you from scraping all pages.

---

| Name           | Type | Required |
| -------------- | ---- | -------- |
| driver_options | list | no       |

**Ignore this parameter if you are not choosing to use the default 'chrome' driver**

Possible values (ONLY for Chrome driver):

- `'--headless'`
- `'--ignore-certificate-errors'`
- `'--incognito'`
- `'--no-sandbox'`
- `'--disable-setuid-sandbox'`
- `'--disable-dev-shm-usage'`

Click this link to view all possible arguments (ONLY for Chrome driver): https://chromedriver.chromium.org/capabilities

---

## Methods

**This method is both public and private, though it really should only be used by the class**

```Python
locate_html_element(self, driver, element, selector, wait_seconds)
```

---

| Name   | Type       | Required |
| ------ | ---------- | -------- |
| driver | web driver | yes      |

Possible values:

- A web driver (Chrome, FireFox, etc)

---

| Name    | Type   | Required |
| ------- | ------ | -------- |
| element | string | yes      |

Possible values:

- Id selector of an HTML element
- Class selector of an HTML element

---

| Name     | Type          | Required |
| -------- | ------------- | -------- |
| selector | Module import | yes      |

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

| Name         | Type   | Required |
| ------------ | ------ | -------- |
| wait_seconds | number | no       |

**default**: `30`

Description:

- Waits a certain number of seconds in order to locate an HTML element
- If an element exists on the page, it will be located instantaneously
- If an element does not yet exist, (if it will appear once a request is made, for instance)
- wait_seconds may have to be increased depending on how long it takes for an element to appear

**please note**: 30 seconds is plenty; this time would rarely have to be increased

---

```Python
GoogleNewsScraper().scrape(search_text, cb)
```

---

| Name        | Type | Required |
| ----------- | ---- | -------- |
| search_text | str  | yes      |

---

**Descrption**: A series of word(s) that will be inputted into the Google search engine

| Name | Type     | Required |
| ---- | -------- | -------- |
| cb   | function | no       |

**Descrption**:

- Will return all article data on a single page for every page scraped (defaults to False)

- **Example**:

```Python
def handle_page_data(page_data: list):
  # Do something with page_data

GoogleNewsScraper().scrape(get_page_data)
```

**NOTE**:

- If no argument is provided fro 'cb,' the scrape method will return a two-dimensional list
- Each list will contain an object of news article data for every news article on that page

**Example of what type of data that a single article-object will contain:**

- `'description'`: The preview description of the news article
- `'title'`: The title of the news article
- `'source'`: The source of news article (New York Times, for instance)
- `'image_url'`: The url of the preview news article image
- `'article_link'`: A link to the news article
- `'time_published_ago'`: A datetime string that represents the date of when the article was published

---
