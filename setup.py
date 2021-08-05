import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='GoogleNewsScraper',
    version='0.0.3',
    description='Scrapes Google News article data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/GeminidSystems/google_news_scraper',
    author='Geminid Systems',
    author_email='dev@geminidsystems.com',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['selenium'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
