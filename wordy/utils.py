from typing import Any, Collection, List, Sequence
from collections import Counter


def multiline_input(prompt: str) -> List[str]:
    """Get multiline input from user.

    The user can terminate the solution by entering an empty line.
    The user cannot edit previously entered lines.

    Args:
        prompt: Prompt message to show to user.

    Returns:
        Lines typed by the user.
    """
    lines: List[str] = []
    while True:
        if not lines and prompt:
            line = input(prompt + "\n")
        else:
            line = input()

        if line:
            lines.append(line)
        else:
            return lines


def has_duplicates(items: Collection) -> bool:
    return len(items) != len(set(items))


def get_duplicates(items: Collection) -> List[Any]:
    items_by_usage = Counter(items)
    return [item for item, usage in items_by_usage.items() if usage > 1]


def join(items: Sequence[str]) -> str:
    """Comma-separate items with the last item preceded by and."""
    if not items:
        return ""
    elif len(items) == 1:
        return items[0]
    joined = ", ".join(items[:-1])
    return f"{joined}, and {items[-1]}"
