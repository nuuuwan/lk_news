import unittest

from news_lk3 import AdaDeranaLk


class TestCase(unittest.TestCase):

    def test_single(self):
        newspaper_cls = AdaDeranaLk
        article_list = newspaper_cls.scrape()
        self.assertGreater(len(article_list), 0)
