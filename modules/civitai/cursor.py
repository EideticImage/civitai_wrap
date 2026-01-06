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