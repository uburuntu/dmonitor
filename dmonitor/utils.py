import time


class Timer:
    def __init__(self, interval: float):
        self.interval = float(interval)
        self.last = 0.

    def start(self):
        self.last = time.monotonic()
        return self

    def acquire(self):
        curr_ts = time.monotonic()
        if self.last + self.interval > curr_ts:
            return False
        self.last = curr_ts
        return True
