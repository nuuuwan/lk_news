from news_lk3.core import AbstractNewsPaper


class LankadeepaLk(AbstractNewsPaper):
    @classmethod
    def get_original_lang(cls):
        return "si"

    @classmethod
    def get_index_urls(cls):
        return [
            "https://www.lankadeepa.lk/latest_news/1",
            "https://www.lankadeepa.lk/feature/2",
            "https://www.lankadeepa.lk/politics/13",
            "https://www.lankadeepa.lk/editorial/117",
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for h5 in soup.find_all("h5", {"class": "p-b-0"}):
            article_url = h5.find("a").get("href")
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_title(cls, soup):
        h3 = soup.find("h3", {"class": "f1-l-3 cl2 p-b-0 respon2"})
        assert h3, "[parse_title] no h3"
        return h3.text

    @classmethod
    def parse_body_lines(cls, soup):
        div_body = soup.find("div", {"class": "header inner-content p-b-20"})
        assert div_body, "[parse_body_lines] no header_inner"
        return list(
            map(
                lambda line: line.strip(),
                div_body.text.strip().split("\n"),
            )
        )
