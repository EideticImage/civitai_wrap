from threading import Lock


class DownloadStatus:
    def __init__(self):
        self._progresion: int = 0
        self._total: str = ""
        self._received: str = ""
        self._time_total: str = ""
        self._time_spent: str = ""
        self._time_left: str = ""
        self._current_speed: str = ""
        self._is_completed: bool = False
        self._lock: Lock = Lock()

    def update(self, line) -> bool:
        data = [s for s in line.split(" ") if s != ""]
        if len(data) != 12:
            return False
        try:
            progression = int(data[0])
            total = data[1]
            received = data[3]
            time_total = data[8]
            time_spent = data[9]
            time_left = data[10]
            current_speed = data[11][:-1]
        except:
            return False

        with self._lock:
            self._progresion = progression
            self._total = total
            self._received = received
            self._time_total = time_total
            self._time_spent = time_spent
            self._time_left = time_left
            self._current_speed = current_speed
        return True

    def complete(self):
        with self._lock:
            self._is_completed = True
    
    def is_completed(self):
        with self._lock:
            return self._is_completed

    def to_dict(self) -> dict:
        with self._lock:
            return {
                "progression": self._progresion,
                "total": self._total,
                "received": self._received,
                "time_total": self._time_total,
                "time_spent": self._time_spent,
                "time_left": self._time_left,
                "current_speed": self._current_speed,
                "is_completed": self._is_completed,
            }

    def __str__(self) -> str:
        with self._lock:
            if self._is_completed:
                return (
                    f"Completed | {self._received}/{self._total} "
                    f"in {self._time_spent}"
                )

            return (
                f"{self._progresion:3d}% | "
                f"{self._received}/{self._total} | "
                f"speed: {self._current_speed} | "
                f"elapsed: {self._time_spent} | "
                f"left: {self._time_left}"
            )
