import random
from dataclasses import dataclass
from functools import cached_property
from typing import Generator

from utils import File, Hash, Log, Time, TimeFormat

from lk_news.NewspaperFactory import NewspaperFactory
from scraper import AbstractDoc

log = Log("NewsArticle")


@dataclass
class NewsArticle(AbstractDoc):
    newspaper_id: str
    time_ut: int

    @cached_property
    def cmp(self):
        return (self.time_ut, self.doc_id)

    def write_text_from_article(self, article):
        assert len(article.original_title) >= 5, article.original_title
        text_content = "\n\n".join(
            [article.original_title] + article.original_body_lines
        )
        assert len(text_content) >= 5, text_content

        if not self.has_text:
            File(self.text_path).write(text_content)
            log.debug(f"Wrote {self.text_path}")

    @classmethod
    def from_news_lk3_article(cls, article):

        description = article.original_title
        if len(description) < 5:
            log.error(f'Description too short: "{description}"')
            return None

        num = article.newspaper_id + "-" + Hash.md5(article.original_title)[:8]

        time_ut = article.time_ut
        dt = Time.now().ut - time_ut
        assert dt > 0, f"{time_ut=} is in the future"
        assert dt < 86400 * 365.35 * 10, f"{time_ut=} is older than 10 years"
        date_str = TimeFormat.DATE.format(Time(article.time_ut))

        doc = cls(
            num=num,
            date_str=date_str,
            description=article.original_title,
            url_metadata=article.url,
            lang=article.original_lang,
            newspaper_id=article.newspaper_id,
            time_ut=article.time_ut,
        )

        doc.write()
        doc.write_text_from_article(article)

        return doc

    @classmethod
    def gen_docs(cls) -> Generator["NewsArticle", None, None]:
        url_metadata_set = cls.get_url_metadata_set()
        newspaper_cls_list = NewspaperFactory.list_all()
        random.shuffle(newspaper_cls_list)
        for newspaper_cls in newspaper_cls_list:
            for article in newspaper_cls.gen_articles(url_metadata_set):
                doc = cls.from_news_lk3_article(article)
                if doc is not None:
                    yield doc
