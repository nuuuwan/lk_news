import asyncio
import random
import time
from functools import cache

from googletrans import Translator as GoogleTranslator
from utils import Log

log = Log("Translator")

GOOGLE_TRANSLATOR = GoogleTranslator()


class Translator:
    MAX_DELAY_S = 0.5

    @staticmethod
    def sleep():
        time_sleep_s = random.random() * Translator.MAX_DELAY_S
        log.debug(f"😴 {time_sleep_s:.2f}s")
        time.sleep(time_sleep_s)

    def __init__(self, src: str, dest: str):
        self.src = src
        self.dest = dest

    async def translate_single(self, text: str) -> str:
        try:
            Translator.sleep()
            result = await GOOGLE_TRANSLATOR.translate(
                text, src=self.src, dest=self.dest
            )
            if result:
                log.debug(
                    f'"{text}" ({self.src})'
                    + f' -> "{result.text}" ({self.dest})'
                )
                return result.text
        except Exception as e:
            log.error(
                f'Could not translate "{text}"'
                + f" ({self.src}) to {self.dest}: {e}"
            )
        return None

    async def translate(self, text) -> str:
        DELIM = ". "
        sentences = text.split(DELIM)
        translated_sentences = []
        for sentence in sentences:
            translated_sentence = await self.translate_single(sentence.strip())
            if translated_sentence is None:
                translated_sentence = sentence
            translated_sentences.append(translated_sentence)
        return DELIM.join(translated_sentences)


if __name__ == "__main__":
    t_en_to_si = Translator("en", "si")
    print(asyncio.run(t_en_to_si.translate("Hello. How are you?")))
