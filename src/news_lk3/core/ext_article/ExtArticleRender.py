from functools import cache


class ExtArticleRender:
    CONTINUED = '...'
    END = '◼️'
    END_SUMMARY = '🟩'

    @property
    def title_display(self) -> str:
        if self.is_en or not self.has_en_translation:
            return self.original_title
        return self.translated_text['en']['title']

    @property
    def body_lines_display(self) -> list[str]:
        if self.is_en or not self.has_en_translation:
            return self.original_body_lines
        return self.translated_text['en']['body_lines']

    @property
    def summary_lines_display(self) -> list[str]:
        if self.summary_lines:
            return self.summary_lines
        return []

    @cache
    def get_summarized_body(self, max_chars: int) -> str:
        total_chars = 0
        display_lines = []
        is_partial = False

        for line in self.body_lines_display:
            if len(line) + total_chars > max_chars:
                display_lines.append(ExtArticleRender.CONTINUED)
                is_partial = True
                break
            display_lines.append(line)
            total_chars += len(line)

        if not is_partial:
            display_lines.append(ExtArticleRender.END)

        lines = []
        summary_lines = self.summary_lines_display
        if summary_lines:
            lines.extend(summary_lines)
            lines.append(ExtArticleRender.END_SUMMARY)
        if display_lines:
            lines.extend(display_lines)

        return '\n\n'.join(lines)
