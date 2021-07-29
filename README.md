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
GoogleNewsScraper(driver, automation_options, chrome_driver_arguments)
```

**Constructor Parameters**

| Name   | Type                | Required | Description |
| ------ | ------------------- | -------- | ----------- |
| driver | string or interface | no       | See below.  |

Possible values:

- `'chrome'`: The driver will default to use this package's chrome driver
- A path to some driver (FireFox, for instance) stored on the user's system

---

| Name               | Type   | Required | Description |
| ------------------ | ------ | -------- | ----------- |
| automation_options | object | yes      | See below.  |

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

| Name                    | Type | Required | Description |
| ----------------------- | ---- | -------- | ----------- |
| chrome_driver_arguments | list | no       | See below.  |

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
