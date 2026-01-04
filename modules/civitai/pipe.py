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

class Pipe:
    def __init__(self, api_func, filter=None, **kwargs):
        self.api_func = api_func
        self.kwargs = kwargs
        self.filter = filter

        self.current_index = 0
        self.cursor = Cursor()
        self.values = []

    def fetch(self, count):
        while len(self.values) < count and not self.cursor.reached_end():
            limit = min(200, count - len(self.values))
            print(f'Sent request - cursor: {self.cursor.get()}')
            
            new_values, metadata = self.api_func(**self.kwargs, limit=limit, cursor=self.cursor.get())
            self.values.extend([value for value in new_values if self.filter is None or self.filter(value)])
            
            self.cursor.update(metadata.get("nextCursor", None))
        print(self.values)
        return self.values
    
    def next(self, count):
        pass                    
