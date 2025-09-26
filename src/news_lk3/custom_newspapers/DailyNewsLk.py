import os

from dateutil import parser

from news_lk3.core import AbstractNewsPaper

URL_BASE = "http://dailynews.lk"


class DailyNewsLk(AbstractNewsPaper):
    @classmethod
    def get_index_urls(cls):
        index_urls = []
        for category in [
            "local",
            "politics",
            "sports",
            "editorial",
            "business",
            "featured",
            "entertainment",
            "events",
            "lawnorder",
        ]:
            index_urls.append(os.path.join(URL_BASE, "category", category))
        return index_urls

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []

        for li in soup.find_all(
            "li", {"class": "grid-style grid-2-style"}
        ) + soup.find_all(
            "li", {"class": "list-post penci-item-listp penci-slistp"}
        ):
            article_url = os.path.join(URL_BASE, li.find("a").get("href"))
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        div_time = soup.find("div", {"class": "post-box-meta-single"})
        assert div_time, "[parse_time_ut] div_time not found"
        span = div_time.find("span")
        assert span, "[parse_time_ut] span not found"
        d = parser.parse(span.text)
        return int(d.timestamp())

    @classmethod
    def parse_title(cls, soup):
        h1 = soup.find("h1", {"class": "post-title"})
        assert h1, "[parse_title] h1 not found"
        return h1.text

    @classmethod
    def parse_body_lines(cls, soup):
        div_body = soup.find(
            "div", {"class": "inner-post-entry entry-content"}
        )
        assert div_body, "[parse_body_lines] div_body not found"

        body_lines = []
        for p in div_body.find_all("p"):
            body_lines.append(p.text.strip())
        return body_lines
