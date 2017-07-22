class BaseWordyError(Exception):
    pass


class BaseGameError(BaseWordyError):
    pass


class InvalidPlayerName(BaseGameError):
    pass


class InvalidWord(BaseGameError):
    pass


class InvalidSubmission(BaseGameError):
    pass


class UnsupportedLanguage(BaseGameError):
    pass


class BaseInterfaceError(BaseWordyError):
    pass


class InvalidTitle(BaseInterfaceError):
    pass
