from collections import deque
from datetime import UTC, datetime, timedelta

from ..config import settings

_MAX_TRACKED_KEYS = 10000


class RateLimiter:
    def __init__(self, max_hits: int, window_minutes: int) -> None:
        self._max_hits = max_hits
        self._window = timedelta(minutes=window_minutes)
        self._hits: dict[str, deque[datetime]] = {}

    def _actual_hits(self, key: str) -> deque[datetime]:
        hits = self._hits.get(key)
        if hits is None:
            return deque()

        threshold = datetime.now(UTC) - self._window
        while hits and hits[0] <= threshold:
            hits.popleft()

        if not hits:
            del self._hits[key]

        return hits

    def _sweep(self) -> None:
        for key in list(self._hits):
            self._actual_hits(key)

    def is_blocked(self, key: str) -> bool:
        return len(self._actual_hits(key)) >= self._max_hits

    def retry_after_seconds(self, key: str) -> int:
        hits = self._actual_hits(key)
        if not hits:
            return 0

        left = hits[0] + self._window - datetime.now(UTC)
        return max(1, int(left.total_seconds()))

    def hit(self, key: str) -> None:
        if len(self._hits) >= _MAX_TRACKED_KEYS:
            self._sweep()

        self._actual_hits(key)
        self._hits.setdefault(key, deque()).append(datetime.now(UTC))

    def reset(self, key: str) -> None:
        self._hits.pop(key, None)


login_email_rate_limiter = RateLimiter(
    max_hits=settings.LOGIN_MAX_ATTEMPTS_PER_EMAIL,
    window_minutes=settings.LOGIN_ATTEMPTS_WINDOW_MINUTES,
)

login_ip_rate_limiter = RateLimiter(
    max_hits=settings.LOGIN_MAX_ATTEMPTS_PER_IP,
    window_minutes=settings.LOGIN_ATTEMPTS_WINDOW_MINUTES,
)

password_reset_request_rate_limiter = RateLimiter(
    max_hits=settings.PASSWORD_RESET_REQUEST_MAX_PER_IP,
    window_minutes=settings.PASSWORD_RESET_REQUEST_WINDOW_MINUTES,
)

password_reset_confirm_rate_limiter = RateLimiter(
    max_hits=settings.PASSWORD_RESET_CONFIRM_MAX_PER_IP,
    window_minutes=settings.PASSWORD_RESET_CONFIRM_WINDOW_MINUTES,
)
