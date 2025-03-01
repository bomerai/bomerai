"""uWSGI configuration values."""

from core.types.environment import env

__all__ = ("UWSGI_SOCKET",)

UWSGI_SOCKET = env.str("UWSGI_SOCKET", "")
