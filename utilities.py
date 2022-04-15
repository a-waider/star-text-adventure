import sys
import time
from typing import Tuple


def text_print(text, sleep_time: int = 0.01):
    for i in text:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(sleep_time)


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
