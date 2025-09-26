"""Utils for reading remote files."""

import ssl

import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import FiledVariable

USER_AGENT = ' '.join(
    [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0)',
        'Gecko/20100101 Firefox/65.0',
    ]
)


# pylint: disable=W0212
ssl._create_default_https_context = ssl._create_unverified_context  # noqa


class WWW:
    def __init__(self, url):
        self.url = url

    def readBinary(self):
        try:
            resp = requests.get(self.url, headers={'user-agent': USER_AGENT})
            if resp.status_code != 200:
                return None
            return resp.content
        except requests.exceptions.ConnectionError:
            return None

    def read(self):
        def nocache():
            binary = self.readBinary()
            if not binary:
                return None
            return binary.decode()

        return FiledVariable(self.url, nocache).value

    def readSelenium(self):
        def nocache():
            options = Options()
            options.add_argument('--headless')
            driver = webdriver.Firefox(options=options)
            driver.get(self.url)
            content = driver.page_source
            driver.quit()
            return content

        return FiledVariable(self.url + '.selenium', nocache).value
