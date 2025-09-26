from utils import Log

from news_lk3.base import Summarizer, Translator
from news_lk3.core.article.Article import Article

log = Log("ExtArticleBase")


class ExtArticleBase(Article):
    def __init__(
        self,
        # Article attributes
        newspaper_id: str,
        url: str,
        time_ut: int,
        original_lang: str,
        original_title: str,
        original_body_lines: list[str],
        # (new) attributes
        translated_text: dict[str, dict[str, str]],
        summary_lines: list[str],
    ):
        super().__init__(
            newspaper_id=newspaper_id,
            url=url,
            time_ut=time_ut,
            original_lang=original_lang,
            original_title=original_title,
            original_body_lines=original_body_lines,
        )
        self.translated_text = translated_text
        self.summary_lines = summary_lines

    @staticmethod
    async def get_translated_text(article: Article):
        idx = {}
        src = article.original_lang

        for dest in ["si", "ta", "en"]:
            if src == dest:
                continue
            translator = Translator(src, dest)

            translated_title = await translator.translate(
                article.original_title,
            )
            translated_body_lines = []
            for line in article.original_body_lines:
                translated_line = await translator.translate(
                    line,
                )
                translated_body_lines.append(translated_line)
            idx[dest] = dict(
                title=translated_title,
                body_lines=translated_body_lines,
            )
        return idx

    @staticmethod
    def get_summary_lines(translated_text) -> list[str]:
        if not (translated_text and "en" in translated_text):
            return []

        title = translated_text["en"]["title"]
        body_lines = translated_text["en"]["body_lines"]
        content_lines = [title] + body_lines
        return Summarizer().summarize(content_lines)

    @property
    def to_dict(self) -> dict:
        return dict(
            translated_text=self.translated_text,
            summary_lines=self.summary_lines,
        )

    @property
    def has_en_translation(self):
        return self.translated_text and "en" in self.translated_text
