from utils import TimeFormat

from news_lk3.core import AbstractNewsPaper

TIME_RAW_FORMAT = '%Y-%m-%dT%H:%M:%S+05:30'


class DivainaLk(AbstractNewsPaper):
    @classmethod
    def get_original_lang(cls):
        return 'si'

    @classmethod
    def get_index_urls(cls):
        return [
            'https://divaina.lk/category/vigasa-puwath/',
            'https://divaina.lk/category/pradeshiya-puvath/',
            'https://divaina.lk/category/visheshanga/',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for h3 in soup.find_all(
            'h3', {'class': 'entry-title td-module-title'}
        ):
            article_url = h3.find('a').get('href')
            article_urls.append(article_url)

        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        time_ = soup.find(
            'time', {'class': 'entry-date updated td-module-date'}
        )
        return (
            TimeFormat(TIME_RAW_FORMAT)
            .parse(time_.get('datetime').strip())
            .ut
        )

    @classmethod
    def parse_title(cls, soup):
        h1 = soup.find('h1', {'class': 'entry-title'})
        return h1.text

    @classmethod
    def parse_body_lines(cls, soup):
        div = soup.find('div', {'class': 'td-post-content tagdiv-type'})
        ps = div.find_all('p')
        return list(
            map(
                lambda p: p.text,
                ps,
            )
        )
