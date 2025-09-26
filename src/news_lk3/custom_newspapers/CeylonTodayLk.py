from utils import TimeFormat, TimeZoneOffset

from news_lk3.core import AbstractNewsPaper

TIME_RAW_FORMAT = "%Y-%m-%dT%H:%M:%S+05:30"


class CeylonTodayLk(AbstractNewsPaper):
    @classmethod
    def get_index_urls(cls):
        return [
            "https://ceylontoday.lk/category/local/",
            "https://ceylontoday.lk/category/business/",
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for a in soup.find_all("a", {"class": "td-image-wrap"}):
            article_url = a.get("href")
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        time_ = soup.find(
            "time", {"class": "entry-date updated td-module-date"}
        )
        return (
            TimeFormat(TIME_RAW_FORMAT, TimeZoneOffset.LK)
            .parse(time_.get("datetime"))
            .ut
        )

    @classmethod
    def parse_author(cls, soup):
        div = soup.find("div", {"class": "td-post-author-name"})
        a = div.find("a")
        return a.text

    @classmethod
    def parse_title(cls, soup):
        h1 = soup.find("h1", {"class": "entry-title"})
        return h1.text

    @classmethod
    def parse_body_lines(cls, soup):
        div = soup.find("div", {"class": "td-post-content tagdiv-type"})
        return list(
            map(
                lambda line: line.strip(),
                div.text.strip().split("\n"),
            )
        )
