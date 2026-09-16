from enum import StrEnum


class UserRole(StrEnum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"


class UserOnlineStatus(StrEnum):
    ONLINE = "ONLINE"
    RECENTLY_ONLINE = "RECENTLY_ONLINE"
    LONG_AGO = "LONG_AGO"
