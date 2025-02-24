"""Utils related to users."""

from django.contrib.auth.models import User

SYSTEM_USER_USERNAME = "system_user"


async def get_system_user() -> User:
    """Return the system user."""
    return await User.objects.aget(username=SYSTEM_USER_USERNAME)
