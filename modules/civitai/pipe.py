class Pipe:
    def __init__(self, api_func, filter=None, **kwargs):
        self.api_func = api_func
        self.kwargs = kwargs
        self.filter = filter

    def fetch(self, count):
        values = []
        cursor = None
        while len(values) < count:
            limit = min(200, count - len(values))
            print('Sent request')
            new_values, metadata = self.api_func(**self.kwargs, limit=limit, cursor=cursor)
            values.extend([value for value in new_values if self.filter is None or self.filter(value)])
            
            cursor = metadata.get("nextCursor", None)
            if cursor is None: return values
        return values