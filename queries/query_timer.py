import time

class Timer:
    def __init__(self):
        self._times = []
        self._start = 0

    def start(self) -> None:
        self._start = time.time_ns()

    def end(self) -> None:
        self._times.append((time.time_ns() - self._start) / (1_000_000))
        self._start = 0

    def print(self, desc: str = "") -> None:
        times = [t for t in self._times if t > 0]
        if desc:
            print(desc)
        print(f"avg {sum(times) / len(times):.2f} ms")
        print(f"max {max(times):.2f} ms")
        print(f"min {min(times):.2f} ms")

    def reset(self) -> None:
        self._times = []
        self._start = 0
