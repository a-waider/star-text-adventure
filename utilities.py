import time
from typing import Tuple


def print(text: 'list[str]' = "", sleep_time: int = 0.01):
    from builtins import print

    def text_print(text: str, sleep_time: int = 0.01):
        for character in text:
            print(character, end="")
            time.sleep(sleep_time)

    if isinstance(text, list):
        for sentence in text:
            text_print(sentence, sleep_time=sleep_time)
            input(" <enter>")
    elif isinstance(text, str):
        text_print(text, sleep_time=sleep_time)
        print()
    else:
        raise Exception


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
