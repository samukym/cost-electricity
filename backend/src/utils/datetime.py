from datetime import datetime


class UtilsDateTime:
    def timestampToRoundHour(self, timestamp: int) -> int:
        return int(
            datetime.fromtimestamp(timestamp)
            .replace(minute=0, second=0, microsecond=0)
            .timestamp()
        )