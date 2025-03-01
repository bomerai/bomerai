"""Collection of functions to encrypt and decrypt data."""

import hashlib
from base64 import urlsafe_b64encode

from cryptography.fernet import Fernet, MultiFernet

from core.types.environment import env

__all__ = ["key_hash", "encrypt", "decrypt", "rotate"]


def _transform_key(key: bytes) -> bytes:
    """Transform the given key into a hash with a fixed length."""
    return urlsafe_b64encode(hashlib.sha256(key).digest())


def key_hash(key: bytes | None = None) -> bytes:
    """Get the hash of the given key, using the DJANGO_SECRET_KEY as default."""
    if key is None:
        key = bytes(env.str("DJANGO_SECRET_KEY"), "utf-8")
    return _transform_key(key)


def encrypt(value: bytes) -> bytes:
    """Encrypt the given value using the DJANGO_SECRET_KEY."""
    f = Fernet(key_hash())
    return f.encrypt(value)


def decrypt(value: bytes) -> str:
    """Decrypt the given value using the DJANGO_SECRET_KEY."""
    f = Fernet(key_hash())
    return str(f.decrypt(value), "utf-8")


def rotate(value: bytes, old_key: bytes, new_key: bytes) -> bytes:
    """Rotate the encryption key of the given value."""
    old_key_transformed = _transform_key(old_key)
    new_key_transformed = _transform_key(new_key)
    mf = MultiFernet([Fernet(new_key_transformed), Fernet(old_key_transformed)])
    return mf.rotate(value)
