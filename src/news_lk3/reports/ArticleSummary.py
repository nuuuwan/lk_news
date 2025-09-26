import os
from functools import cached_property

from utils import Directory, Log, Time, TimeFormat, TSVFile

from news_lk3.core import Article

log = Log("ArticleSummary")


class ArticleSummary:
    @cached_property
    def summary(self):
        d_list = []
        for article in Article.list_from_remote():
            d_list.append(
                dict(
                    # more useful
                    newspaper_id=article.newspaper_id,
                    time_str=TimeFormat.TIME.format(Time(article.time_ut)),
                    original_title=article.original_title,
                    n_original_body_lines=len(article.original_body_lines),
                    # less useful
                    hash=Article.get_hash(article.url),
                    time_ut=article.time_ut,
                    original_lang=article.original_lang,
                    url=article.url,
                )
            )
        d_list = sorted(d_list, key=lambda d: d["time_ut"], reverse=True)
        return d_list

    @property
    def summary_file_path(self):
        return os.path.join(Article.DIR_REPO, "summary.tsv")

    def store_summary(self):
        summary = self.summary
        if not Directory(Article.DIR_REPO).exists:
            os.makedirs(Article.DIR_REPO)
            log.debug(f"Created directory {Article.DIR_REPO}")

        TSVFile(self.summary_file_path).write(summary)
        log.debug(f"Stored summary to {self.summary_file_path}")
