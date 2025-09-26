# import time

# from pytgpt.phind import PHIND as bot_cls
from utils import Log

log = Log("Summarizer")


class Summarizer:
    MAX_CHARS = 200
    T_WAIT = 5

    def summarize(self, content_lines: list[str]) -> list[str]:
        # content = "\n".join(content_lines)
        # try:
        #     log.debug(f"😴 Sleeping for {Summarizer.T_WAIT}s...")
        #     time.sleep(Summarizer.T_WAIT)
        #     bot = bot_cls()
        #     summary = bot.chat(
        #         "Summarize the following into "
        #         + f"{Summarizer.MAX_CHARS} characters:"
        #         + f"\n{content}"
        #     )
        # except Exception as e:
        #     log.error(f"Failed to summarize: {e}")
        #     return ""

        # n_before = len(content)
        # n_after = len(summary)
        # log.info(f"Summarized {n_before} -> {n_after} chars.")
        # return summary.split("\n")
        return []


if __name__ == "__main__":
    text = """
The ascension of Junius Richard Jayewardene to the premier seat of political power in 1977 paved the way for a drastic transformation of Sri Lanka’s politico-economic landscape and environment.

J.R. Jayewardene known popularly as “JR” ushered in political, economic, and electoral changes that utterly changed Sri Lanka.  In the words of William Butler Yeats “All changed, changed utterly.”

The advent of JR as Prime Minister in 1977 and as the first Executive President in 1978 saw great changes in three vital spheres. Firstly the economy was liberalised and free enterprise encouraged. Secondly the Westminster model of Parliamentary governance introduced by the British was turned into an executive presidency. Parliament was de-valued. Thirdly the prevailing “first past the post winner” electoral practice was replaced with the proportional representation scheme.
These three changes have utterly changed Sri Lanka. JR’s right hand man or chief deputy in executing the economic changes was his Finance Minister Ronnie de Mel. Ronald Joseph Godfrey de Mel known as Ronnie de Mel and Ronnie, served in the Jayewardene Government as Finance Minister for a continuous stretch of 11 years from 1977 to 1988.  It was Ronnie who was instrumental in establishing a free or capitalist economy in Sri Lanka.

Ronnie de Mel born on 11 April 1925, passed away in Colombo at the age of 98 on 27 February 2024. The veteran politician represented the Devinuwara constituency in Parliament from 1967 to 1989 for a period of 20 years. He later served as Matara district MP from 1994 to 2001. Thereafter he was a national list MP from 2001 to 2004. The jewel in Ronnie de Mel’s parliamentary career crown was his lengthy stint as finance minister. This column focuses on Ronnie de Mel this week.    """  # noqa
    print(Summarizer().summarize(text))
