"""Test utilities for the configurable_variables app."""

from contextlib import contextmanager
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, MagicMock, Mock, _patch, patch

from configurable_variables.interface import NoSuchVariableError, app_config

if TYPE_CHECKING:
    from collections.abc import Generator


@contextmanager
def patch_app_config(mock_config: dict) -> "Generator[_patch[AsyncMock | MagicMock]]":
    """Patch the app_config.get method to return values from the provided dict, bypassing encryption and db access.

    Example usage:
    ```python
    from configurable_variables.test.utils import patch_app_config

    @pytest.fixture()
    def file_manager() -> FileManager:
        with patch_app_config({"GOOGLE_CREDENTIALS_JSON": "{}"}):
            return FileManager(bucket_name=S3_BUCKET)
    ```

    Can be called in nested contexts to override multiple values:
    ```python
    with patch_app_config({"TEST_KEY1": "123", "TEST_KEY2": "456"}):
        assert app_config.get("TEST_KEY1") == "123"
        assert app_config.get("TEST_KEY2") == "456"

        with patch_app_config({"TEST_KEY2": "789", "TEST_KEY3": "012"}):
            assert app_config.get("TEST_KEY1") == "123"
            assert app_config.get("TEST_KEY2") == "789"
            assert app_config.get("TEST_KEY3") == "012"
    ```

    If you need to temporarily stop the patch, you can use the `stop` method on the returned patcher:
    ```python
    @pytest.fixture()
    def app_config_fixture() -> "Generator[_patch[AsyncMock | MagicMock]]":
        with patch_app_config({"TEST_KEY": "test_value"}) as patcher:
            yield patcher


    @pytest.mark.django_db()
    def test_patch_app_config_used_in_fixture_can_be_stopped(app_config_fixture: "_patch[AsyncMock | MagicMock]") -> None:
        assert app_config.get("TEST_KEY") == "test_value"

        app_config_fixture.stop()

        with pytest.raises(NoSuchVariableError):
            app_config.get("TEST_KEY")
    """
    existing_get = app_config.get if isinstance(app_config.get, Mock) else None

    patcher = patch.object(app_config, "get")
    mock_get = patcher.start()

    def lookup(key: str) -> str | None:
        if key in mock_config:
            # this key is in our mock config
            return mock_config[key]

        # if there is a higher level patch, try getting the key from that
        if existing_get:
            return existing_get(key)

        # if no key and no higer level patch, this key hasn't been mocked
        msg = f"No configurable variable found with name {key}"
        raise NoSuchVariableError(msg)

    mock_get.side_effect = lookup

    try:
        yield patcher
    finally:
        patcher.stop()
