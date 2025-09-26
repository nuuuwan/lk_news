import time

from utils import JSONFile, Log

from lk_news import NewsArticle, NewspaperFactory

log = Log("pipeline")
MIN_T_DAYS = 7


def build_custom_summary():
    doc_list = NewsArticle.list_all()
    min_t = time.time() - MIN_T_DAYS * 86400
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

    no_data = []
    for newspaper_cls in NewspaperFactory.list_all():
        newspaper_id = newspaper_cls.get_newspaper_id()
        if newspaper_id not in newspaper_to_n:
            no_data.append(newspaper_id)

    custom_summary = dict(
        MIN_T_DAYS=MIN_T_DAYS,
        no_data=no_data,
        newspaper_to_n=newspaper_to_n,
    )

    log.debug(f"{custom_summary=}")
    JSONFile("custom_summary.json").write(custom_summary)
    log.info("Wrote custom_summary.json")


if __name__ == "__main__":
    # NewsArticle.run_pipeline()
    build_custom_summary()
