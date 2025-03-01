from typing import TYPE_CHECKING

import pytest

from configurable_variables.interface import NoSuchVariableError, app_config
from configurable_variables.test.utils import patch_app_config

if TYPE_CHECKING:
    from collections.abc import Generator
    from unittest.mock import AsyncMock, MagicMock, _patch


@pytest.mark.django_db()
def test_patch_app_config_allows_mocking() -> None:
    with pytest.raises(NoSuchVariableError):
        app_config.get("TEST_KEY")

    with patch_app_config({"TEST_KEY": "test_value"}):
        assert app_config.get("TEST_KEY") == "test_value"

    with pytest.raises(NoSuchVariableError):
        app_config.get("TEST_KEY")


@pytest.mark.django_db()
def test_patch_app_config_allows_nested_calls() -> None:
    with pytest.raises(NoSuchVariableError):
        app_config.get("TEST_KEY")

    with patch_app_config({"TEST_KEY1": "123", "TEST_KEY2": "456"}):
        assert app_config.get("TEST_KEY1") == "123"
        assert app_config.get("TEST_KEY2") == "456"

        with patch_app_config({"TEST_KEY2": "789", "TEST_KEY3": "012"}):
            assert app_config.get("TEST_KEY1") == "123"
            assert app_config.get("TEST_KEY2") == "789"
            assert app_config.get("TEST_KEY3") == "012"


@pytest.mark.django_db()
def test_patch_app_config_only_mocks_given_keys() -> None:
    with pytest.raises(NoSuchVariableError):
        app_config.get("TEST_KEY")

    with patch_app_config({"OTHER_KEY": "other_value"}):
        assert app_config.get("OTHER_KEY") == "other_value"

        with pytest.raises(NoSuchVariableError):
            app_config.get("TEST_KEY")


@pytest.mark.django_db()
def test_patch_app_config_can_be_stopped() -> None:
    with pytest.raises(NoSuchVariableError):
        app_config.get("TEST_KEY")

    with patch_app_config({"TEST_KEY": "test_value"}) as patcher:
        assert app_config.get("TEST_KEY") == "test_value"

        patcher.stop()

        with pytest.raises(NoSuchVariableError):
            app_config.get("TEST_KEY")


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


@pytest.mark.django_db()
def test_patch_app_config_stops_on_exception() -> None:
    with pytest.raises(NoSuchVariableError):
        app_config.get("TEST_KEY")

    class TestException(Exception): ...

    try:
        # patch the app config, then raise an exception as if a test failed
        with patch_app_config({"TEST_KEY": "test_value"}):
            assert app_config.get("TEST_KEY") == "test_value"
            raise TestException  # noqa: TRY301
    except TestException:
        pass

    with pytest.raises(NoSuchVariableError):
        app_config.get("TEST_KEY")
