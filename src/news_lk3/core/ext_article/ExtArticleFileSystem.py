import asyncio
import os

from utils import JSONFile, Log

from news_lk3.core.article.Article import Article

log = Log("ExtArticleFileSystem")


class ExtArticleFileSystem:
    @staticmethod
    def get_extended_data(article: Article):
        file_path = os.path.join(
            Article.DIR_REPO,
            "ext_articles",
            ExtArticleFileSystem.get_ext_article_file_name(article.url),
        )

        if not os.path.exists(file_path):
            return {}
        return JSONFile(file_path).read()

    @classmethod
    def from_article(cls, article: Article, force_extend: bool):
        extended_data = ExtArticleFileSystem.get_extended_data(article)
        translated_text = extended_data.get(
            "translated_text",
            None,
        )
        summary_lines = extended_data.get(
            "summary_lines",
            None,
        )

        if force_extend:
            if not translated_text:
                translated_text = asyncio.run(cls.get_translated_text(article))
            if not summary_lines:
                summary_lines = cls.get_summary_lines(translated_text)

        return cls(
            newspaper_id=article.newspaper_id,
            url=article.url,
            time_ut=article.time_ut,
            original_lang=article.original_lang,
            original_title=article.original_title,
            original_body_lines=article.original_body_lines,
            translated_text=translated_text,
            summary_lines=summary_lines,
        )

    @staticmethod
    def get_ext_article_file_name(url):
        h = Article.get_hash(url)
        return f"{h}.ext.json"

    @property
    def relative_ext_article_file_path(self):
        return os.path.join(
            "ext_articles",
            ExtArticleFileSystem.get_ext_article_file_name(self.url),
        )

    @property
    def relative_ext_article_file_path_unix(self):
        return self.relative_ext_article_file_path.replace("\\", "/")

    @property
    def temp_ext_article_file_path(self):
        return os.path.join(
            Article.DIR_REPO, self.relative_ext_article_file_path
        )

    def store(self):
        JSONFile(self.temp_ext_article_file_path).write(self.to_dict)
        log.info(f"Stored {self.temp_ext_article_file_path}.")
