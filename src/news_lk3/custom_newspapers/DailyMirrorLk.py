from news_lk3.core import AbstractNewsPaper


class DailyMirrorLk(AbstractNewsPaper):
    @classmethod
    def get_time_raw_format(cls):
        return "%Y-%m-%d %H:%M:%S"
        # return '%d %B %Y %I:%M %p' # previous

    @classmethod
    def get_index_urls(cls):
        return [
            "https://www.dailymirror.lk/latest-news/342",
            "https://www.dailymirror.lk/top-storys/155",
            "https://www.dailymirror.lk/business",
            "https://www.dailymirror.lk/opinion/231",
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for div in soup.find_all("div", {"class": "col-md-8"}):
            a_list = div.find_all("a")
            for a in a_list:
                article_url = a.get("href")
                if article_url == "#000000":
                    continue
                has_invalid_keyword = False
                for invalid_keyword in [
                    "dailymirrorepaper",
                    "lk/print",
                    "lk/australia",
                ]:
                    if invalid_keyword in article_url:
                        has_invalid_keyword = True
                        break
                if has_invalid_keyword:
                    continue
                article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_title(cls, soup):
        h1 = soup.find("h1", {"class": "inner_header"})
        assert h1, "[parse_title] no h1"
        return h1.text

    @classmethod
    def parse_body_lines(cls, soup):
        div_content = soup.find("div", {"class": "a-content"})
        assert div_content, "[parse_body_lines] no div_content"
        return list(
            map(
                lambda line: line.strip(),
                div_content.text.strip().split("\n"),
            )
        )
