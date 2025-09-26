import os
import sys

from utils import JSONFile, Log

from lk_news import NewsArticle
from news_lk3 import Article

log = Log("one_off_backpopulate")


def main(max_docs: int):
    log.debug(f"max_docs={max_docs}")
    dir_news_lk_data = os.path.join("..", "news_lk3_data")
    dir_articles = os.path.join(dir_news_lk_data, "articles")

    n_docs = 0
    for file_name in os.listdir(dir_articles):
        if not file_name.endswith(".json"):
            continue
        file_path = os.path.join(dir_articles, file_name)
        article_d = JSONFile(file_path).read()
        article = Article(
            newspaper_id=article_d["newspaper_id"],
            time_ut=article_d["time_ut"],
            original_title=article_d["original_title"],
            original_body_lines=article_d["original_body_lines"],
            original_lang=article_d["original_lang"],
            url=article_d["url"],
        )
        NewsArticle.from_news_lk3_article(article)
        n_docs += 1
        if n_docs >= max_docs:
            log.info(f"🛑 Reached max_docs={max_docs}, stopping")
            sys.exit(0)

    log.info(f" 🛑 All {n_docs} articles processed.")


if __name__ == "__main__":
    main(max_docs=int(sys.argv[1]))
