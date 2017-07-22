from typing import List


class Submission:
    def __init__(self, player: str, solution: List[List[str]]) -> None:
        self.player = player
        self.solution = [[character.upper() for character in line] for line in solution]

    def __bool__(self) -> bool:
        for line in self.solution:
            for character in line:
                if character != " ":
                    return True
        return False

    def get_letters(self) -> List[str]:
        return [
            character
            for line in self.solution
            for character in line
            if character != " "
        ]

    def get_words(self) -> List[str]:
        line_words = self._parse_words_by_line(solution=self.solution)
        transposed_solution = [list(line) for line in zip(*self.solution)]
        column_words = self._parse_words_by_line(solution=transposed_solution)
        return [*line_words, *column_words]

    @staticmethod
    def _parse_words_by_line(solution: List[List[str]]) -> List[str]:
        words = []
        word_stack = []
        for line in solution:
            for character in line:
                if character == " ":
                    if word_stack:
                        if len(word_stack) > 1:  # we ignore one-character words
                            word = "".join(word_stack)
                            words.append(word)
                        word_stack = []
                else:
                    word_stack.append(character)
            if word_stack:
                if len(word_stack) > 1:  # we ignore one-character words
                    word = "".join(word_stack)
                    words.append(word)
                word_stack = []
        return words
