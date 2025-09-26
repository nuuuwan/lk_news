import unittest

from news_lk3 import AdaDeranaLk


class TestCase(unittest.TestCase):

    def test_single(self):
        newspaper_cls = AdaDeranaLk
        article_list = newspaper_cls.scrape()
        print(article_list)
        self.assertGreater(len(article_list), 0)
