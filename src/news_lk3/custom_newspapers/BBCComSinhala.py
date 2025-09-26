from utils import TimeFormat

from news_lk3.core import AbstractNewsPaper

TIME_RAW_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


class BBCComSinhala(AbstractNewsPaper):
    @classmethod
    def get_original_lang(cls):
        return 'si'

    @classmethod
    def get_index_urls(cls):
        return [
            'https://www.bbc.com/sinhala/topics/cg7267dz901t',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for a in soup.find_all('a', {'class': 'focusIndicatorDisplayBlock'}):
            article_url = a.get('href')
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        meta_published_time = soup.find(
            'meta', {'name': 'article:published_time'}
        )
        return (
            TimeFormat(TIME_RAW_FORMAT)
            .parse(meta_published_time.get('content'))
            .ut
        )

    @classmethod
    def parse_title(cls, soup):
        h1 = soup.find('h1', {'id': 'content'})
        return h1.text

    @classmethod
    def parse_body_lines(cls, soup):
        divs = soup.find_all('div', {'dir': 'ltr'})
        return list(
            map(
                lambda div: div.text,
                divs,
            )
        )
