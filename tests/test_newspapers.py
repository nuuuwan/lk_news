import unittest

from lk_news import NewspaperFactory


class TestCase(unittest.TestCase):
    def test_scrape(self):
        newspaper_cls_list = NewspaperFactory.list_all()
        for newspaper_cls in newspaper_cls_list:
            article_list = newspaper_cls.scrape()
            self.assertGreater(len(article_list), 0)
