import time

from utils import JSONFile, Log

from lk_news import NewsArticle

log = Log("pipeline")


def build_custom_summary():
    doc_list = NewsArticle.list_all()
    min_t = time.time() - 86400
    latest_doc_list = [doc for doc in doc_list if doc.time_ut >= min_t]
    newspaper_to_n = {}
    for doc in latest_doc_list:
        newspaper_id = doc.newspaper_id
        if newspaper_id not in newspaper_to_n:
            newspaper_to_n[newspaper_id] = 0
        newspaper_to_n[newspaper_id] += 1

    newspaper_to_n = dict(
        sorted(newspaper_to_n.items(), key=lambda x: x[1], reverse=True)
    )
    log.debug(f"{newspaper_to_n=}")
    JSONFile("newspaper_to_n.json").write(newspaper_to_n)
    log.info(f"Wrote newspaper_to_n.json")


if __name__ == "__main__":
    NewsArticle.run_pipeline()
    build_custom_summary()
