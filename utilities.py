import sys
import time


def text_print(text, sleep_time: int = 0.01):
    for i in text:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(sleep_time)


def trailing_s(name: str) -> str:
    if str(name).endswith("s"):
        return f"{name}'"
    return f"{name}'s"
