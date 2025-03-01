from collections.abc import Generator
from unittest.mock import AsyncMock, PropertyMock, patch

import pytest
from asgiref.sync import async_to_sync
from cryptography.fernet import InvalidToken

from configurable_variables.interface import (
    DecryptionError,
    NoSuchVariableError,
    app_config,
)
from configurable_variables.models import ConfigurableVariable


@pytest.fixture(autouse=True)
def mock_post_save() -> Generator:
    with patch("core.db_constants.constants", AsyncMock()):
        yield


@pytest.fixture()
def configurable_variable() -> ConfigurableVariable:
    """Create a configurable variable."""
    config_var = ConfigurableVariable.objects.create(
        name="TEST_VARIABLE", encrypted_value=b"value"
    )
    config_var.save()
    return config_var


@pytest.mark.django_db()
@pytest.mark.usefixtures("configurable_variable")
def test_get_accesses_value() -> None:
    with patch.object(
        ConfigurableVariable, "value", new_callable=PropertyMock
    ) as mock_value:
        mock_value.return_value = "decrypted_value"
        assert app_config.get("TEST_VARIABLE") == "decrypted_value"
        assert mock_value.call_count == 1


@pytest.mark.django_db()
@pytest.mark.usefixtures("configurable_variable")
def test_get_raises_no_such_variable_error() -> None:
    with pytest.raises(NoSuchVariableError):
        app_config.get("NON_EXISTENT_VARIABLE")


@pytest.mark.django_db()
@pytest.mark.usefixtures("configurable_variable")
def test_get_raises_decryption_error() -> None:
    with patch.object(
        ConfigurableVariable, "value", new_callable=PropertyMock
    ) as mock_value:
        mock_value.side_effect = InvalidToken()
        with pytest.raises(DecryptionError):
            app_config.get("TEST_VARIABLE")
        assert mock_value.call_count == 1


@pytest.mark.django_db()
@pytest.mark.usefixtures("configurable_variable")
def test_aget_accesses_value() -> None:
    with patch.object(
        ConfigurableVariable, "value", new_callable=PropertyMock
    ) as mock_value:
        mock_value.return_value = "decrypted_value"
        assert async_to_sync(app_config.aget)("TEST_VARIABLE") == "decrypted_value"
        assert mock_value.call_count == 1


@pytest.mark.django_db()
@pytest.mark.usefixtures("configurable_variable")
def test_aget_raises_no_such_variable_error() -> None:
    with pytest.raises(NoSuchVariableError):
        async_to_sync(app_config.aget)("NON_EXISTENT_VARIABLE")


@pytest.mark.django_db()
@pytest.mark.usefixtures("configurable_variable")
def test_aget_raises_decryption_error() -> None:
    with patch.object(
        ConfigurableVariable, "value", new_callable=PropertyMock
    ) as mock_value:
        mock_value.side_effect = InvalidToken()
        with pytest.raises(DecryptionError):
            async_to_sync(app_config.aget)("TEST_VARIABLE")
        assert mock_value.call_count == 1
