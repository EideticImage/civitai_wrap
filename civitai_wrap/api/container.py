from collections import deque
from threading import Lock
import time

class ContainerIterator:
    def __init__(self, container: "Container"):
        self.container = container
        self.index = 0

    def __next__(self):
        while self.index >= len(self.container):
            if self.container.is_full(): raise StopIteration
            time.sleep(0.5)

        self.index += 1
        return self.container.get_value(self.index-1)

    def __iter__(self):
        return self


class Container:
    def __init__(self):
        self._is_full = False
        self._index = 0
        self._values = deque()
        self._lock = Lock()

    def __len__(self):
        with self._lock:
            return len(self._values)

    def get_value(self, index):
        with self._lock:
            if index >= len(self._values): return 
            return self._values[index]

    def fill(self):
        with self._lock:
            self._is_full = True
        return self

    def is_full(self):
        with self._lock:
            return self._is_full

    def append(self, value):
        with self._lock:
            self._values.append(value)

    def extend(self, values):
        with self._lock:
            self._values.extend(values)
    
    def __iter__(self):
        return ContainerIterator(self)
