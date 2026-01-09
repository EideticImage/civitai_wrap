from .filter import Filter


class AndFilter(Filter):
    def __init__(self, *filters):
        self.filters = filters

    def __call__(self, item):
        return all(f(item) for f in self.filters)
    
class OrFilter(Filter):
    def __init__(self, *filters):
        self.filters = filters

    def __call__(self, item):
        return any(f(item) for f in self.filters)