import os
import tempfile
from functools import cache

from utils import Directory, Git, Hash, JSONFile, Log

log = Log("ArticleLoader")


class ArticleFileSystem:
    DIR_REPO = os.path.join(tempfile.gettempdir(), "news_lk3_data")
    DIR_REPO_ARTICLES = os.path.join(DIR_REPO, "articles")

    HASH_SALT = "123019839120398"
    HASH_LENGTH = 8

    @staticmethod
    def get_hash(url):
        return Hash.md5(url + ArticleFileSystem.HASH_SALT)[
            : ArticleFileSystem.HASH_LENGTH
        ]

    @staticmethod
    def get_article_file_name(url):
        h = ArticleFileSystem.get_hash(url)
        return f"{h}.json"

    @staticmethod
    def load_d_from_file(article_file):
        return JSONFile(article_file).read()

    @classmethod
    def load_from_file(cls, article_file):
        d = cls.load_d_from_file(article_file)
        return cls.from_dict(d)

    @property
    def relative_article_file_path(self):
        return os.path.join(
            "articles", ArticleFileSystem.get_article_file_name(self.url)
        )

    @property
    def relative_article_file_path_unix(self):
        return self.relative_article_file_path.replace("\\", "/")

    @property
    def temp_article_file_path(self):
        return os.path.join(
            ArticleFileSystem.DIR_REPO, self.relative_article_file_path
        )

    def store(self):
        JSONFile(self.temp_article_file_path).write(self.to_dict)
        log.info(f"Stored {self.temp_article_file_path}.")

    @classmethod
    @cache
    def list_from_remote(cls) -> list:
        git = Git("https://github.com/nuuuwan/news_lk3_data.git")
        git.clone(cls.DIR_REPO, branch_name="main")
        git.checkout("main")

        articles = []
        for child in Directory(cls.DIR_REPO_ARTICLES).children:
            if isinstance(child, Directory) or child.ext != "json":
                continue
            article = cls.load_from_file(child.path)
            articles.append(article)

        sorted_articles = sorted(
            articles, key=lambda article: article.time_ut, reverse=True
        )

        n_articles = len(sorted_articles)
        log.debug(f"Loaded {n_articles} articles")
        return sorted_articles
