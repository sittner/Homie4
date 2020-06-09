import time
from threading import Event, Thread
import traceback

import logging

logger = logging.getLogger(__name__)


class Repeating_Timer(object):
    """Repeat `function` every `interval` milliseconds."""

    def __init__(self, interval):
        self.interval = int(interval * 1000000)

        self.start = time.monotonic_ns()
        self.event = Event()

        self.thread = Thread(target=self._target)
        self.thread.setDaemon(True)
        self.thread.start()

        self.callbacks = []

    def _target(self):
        while not self.event.wait(self._time * 0.000000001):
            for callback in self.callbacks:
                try:
                    callback()
                except Exception as e:
                    logger.error("Error in timer callback: {}  {}".format(e,traceback.format_exc()))

    @property
    def _time(self):
        return self.interval - ((time.monotonic_ns() - self.start) % self.interval)

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def stop(self):
        self.event.set()
        self.thread.join()

