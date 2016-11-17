import time


try:
    monotonic = time.perf_counter
except AttributeError:
    # Python 3.2 and below
    monotonic = time.clock
