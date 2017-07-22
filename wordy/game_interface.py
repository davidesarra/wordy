import time
from typing import Any, List

import terminaltables

import wordy.utils
from wordy.errors import InvalidTitle
from wordy.interface import Interface


class GameInterface(Interface):
    def get_players_names(self):
        return self.get_list_of_strings(
            message="\nEnter the player names (separated by commas): ",
            separator=",",
            strip_whitespace=True,
            mandatory=True,
        )

    def get_n_rounds(self):
        return self.get_integer(
            message=(
                "\nEnter the number of rounds to play "
                "or leave blank to decide later: "
            ),
            mandatory=False,
        )

    def get_round_time(self):
        return self.get_integer(
            message="\nEnter the duration of each round in seconds: ", mandatory=True
        )

    def get_language(self):
        return self.get_string(
            message=(
                "\nEnter the language in which you want to play "
                "(e.g. en for English): "
            ),
            mandatory=True,
        ).lower()

    def get_whether_play_new_round(self, played_rounds):
        return self.get_boolean(
            message=(
                f"\nYou played {played_rounds} rounds. "
                f"Do you want to play another round? "
            ),
            true_values={"YES", "yes", "Y", "y"},
            false_values={"NO", "no", "N", "n"},
        )

    def get_solutions(self, player_names):
        default_solution = [" "]

        def pad_lines(lines: List[str]) -> List[str]:
            max_columns = max(len(line) for line in lines)
            padded_lines = []
            for line in lines:
                columns = len(line)
                padding = " " * (max_columns - columns)
                padded_line = f"{line}{padding}"
                padded_lines.append(padded_line)
            return padded_lines

        def get_words_grid(solution: List[str]) -> List[List[str]]:
            padded_lines = pad_lines(lines=solution)
            return [list(line) for line in padded_lines]

        solutions_by_player = {}
        for player_name in player_names:
            prompt = f"{player_name}, enter your solution:"
            solution = wordy.utils.multiline_input(prompt=prompt) or default_solution
            words_grid = get_words_grid(solution=solution)
            solutions_by_player[player_name] = words_grid
        return solutions_by_player

    def get_if_ready_for_next_round(self):
        self.get_string(
            message=("\nHit <Enter> when you are ready " "to play the next round..."),
            mandatory=False,
        )
        return True

    @staticmethod
    def show_game_intro():
        print(
            "\n\n\n\t################### WORDY ###################"
            "\n\tEach round a number of letter is drawn. Your "
            "\n\tobjective is to compose several words using "
            "\n\tthese letters so that the words are connected "
            "\n\tto one another and each letter is used once. "
            "\n\tEach letter is associated to a score, which "
            "\n\tleads to the player score. Words must have at "
            "\n\tleast two characters.\n"
        )

    @staticmethod
    def show_new_round(round_number):
        title = f"ROUND #{round_number}"
        header = Header(title=title)
        print(f"\n\n\n{header}\n")

    @staticmethod
    def show_letter_draw(letter_draw):
        message = ""
        for letter in letter_draw:
            message += f"{letter.letter.upper():>2} ({letter.points})"
        print(message)

    @staticmethod
    def show_round_timer(seconds):
        print("\n")
        while seconds:
            formatted_minutes, formatted_seconds = divmod(seconds, 60)
            print(f"\t{formatted_minutes:02d}:{formatted_seconds:02d}", end="\r")
            time.sleep(1)
            seconds -= 1
        # TODO: Play sound when time is up
        print("")
        print("\nTime is up!\n")

    def show_round_scores(self, scores):
        self._show_scores(scores=scores, title="Round Scores")

    def show_running_scores(self, scores):
        self._show_scores(scores=scores, title="Running Scores")

    def show_final_scores(self, scores):
        self._show_scores(scores=scores, title="Final Scores")
        print("Thanks for playing! :)\n")

    def _show_scores(self, scores, title):
        ordered_scores = sorted(
            [(player, score) for player, score in scores.items()],
            key=lambda x: x[1],
            reverse=True,
        )
        formatted_scores = "\n".join(
            [
                f" {rank + 1:>2}) {player}: {score}"
                for rank, (player, score) in enumerate(ordered_scores)
            ]
        )
        self._show(title=title, body=formatted_scores)

    def show_scores_by_word_and_player(self, scores):
        if not scores:
            return
        headers = ["player", "word", "points"]
        rows = [[score[header] for header in headers] for score in scores]
        sorted_rows = sorted(rows, key=lambda row: (-row[2], row[1], row[0]))
        table = terminaltables.AsciiTable([headers, *sorted_rows]).table
        self._show(title="Word Scores", body=table)

    @staticmethod
    def _show(title, body):
        header = Header(title=title)
        print(f"\n{header}\n{body}\n")

    @staticmethod
    def show_error(player: str, error: Any) -> None:
        print(f"\n{player}: {error}")


class Header:
    _STYLE = "="
    _TITLE_TO_LENGTH_RATIO = 4
    _MAX_TITLE_LENGTH = 65
    _MIN_LENGTH = 25
    _MAX_LENGTH = 80
    _PATTERN = "{decoration} {title} {decoration}{padding}"

    def __init__(self, title):
        self._title = title
        self._validate_title()

    def _validate_title(self):
        if not self._title:
            raise InvalidTitle(f"Title must have at least a character")

        title_length = len(self._title)
        if title_length > self._MAX_TITLE_LENGTH:
            raise InvalidTitle(
                f'Title "{self._title}" is too long'
                f"({title_length} > {self._MAX_TITLE_LENGTH})"
            )

    def __str__(self):
        title_length = len(self._title)
        spacing_length = self._PATTERN.count(" ")
        raw_header_length = title_length * self._TITLE_TO_LENGTH_RATIO
        header_length = int(
            min(max(raw_header_length, self._MIN_LENGTH), self._MAX_LENGTH)
        )
        decoration_length, padding_length = divmod(
            header_length - title_length - spacing_length, 2
        )
        decoration = self._STYLE * decoration_length
        padding = " " * padding_length
        return self._PATTERN.format(
            decoration=decoration, title=self._title, padding=padding
        )

    def __eq__(self, other):
        return str(self) == str(other)

    def __repr__(self):
        return f'<Header: "{self}">'
