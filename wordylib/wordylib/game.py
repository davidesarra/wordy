from typing import Set


class Game:
    def __init__(self):
        self._players: Set[str] = set()

    @property
    def players(self) -> Set[str]:
        return {*self._players}

    def add_player(self, player: str) -> None:
        if player in self._players:
            raise ValueError(f"{player} is already playing")
        self._players.add(player)
