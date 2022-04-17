import time
from typing import Tuple


def print(text: 'list[str]' = "", sleep_time: int = 0.01):
    # pylint: disable=cyclic-import
    from builtins import print

    from main import TEST_MODE

    def text_print(text: str):
        for character in text:
            print(character, end="")
            if not TEST_MODE[0]:
                time.sleep(sleep_time)

    if isinstance(text, list):
        for sentence in text:
            text_print(sentence)
            if not TEST_MODE[0]:
                input(" <enter>")
    elif isinstance(text, str):
        text_print(text)
        print()
    else:
        text_print(str(text))


def trailing_s(name: str) -> str:
    if str(name).endswith("s"):
        return f"{name}'"
    return f"{name}'s"


def colored_health(health: int, max_health: int) -> 'Tuple[str,str]':
    if health/max_health < 0.3:
        health_color = "yellow"
        heart_icon = "💛"
    elif health/max_health < 0.1:
        health_color = "red"
        heart_icon = "❤"
    else:
        health_color = "green"
        heart_icon = "💚"
    return heart_icon, health_color
