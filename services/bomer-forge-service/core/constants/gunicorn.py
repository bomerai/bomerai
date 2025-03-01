"""Gunicorn webserver configuration values."""

from core.types.environment import env

__all__ = (
    "GUNICORN_DOMAIN_SOCKET",
    "GUNICORN_PIDFILE",
    "GUNICORN_PRELOAD_APP",
    "GUNICORN_TIMEOUT",
    "GUNICORN_WORKERS",
)

GUNICORN_DOMAIN_SOCKET = env.str("GUNICORN_DOMAIN_SOCKET", "")
GUNICORN_PIDFILE = env.str("GUNICORN_PIDFILE", "")
GUNICORN_PRELOAD_APP = env.bool("GUNICORN_PRELOAD_APP", True)
GUNICORN_TIMEOUT = env.int("GUNICORN_TIMEOUT", 30)
GUNICORN_WORKERS = env.int("GUNICORN_WORKERS", 1)
