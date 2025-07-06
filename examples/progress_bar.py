import time

from mooch import ColoredProgressBar

if __name__ == "__main__":
    pb = ColoredProgressBar(
        total=5,
    )

    for _ in range(5):
        time.sleep(1.5)
        pb.update()
