from enum import StrEnum


class RateLimitScope(StrEnum):
    LOGIN_IP = "login_ip"
    LOGIN_EMAIL = "login_email"
    PASSWORD_RESET_REQUEST = "password_reset_request"
    PASSWORD_RESET_CONFIRM = "password_reset_confirm"
