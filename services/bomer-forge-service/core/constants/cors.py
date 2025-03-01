"""Django CORS configuration values."""

from core.types.environment import env

__all__ = (
    "DJANGO_CORS_ALLOWED_ORIGINS",
    "DJANGO_CORS_ALLOW_HEADERS",
    "DJANGO_CORS_ALLOW_CREDENTIALS",
)

DJANGO_CORS_ALLOWED_ORIGINS = env.json(
    "DJANGO_CORS_ALLOWED_ORIGINS",
    [
        "http://localhost:3000",
    ],
)

DJANGO_CORS_ALLOW_CREDENTIALS = env.bool("DJANGO_CORS_ALLOW_CREDENTIALS", True)

DJANGO_CORS_ALLOW_HEADERS = env.json(
    "DJANGO_CORS_ALLOW_HEADERS",
    [
        "Content-Type",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Credentials",
        "accept",
        "accept-encoding",
        "authorization",
        "content-type",
        "dnt",
        "origin",
        "user-agent",
        "x-csrftoken",
        "x-csrf-token",
        "x-requested-with",
    ],
)

CORS_ALLOW_METHODS = env.json(
    "CORS_ALLOW_METHODS",
    [
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS",
        "PATCH",
    ],
)
