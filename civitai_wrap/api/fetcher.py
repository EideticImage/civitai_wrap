from dataclasses import dataclass
import time

from civitai_wrap import Logger
from .container import Container
from .cursor import Cursor
import threading


@dataclass
class RetryConfig:
    max_attempts = 6
    backoff = 0.25


class MaxRetryExceeded(Exception):
    pass


class Fetcher:
    def __init__(self, api_func, filter=None, **kwargs):
        self.api_func = api_func
        self.kwargs = kwargs
        self.filter = filter

        self.cursor = Cursor()
        self.retry_config = RetryConfig()
        self.thread = None

    def fetch(self, container=None, count=None):
        if self.thread:
            raise Exception

        if container is None:
            container = Container()
        if count is None:
            count = float("inf")

        self.thread = threading.Thread(
            target=self._fetch, args=(container, count), daemon=True
        )
        self.thread.start()

    def _fetch(self, container, count):
        logger = Logger(count).reprint()

        while len(container) < count and not self.cursor.reached_end():
            limit = min(200, count - len(container))
            try:
                new_values, metadata = self._safe_api_func(limit)
            except:
                return container.fill()
            filtered_values = [
                value
                for value in new_values
                if self.filter is None or self.filter(value)
            ]
            container.extend(filtered_values)
            logger.on_request_results(len(filtered_values)).reprint()

            self.cursor.update(metadata.get("nextCursor", None))
        return container.fill()

    def _safe_api_func(self, limit):
        delay = self.retry_config.backoff
        max_attempts = self.retry_config.max_attempts
        for attempt in range(max_attempts):
            try:
                return self.api_func(
                    **self.kwargs, limit=limit, cursor=self.cursor.get()
                )
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise MaxRetryExceeded() from e
                time.sleep(delay)
                delay *= 2
