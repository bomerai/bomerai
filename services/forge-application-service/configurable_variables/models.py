"""Model to store configurable variables for the app."""

from typing import Any

import structlog
from asgiref.sync import async_to_sync
from cryptography.fernet import InvalidToken
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from configurable_variables.crypto import decrypt, encrypt, key_hash, rotate

logger = structlog.getLogger(__name__)


class ConfigurableVariable(models.Model):
    """Model to store configurable variables for the app."""

    name = models.CharField(max_length=255, unique=True)
    enc_key_hash = models.CharField(max_length=255)
    encrypted_value = models.BinaryField(editable=True)

    def __str__(self) -> str:
        """Return the name of the variable."""
        return self.name

    def can_decrypt(self) -> bool:
        """Return whether the value can be decrypted with the current DJANGO_SECRET_KEY."""
        try:
            decrypt(bytes(self.encrypted_value))
        except InvalidToken:
            return False
        return True

    def rotate(self, old_key: bytes, new_key: bytes) -> None:
        """Rotate the encryption key of the variable."""
        self.encrypted_value = rotate(bytes(self.encrypted_value), old_key, new_key)
        self.enc_key_hash = key_hash(new_key).decode("utf-8")
        self.save()

    @property
    def value(self) -> str:
        """Return the value of the variable."""
        return decrypt(bytes(self.encrypted_value))

    @value.setter
    def value(self, value: str) -> None:
        """Set the value of the variable."""
        self.encrypted_value = encrypt(value.encode("utf-8"))
        self.enc_key_hash = key_hash().decode("utf-8")


@receiver(post_save, sender=ConfigurableVariable)
def refresh_db_constants(
    sender: Any, instance: Any, **kwargs: dict
) -> None:  # noqa: ARG001
    """Refresh the `constants` object when a `ConfigurableVariable` is saved."""
    logger.info("Refreshing constants")

    from core.db_constants import constants

    async_to_sync(constants.set_values)()
