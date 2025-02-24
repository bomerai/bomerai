from unittest.mock import AsyncMock, patch

import pytest
from cryptography.fernet import InvalidToken

from configurable_variables.models import ConfigurableVariable


class TestConfigurableVariable:
    def test___str__(self) -> None:
        model = ConfigurableVariable(
            name="test-name", enc_key_hash="test-hash", encrypted_value=b"test-value"
        )

        assert str(model) == "test-name"

    def test_can_decrypt_success(self) -> None:
        model = ConfigurableVariable(
            name="test-name", enc_key_hash="test-hash", encrypted_value=b"test-value"
        )
        with patch("configurable_variables.models.decrypt") as mock_decrypt:
            mock_decrypt.return_value = "success"

            assert model.can_decrypt() is True

            assert mock_decrypt.call_count == 1
            assert mock_decrypt.call_args[0] == (b"test-value",)

    def test_can_decrypt_failure(self) -> None:
        model = ConfigurableVariable(
            name="test-name", enc_key_hash="test-hash", encrypted_value=b"test-value"
        )
        with patch("configurable_variables.models.decrypt") as mock_decrypt:
            mock_decrypt.side_effect = InvalidToken

            assert model.can_decrypt() is False

            assert mock_decrypt.call_count == 1
            assert mock_decrypt.call_args[0] == (b"test-value",)

    @pytest.mark.django_db()
    def test_rotate(self) -> None:
        model = ConfigurableVariable(
            name="test-name", enc_key_hash="test-hash", encrypted_value=b"test-value"
        )
        with (
            patch("configurable_variables.models.rotate") as mock_rotate,
            patch("configurable_variables.models.key_hash") as mock_key_hash,
            patch(
                "core.db_constants.constants", AsyncMock()
            ) as mock_refresh_db_constants,
        ):
            mock_rotate.return_value = b"new-value"
            mock_key_hash.return_value.decode.return_value = "new-hash"
            model.rotate(b"old-key", b"new-key")

            assert mock_rotate.call_count == 1
            assert mock_rotate.call_args[0] == (b"test-value", b"old-key", b"new-key")

            assert model.encrypted_value == b"new-value"
            assert model.enc_key_hash == "new-hash"

            mock_refresh_db_constants.set_values.assert_called_once()

    def test_value_getter(self) -> None:
        model = ConfigurableVariable(
            name="test-name", enc_key_hash="test-hash", encrypted_value=b"test-value"
        )
        with patch("configurable_variables.models.decrypt") as mock_decrypt:
            mock_decrypt.return_value = "success"

            assert model.value == "success"

            assert mock_decrypt.call_count == 1
            assert mock_decrypt.call_args[0] == (b"test-value",)

    def test_value_setter(self) -> None:
        model = ConfigurableVariable(
            name="test-name", enc_key_hash="test-hash", encrypted_value=b"test-value"
        )
        with (
            patch("configurable_variables.models.encrypt") as mock_encrypt,
            patch("configurable_variables.models.key_hash") as mock_key_hash,
        ):
            model.value = "success"

            assert mock_encrypt.call_count == 1
            assert mock_encrypt.call_args[0] == (b"success",)
            assert model.encrypted_value == mock_encrypt.return_value
            assert model.enc_key_hash == mock_key_hash.return_value.decode.return_value
