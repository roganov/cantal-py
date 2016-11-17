from contextlib import contextmanager

from .counters import Counter
from .levels import Integer
from .clock import monotonic


class RequestTracker(object):
    def __init__(self, group_name, **kwargs):
        self.requests = Counter(group=group_name,
            metric="requests", **kwargs)
        self.duration = Counter(group=group_name,
            metric="total_duration", **kwargs)
        self.errors = Counter(group=group_name,
            metric="errors", **kwargs)
        self.in_progress = Integer(group=group_name,
            metric="in_progress", **kwargs)

    @contextmanager
    def request(self):
        start = monotonic()
        self.in_progress.incr()
        try:
            yield
        except Exception:
            self.errors.incr()
            raise
        finally:
            dur = monotonic() - start
            self.in_progress.decr()
            self.requests.incr()
            self.duration.incr(int(dur * 1000))
