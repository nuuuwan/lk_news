import os

from utils import File, Log, Time, TimeFormat

from news_lk3.core import Article, ExtArticle
from news_lk3.reports.ArticleSummary import ArticleSummary

log = Log("ReadMe")


class ReadMe(ArticleSummary):
    PATH = os.path.join(Article.DIR_REPO, "README.md")
    N_DISPLAY = 100
    ARTICLE_BODY_MAX_CHARS = 1_000
    TIME_FORMAT_DATE_STR = TimeFormat("%Y-%m-%d (%A)")

    @staticmethod
    def render_article(article) -> list[str]:
        ea = ExtArticle.from_article(article, force_extend=False)
        lines = [
            f"### {ea.title_display}",
            "",
            f"*{TimeFormat.TIME.format(Time(article.time_ut))}*"
            + f" · [`{article.newspaper_id}`]({article.url})"
            + f" · `{article.original_lang}`",
            "",
            ea.get_summarized_body(max_chars=ReadMe.ARTICLE_BODY_MAX_CHARS),
            "",
            f"[Data]({ea.relative_article_file_path_unix})",
            "",
        ]
        if os.path.exists(ea.temp_ext_article_file_path):
            lines.extend(
                [
                    "[Extended Data]"
                    + f"({ea.relative_ext_article_file_path_unix})",
                    "",
                ]
            )
        lines.extend(["---", ""])
        return lines

    @staticmethod
    def render_stats_line(label: str, value: int):
        return f"{label} | {value:,}"

    @staticmethod
    def render_ext_article_stats(article_list) -> list[str]:
        n_articles = len(article_list)
        n_ext_articles = 0
        for article in article_list:
            ext_article = ExtArticle.from_article(article, force_extend=False)
            if os.path.exists(ext_article.temp_ext_article_file_path):
                n_ext_articles += 1

        p_ext_articles = n_ext_articles / n_articles

        return [
            "## Data Extension Stats",
            "",
            "Extensions include translations"
            + " and NER (Named Entity Recognition).",
            "",
            f"{n_ext_articles:,} ({p_ext_articles:.1%})"
            + f" of {n_articles:,} articles have been extended.",
            "",
        ]

    @staticmethod
    def get_newspaper_to_n(article_list: list[Article]) -> dict[str, int]:
        newspaper_to_n = {}
        for article in article_list:
            newspaper_to_n[article.newspaper_id] = (
                newspaper_to_n.get(article.newspaper_id, 0) + 1
            )
        return newspaper_to_n

    @staticmethod
    def render_article_stats(article_list: list[Article]) -> list[str]:
        lines = [
            "## Newspaper Stats",
            "",
            f"*Scraped **{len(article_list):,}** Articles*",
            "",
            "newspaper | n",
            "--- | ---:",
        ]
        newspaper_to_n = ReadMe.get_newspaper_to_n(article_list)
        for newspaper_id, n in sorted(
            newspaper_to_n.items(), key=lambda x: x[1]
        ):
            lines.append(ReadMe.render_stats_line(newspaper_id, n))

        lines.append("")

        return lines

    def write(self):
        articles = Article.list_from_remote()

        lines = [
            "# Newspaper Articles from Sri Lanka :sri_lanka:",
            "",
            f"As of **{TimeFormat.TIME.format(Time.now())}**",
            "",
        ]
        lines.extend(ReadMe.render_article_stats(articles))
        lines.extend(ReadMe.render_ext_article_stats(articles))

        lines.extend([f"## Latest {ReadMe.N_DISPLAY:,} Articles ", ""])
        prev_date_str = None
        for article in articles[: self.N_DISPLAY]:
            date_str = ReadMe.TIME_FORMAT_DATE_STR.stringify(
                Time(article.time_ut)
            )
            if date_str != prev_date_str:
                lines.extend([f"### {date_str}", ""])
                prev_date_str = date_str
            lines.extend(ReadMe.render_article(article))

        File(ReadMe.PATH).write("\n".join(lines))
        log.debug(f"Wrote {ReadMe.PATH}")
