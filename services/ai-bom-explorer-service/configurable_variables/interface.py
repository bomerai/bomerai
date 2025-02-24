"""Public interface for the configurable_variables app."""

from cryptography.fernet import InvalidToken

from configurable_variables.models import ConfigurableVariable

__all__ = ["app_config", "DecryptionError", "NoSuchVariableError"]


class DecryptionError(Exception):
    """Raised when a variable cannot be decrypted."""


class NoSuchVariableError(Exception):
    """Raised when a variable with the given name does not exist."""


class _App_Config:  # noqa: N801
    def get(self, variable_name: str) -> str:
        """Get the value of the named configurable variable.

        If a configurable variable with the given name does not exist, raise a NoSuchVariableError.
        If the variable cannot be decrypted, raise a DecryptionError.
        """
        try:
            return ConfigurableVariable.objects.get(name=variable_name).value
        except ConfigurableVariable.DoesNotExist as e:
            msg = f"No configurable variable found with name {variable_name}"
            raise NoSuchVariableError(msg) from e
        except InvalidToken as e:
            msg = f"Failed to decrypt variable: {variable_name}"
            raise DecryptionError(msg) from e

    async def aget(self, variable_name: str) -> str:
        """Async version of get."""
        try:
            return (await ConfigurableVariable.objects.aget(name=variable_name)).value
        except ConfigurableVariable.DoesNotExist as e:
            msg = f"No configurable variable found with name {variable_name}"
            raise NoSuchVariableError(msg) from e
        except InvalidToken as e:
            msg = f"Failed to decrypt variable: {variable_name}"
            raise DecryptionError(msg) from e


app_config = _App_Config()
