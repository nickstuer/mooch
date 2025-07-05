import time

from mooch import ProgressBar

if __name__ == "__main__":
    pb = ProgressBar(
        total=55,
        prefix="Progress",
    )

    for _ in range(666):
        time.sleep(0.1)
        pb.update()

time.sleep(5)
