from utils import TimeFormat

from news_lk3.core import AbstractNewsPaper


class NewsFirstLk(AbstractNewsPaper):
    BASE_URL = "https://english.newsfirst.lk"

    @classmethod
    def use_selenium(cls):
        return True

    @classmethod
    def get_index_urls(cls):
        index_urls = []
        for category in [
            "latest-news",
            "featured",
            "sports",
            "business",
            "corporate-brief",
            "local",
        ]:
            index_urls.append(f"{cls.BASE_URL}/{category}")
        return index_urls

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for div in soup.find_all("div", {"class": "ng-star-inserted"}):
            a = div.find("a")
            if not a:
                continue
            article_url = cls.BASE_URL + a.get("href")
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        div_author_main = soup.find("div", {"class": "author_main"})
        assert div_author_main, "[parse_time_ut] No div_author_main found"
        span = div_author_main.find("span")
        assert span, "[parse_time_ut] No span found"
        time_str = span.text.strip()
        return TimeFormat("%d-%m-%Y | %I:%M %p").parse(time_str).ut

    @classmethod
    def parse_title(cls, soup):
        h1 = soup.find("h1", {"class": "top_stories_header_news"})
        assert h1, "[parse_title] No h1 found"
        return h1.text

    @classmethod
    def parse_body_lines(cls, soup):
        div_body = soup.find("div", {"class": "new_details"})
        assert div_body, "[parse_body_lines] No div_body found"
        return [
            p.text.strip() for p in div_body.find_all("p") if p.text.strip()
        ]
