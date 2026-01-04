from dataclasses import dataclass
import time

class Cursor:
    def __init__(self):
        self._was_updated = False
        self._cursor = None

    def get(self):
        return self._cursor

    def update(self, cursor):
        self._was_updated = True
        self._cursor = cursor
    
    def reached_end(self):
        return self._was_updated and self._cursor is None


@dataclass
class RetryConfig:
    max_attempts = 6
    backoff = 0.25

class MaxRetryExceeded(Exception):
    pass

class Pipe:
    def __init__(self, api_func, filter=None, **kwargs):
        self.api_func = api_func
        self.kwargs = kwargs
        self.filter = filter

        self.current_index = 0
        self.cursor = Cursor()
        self.values = []
        
        self.retry_config = RetryConfig()

    def fetch(self, count):
        while len(self.values) < count and not self.cursor.reached_end():
            limit = min(200, count - len(self.values))
            print(f'Sent request - cursor: {self.cursor.get()}')
            try:
                new_values, metadata = self.safe_api_func(limit)
            except:
                return self.values
            self.values.extend([value for value in new_values if self.filter is None or self.filter(value)])
            
            self.cursor.update(metadata.get("nextCursor", None))
        return self.values
    
    def safe_api_func(self, limit):
        delay = self.retry_config.backoff
        max_attempts = self.retry_config.max_attempts
        for attempt in range(max_attempts):
            try:
                return self.api_func(**self.kwargs, limit=limit, cursor=self.cursor.get())
            except Exception as e:
                print(f'Error {e} at attempt {attempt+1}')
                if attempt == max_attempts - 1:
                    raise MaxRetryExceeded() from e
                time.sleep(delay)
                delay *= 2

    def next(self, count):
        pass                    
