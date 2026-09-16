from enum import StrEnum


class UserRole(StrEnum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"


class UserPresenceStatus(StrEnum):
    ONLINE = "ONLINE"
    LAST_ONLINE = "LAST_ONLINE"
    RECENTLY = "RECENTLY"
    LONG_AGO = "LONG_AGO"
