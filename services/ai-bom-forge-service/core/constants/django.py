"""Django specific configuration values."""

from uuid import uuid4

from core.types.environment import env

__all__ = (
    "DJANGO_ALLOWED_HOSTS",
    "DJANGO_CSRF_COOKIE_SAMESITE",
    "DJANGO_CSRF_COOKIE_SECURE",
    "DJANGO_CSRF_HEADER_NAME",
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    "DJANGO_CSRF_USE_SESSIONS",
    "DJANGO_DEBUG",
    "DJANGO_SECRET_KEY",
    "DJANGO_SESSION_COOKIE_SAMESITE",
    "DJANGO_SESSION_COOKIE_SECURE",
    "DJANGO_STATIC_ROOT",
)

DJANGO_ALLOWED_HOSTS = env.json(
    "DJANGO_ALLOWED_HOSTS",
    ["localhost", "[::1]", "127.0.0.1"],
)

DJANGO_DEBUG = env.bool("DJANGO_DEBUG", False)
DJANGO_SECRET_KEY = env.str("DJANGO_SECRET_KEY", str(uuid4()))

DJANGO_SESSION_COOKIE_SAMESITE = env.str(
    "DJANGO_SESSION_COOKIE_SAMESITE",
    default="None",
    validator=lambda val: val in ("Strict", "Lax", "None"),
)

DJANGO_SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", default=True)
DJANGO_SESSION_EXPIRE_AT_BROWSER_CLOSE = env.bool("SESSION_EXPIRE_AT_BROWSER_CLOSE", default=True)

DJANGO_CSRF_COOKIE_SAMESITE = env.str(
    "DJANGO_CSRF_COOKIE_SAMESITE",
    default="None",
    validator=lambda val: val in ("Strict", "Lax", "None"),
)

DJANGO_CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE", True)
DJANGO_CSRF_HEADER_NAME = env.str("DJANGO_CSRF_HEADER_NAME", "HTTP_X_CSRFTOKEN")
DJANGO_CSRF_USE_SESSIONS = env.bool("DJANGO_CSRF_USE_SESSIONS", True)

DJANGO_CSRF_TRUSTED_ORIGINS = env.json(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    [
        "https://localhost:3050",
        "https://protocol-research.development.trialspark.com",
        "https://protocol-research.staging.trialspark.com",
    ],
)

DJANGO_STATIC_ROOT = env.str("DJANGO_STATIC_ROOT", "/srv/http/static")
