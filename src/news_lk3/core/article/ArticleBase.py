class ArticleBase:
    DEFAULT_ORIGINAL_LANG = 'en'

    def __init__(
        self,
        newspaper_id: str,
        url: str,
        time_ut: int,
        original_lang: str,
        original_title: str,
        original_body_lines: list[str],
    ):
        self.newspaper_id = newspaper_id
        self.url = url
        self.time_ut = time_ut
        self.original_lang = original_lang
        self.original_title = original_title
        self.original_body_lines = original_body_lines

    @classmethod
    def from_dict(cls, d):
        return cls(
            newspaper_id=d['newspaper_id'],
            url=d['url'],
            time_ut=d['time_ut'],
            original_lang=d.get('original_lang'),
            original_title=d.get('original_title'),
            original_body_lines=d.get('original_body_lines'),
        )

    @property
    def to_dict(self):
        return dict(
            newspaper_id=self.newspaper_id,
            url=self.url,
            time_ut=self.time_ut,
            original_lang=self.original_lang,
            original_title=self.original_title,
            original_body_lines=self.original_body_lines,
        )

    def __lt__(self, other):
        return self.time_ut < other.time_ut

    @property
    def is_en(self):
        return self.original_lang == 'en'
