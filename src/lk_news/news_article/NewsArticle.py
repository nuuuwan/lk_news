from dataclasses import dataclass
from typing import Generator

from scraper import AbstractDoc


@dataclass
class NewsArticle(AbstractDoc):
    newspaper_name: str
    title: str
    body_paragraphs: list[str]

    @classmethod
    def gen_docs(cls) -> Generator["NewsArticle", None, None]:
        pass
