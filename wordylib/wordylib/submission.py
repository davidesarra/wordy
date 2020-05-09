from typing import List


class Submission:
    def __init__(self, player: str, solution: List[List[str]]) -> None:
        self.player = player
        self.solution = [[character.upper() for character in line] for line in solution]

    def get_letters(self) -> List[str]:
        return [
            character
            for line in self.solution
            for character in line
            if character != " "
        ]

    def get_words(self) -> List[str]:
        row_words = self._parse_words_by_line(solution=self.solution)
        transposed_solution = [list(line) for line in zip(*self.solution)]
        column_words = self._parse_words_by_line(solution=transposed_solution)
        return row_words + column_words

    @staticmethod
    def _parse_words_by_line(solution: List[List[str]]) -> List[str]:
        words = []
        word_stack = []

        def clear_word_stack():
            nonlocal word_stack
            word = "".join(word_stack)
            if len(word) > 1:  # we ignore one-character words
                words.append(word)
            word_stack = []

        for line in solution:
            for character in line:
                if character == " ":
                    clear_word_stack()
                else:
                    word_stack.append(character)
            clear_word_stack()

        return words
