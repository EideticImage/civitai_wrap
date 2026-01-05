import time

class Logger():
    def __init__(self, needed_items):
        self.requests = 0
        self.kept_elements = 0
        self.needed_items = needed_items
        self.start_time = time.time()
    
    def on_request_results(self, kept_items):
        self.kept_elements += kept_items
        self.requests += 1
        return self

    def reprint(self):
        text = (
            "Current Task in progress\n"
            f"    Successful requests:    {self.requests}\n"
            f"    Found items:            {self.kept_elements}/{self.needed_items}\n"
            f"    Time spent:             {self._get_time_since_start()}"
        )

        lines = 4
        print("\033[F\033[K" * lines, end="")
        print(text, end="")
        return self
    
    def _get_time_since_start(self):
        secs = time.time() - self.start_time
        mins = secs // 60
        secs = secs % 60
        return f"{int(mins)} mins {secs:.2f} secs"