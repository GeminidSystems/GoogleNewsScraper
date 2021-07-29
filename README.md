# google-news-scraper

## Getting Started

### Installation

```bash
pip install google-news-scraper
```

# Reference

## Importing

```Python
import importlib

GoogleNewsScraper = importlib.import_module('google-news-scraper').GoogleNewsScraper
```

## Instantiating Scraper

```Python
GoogleNewsScraper(driver, automation_options, chrome_driver_arguments).scrape()
```

**Constructor Parameters**

| Name   | Type       | Required |
| ------ | ---------- | -------- |
| driver | web driver | no       |

Possible values:

- `'chrome'`: The driver will default to use this package's chrome driver
- A path to some driver (FireFox, for instance) stored on the user's system

---

| Name               | Type   | Required |
| ------------------ | ------ | -------- |
| automation_options | object | yes      |

Possible values:

- `keywords` : A series of words that will be inputted into Google News.
- `date_range` : Filters how recent data should be. Can be any of the following (defaults to 'Past 24 hours'):
  - Past hours
  - Past 24 hours
  - Past week
  - Past month
  - Past year
  - Archives
- `pages` : Number of pages that should be scraped (defaults to 'max').
- `pagination_pause_per_page` : Waits a certain amount of seconds before a new page is scraped (defaults to 2). Time may have to be increased if Google prevents you from scraping all pages.

---

| Name                    | Type | Required |
| ----------------------- | ---- | -------- |
| chrome_driver_arguments | list | no       |

**Ignore this parameter if you are not choosing to use the default 'chrome' driver**

Possible values:

- `'--headless'`
- `'--ignore-certificate-errors'`
- `'--incognito'`
- `'--no-sandbox'`
- `'--disable-setuid-sandbox'`
- `'--disable-dev-shm-usage'`

Click this link to view all possible arguments: https://chromedriver.chromium.org/capabilities

---

## Methods

**This method is both public and private, though it really should only be used by the class**

```Python
locate_html_element(self, driver, element, selector, wait_seconds=30)
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

- By.ID
- By.CLASS_NAME

---
