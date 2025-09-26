import random
from dataclasses import dataclass
from typing import Generator

from utils import File, Hash, Log, Time, TimeFormat

from lk_news.NewspaperFactory import NewspaperFactory
from scraper import AbstractDoc

log = Log("NewsArticle")


@dataclass
class NewsArticle(AbstractDoc):
    newspaper_id: str
    time_ut: int

    def write_text_from_article(self, article):
        if not self.has_text:
            text_content = "\n\n".join(
                [article.original_title] + article.original_body_lines
            )
            File(self.text_path).write(text_content)
            log.info(f"Wrote {self.text_path}")

    @classmethod
    def from_news_lk3_article(cls, article):
        date_str = TimeFormat.DATE.format(Time(article.time_ut))
        num = article.newspaper_id + "-" + Hash.md5(article.url)[:8]
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
        newspaper_cls_list = NewspaperFactory.list_all()
        random.shuffle(newspaper_cls_list)
        for newspaper_cls in newspaper_cls_list:
            article_list = newspaper_cls.scrape()
            for article in article_list:
                yield cls.from_news_lk3_article(article)
