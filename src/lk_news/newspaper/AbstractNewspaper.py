
from dataclasses import dataclass
from abc import ABC
from functools import cached_property
from typing import Generator

from lk_news.news_article import NewsArticle



class AbstractNewspaper(ABC):
    
    @cached_property
    def name(self) -> str:
        return self.__class__.__name__

    def gen_docs(self) -> Generator[NewsArticle, None, None]:
        raise NotImplementedError
