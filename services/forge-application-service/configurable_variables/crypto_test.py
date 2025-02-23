import base64
from unittest.mock import patch

import pytest
from cryptography.fernet import InvalidToken

from configurable_variables import crypto


def test_key_hash_uses_django_secret_key() -> None:
    with patch("configurable_variables.crypto.env") as mock_env:
        mock_env.str.return_value = "key"
        hashed_key = crypto.key_hash()
    assert hashed_key == b"LHDhK3oGRvkiefQnx7OOczTY5Tic_xZ6HcMOc_gmtoM="
    assert len(base64.urlsafe_b64decode(hashed_key)) == 32


def test_key_hash_uses_given_key() -> None:
    hashed_key = crypto.key_hash(b"given_key")
    assert hashed_key == b"CJDjDO7iGREveh7Iaie80KEhCIByOLHaiw3MWs4EWww="
    assert len(base64.urlsafe_b64decode(hashed_key)) == 32


def test_encrypt() -> None:
    with patch("configurable_variables.crypto.env") as mock_env:
        mock_env.str.return_value = "key"
        encrypted1 = crypto.encrypt(b"value")

        mock_env.str.return_value = "key2"
        encrypted2 = crypto.encrypt(b"value")

        assert encrypted1 != encrypted2


def test_decrypt() -> None:
    with patch("configurable_variables.crypto.env") as mock_env:
        mock_env.str.return_value = "key"

        encrypted = crypto.encrypt(b"value")
        decrypted = crypto.decrypt(encrypted)

        assert decrypted == "value"


def test_decrypt_raises_invalid_token_exception() -> None:
    with patch("configurable_variables.crypto.env") as mock_env:
        mock_env.str.return_value = "key"

        encrypted = crypto.encrypt(b"value")

        mock_env.str.return_value = "key2"
        with pytest.raises(InvalidToken):
            crypto.decrypt(encrypted)


def test_rotate() -> None:
    old_key = b"key"
    new_key = b"new_key"

    with patch("configurable_variables.crypto.env") as mock_env:
        mock_env.str.return_value = str(old_key, "utf-8")
        orig_encrypted_value = crypto.encrypt(b"value")

    rotated_value = crypto.rotate(orig_encrypted_value, old_key, new_key)

    assert rotated_value != orig_encrypted_value

    with patch("configurable_variables.crypto.env") as mock_env:
        mock_env.str.return_value = str(new_key, "utf-8")
        decrypted_rotated_value = crypto.decrypt(rotated_value)

    assert decrypted_rotated_value == "value"
