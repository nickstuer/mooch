from __future__ import annotations

from mooch.progress_bar.progress_bar import ProgressBar

RESET_COLOR = "\033[0m"


class ColoredProgressBar(ProgressBar):
    def __init__(self, *args, **kwargs):  # noqa: ANN002, ANN003
        self.gradient_edge = 0.4  # The point at which the color gradient changes
        self.gradient_edge2 = 0.65  # The point at which the color gradient changes again
        super().__init__(*args, **kwargs)

    def _render_bar(self, progress_float: float) -> str:
        filled_length = int(self.width * progress_float)
        empty_length = self.width - filled_length
        bar_blocks = []
        for i in range(filled_length):
            progress_pos = i / self.width
            color = self.get_color(progress_pos)
            bar_blocks.append(f"{color}{self.symbol}")

        return "".join(bar_blocks) + RESET_COLOR + self.empty_symbol * empty_length

    def get_color(self, progress: float) -> str:
        """Gradient: soft red → warm gold → deep green (19,154,21)."""
        if progress < self.gradient_edge:
            t = progress / self.gradient_edge
            r = round(230 + (240 - 230) * t)
            g = round(90 + (200 - 90) * t)
            b = round(90 + (100 - 90) * t)

        elif progress < self.gradient_edge2:
            t = (progress - self.gradient_edge) / (self.gradient_edge2 - self.gradient_edge)
            r = round(240 + (120 - 240) * t)
            g = round(200 + (180 - 200) * t)
            b = round(100 + (80 - 100) * t)

        else:
            t = (progress - self.gradient_edge2) / (1 - self.gradient_edge2)
            r = round(120 + (19 - 120) * t)
            g = round(180 + (154 - 180) * t)
            b = round(80 + (21 - 80) * t)

        return f"\033[38;2;{r};{g};{b}m"
