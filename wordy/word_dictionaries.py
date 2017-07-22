import requests

from wordy.errors import UnsupportedLanguage


class Dictionary:
    # BUG: cannot look up languages individually (language flag is bogus)
    # BUG: cannot recognise common typos look ups
    NAME = "Wiktionary"
    _API_URL = "https://{language}.wiktionary.org"
    _API_QUERY_APPENDIX = "/w/api.php?action=query&format=json&titles={word}"
    _INVALID_WORD_ID = "-1"

    def __init__(self, language: str) -> None:
        if not self._is_language_supported(language=language):
            raise UnsupportedLanguage(
                (
                    f"{language} is not supported by dictionary {self.NAME}",
                    f"or connection to dictionary is unavailable.",
                )
            )
        self._language = language

    def __contains__(self, word: str) -> bool:
        url = (self._API_URL + self._API_QUERY_APPENDIX).format(
            language=self._language, word=word.lower()
        )
        matching_word_ids = requests.get(url=url).json()["query"]["pages"].keys()
        return self._INVALID_WORD_ID not in matching_word_ids

    def _is_language_supported(self, language: str) -> bool:
        try:
            url = self._API_URL.format(language=language)
            requests.get(url=url)
            return True
        except requests.ConnectionError:
            return False
