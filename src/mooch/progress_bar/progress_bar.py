from __future__ import annotations

import sys
import time


class ProgressBar:
    """Progress bar with optional color gradient, ETA, percentage, and step display.

    Args:
        total (int): The total number of steps for completion.
        width (int, optional): The width of the progress bar in characters. Default is 50.
        prefix (str, optional): String to display before the progress bar. Default is "".
        suffix (str, optional): String to display after the progress bar. Default is "".
        symbol (str, optional): Character used to fill the progress bar. Default is "█".
        empty_symbol (str, optional): Character used for the empty part of the progress bar. Default is " ".
        start_immediately (bool, optional): If True, start rendering immediately. Default is True.

    Methods:
        start() -> None:
            Start rendering the progress bar.

        update(step: int = 1) -> None:
            Increment the progress bar by the given number of steps and render the update.

        finish() -> None:
            Render the final state of the progress bar.

    """

    def __init__(  # noqa: PLR0913
        self,
        total: int,
        *,
        width: int = 50,
        prefix: str = "Progress",
        suffix: str = "",
        symbol: str = "█",
        empty_symbol: str = " ",
        start_immediately: bool = True,
    ):
        self.total: int = total
        self.width: int = width
        self.prefix: str = prefix
        self.suffix: str = suffix
        self.symbol: str = symbol
        self.empty_symbol: str = empty_symbol

        self._stream = sys.stdout

        self._current = 0
        self._last_line_len = 0
        self.is_started = False
        self.is_finished = False

        if start_immediately:
            self._start()

    def update(self, step: int = 1) -> None:
        self._current += step
        self._render()

    def finish(self) -> None:
        self._current = self.total
        self._render()

    def _start(self) -> None:
        if self.is_started or self.is_finished:
            msg = "Progress bar has already been started or finished."
            raise RuntimeError(msg)

        self._start_time = time.time()
        self.is_started = True
        self._stream.write("\033[?25l")  # Hide cursor
        self._stream.flush()
        self._render()

    def _finish(self) -> None:
        self.is_finished = True
        self._last_line_len = 0
        self._stream.write("\n")
        self._stream.flush()

    def get_progress(self) -> float:
        now = time.time()
        elapsed_time = now - self._start_time
        progress_float = min(self._current / self.total, 1.0)

        return (elapsed_time, progress_float)

    def _render_bar(self, progress_float: float) -> str:
        filled_length = int(self.width * progress_float)
        empty_length = self.width - filled_length
        return self.symbol * filled_length + self.empty_symbol * empty_length

    def _render(self) -> None:
        if self.is_finished:
            msg = "Progress bar is already 100% complete."
            raise RuntimeError(msg)

        elapsed_time, progress_float = self.get_progress()

        bar = self._render_bar(progress_float)
        percent = f"{int(progress_float * 100):3d}%"
        steps = f"{str(self._current).rjust(len(str(self.total)))}/{self.total}"

        eta = "ETA N/A"
        if self._current > 0:
            rate = elapsed_time / self._current
            remaining = self.total - self._current
            eta_seconds = float(rate * remaining)
            eta = f"ETA {self.format_time(eta_seconds)}"

        line = f"\r{self.prefix} [{bar}] {percent} {steps} | {eta} {self.suffix}"
        line = line.ljust(self._last_line_len)
        self._last_line_len = len(line)
        self._stream.write(line)
        self._stream.flush()

        if self._current >= self.total:
            self._finish()

    def format_time(self, seconds: float) -> str:
        if seconds < 10:  # noqa: PLR2004
            return f"{seconds:.1f}s"
        seconds = round(seconds)
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)

        if hours:
            return f"{hours}h {mins}m {secs}s"
        if mins:
            return f"{mins}m {secs}s"
        return f"{secs}s"
