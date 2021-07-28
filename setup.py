from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable'
]

keywords = [
    'web scraper',
    'web crawler',
    'crawler',
    'scraper',
    'google news scraper',
    'google news crawler',
    'google news automation',
    'google news automator',
    'google',
    'google news'
]

setup(
    name='google_news_scraper',
    version='0.0.1',
    description='Scrapes Google News article data',
    Long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='https://pypi.org/project/google-news-scraper/',
    author='Geminid Systems',
    author_email='',
    License='MIT',
    classifiers=classifiers,
    keywords=keywords,
    packages=find_packages(),
    install_requires=''
)
