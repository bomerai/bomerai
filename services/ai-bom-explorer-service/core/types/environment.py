"""OS Environment handler."""

from __future__ import annotations

import json
import re
from base64 import b16decode, b64decode
from dataclasses import dataclass
from os import environ
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Generic, TypeVar, overload

from urlpath import URL

from core.error import EnvironmentValidationFailure, MandatoryEnvironmentVariableMissing

from .json import JsonValueType
from .monostate import Monostate

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping


__all__ = (
    "env",
    "Environment",
    "EnvironmentValueType",
    "JsonValueType",
)


def cast_bool(value: str | bool) -> bool:
    """Convert String value to Boolean.

    :param value: String value with a bool like structure
    :type str:
    :returns: `True` if the lower stripped value is: "1", "true", "yes", "t",
        "y", or "on", otherwise `False`.
    """
    if isinstance(value, bool):
        return value

    return value.strip().lower() in ("1", "true", "yes", "t", "y", "on")


BINARY_REGEX = re.compile(pattern="^[-+]?[0-9#]b[01]+$", flags=re.IGNORECASE)
OCTAL_REGEX = re.compile(pattern="^[-+]?[0]o?[0-7]+$", flags=re.IGNORECASE)
HEX_REGEX = re.compile(pattern="^[-+]?[0]x[0-9a-z]+$", flags=re.IGNORECASE)


def cast_int(value: str | int) -> int:
    if isinstance(value, int):
        return value

    if HEX_REGEX.match(value):
        return int(value, base=16)

    if BINARY_REGEX.match(value):
        return int(value, base=2)

    if OCTAL_REGEX.match(value):
        return int(value, base=8)

    return int(value, base=10)


BASE16_REGEX = re.compile("^[a-fA-F0-9]+$")
BASE64_REGEX = re.compile("^[A-Za-z0-9/+=]+$")


def cast_bytes(value: str | bytes) -> bytes:
    if isinstance(value, bytes):
        return value

    if BASE16_REGEX.match(value):
        return b16decode(value)

    if BASE64_REGEX.match(value):
        return b64decode(value)

    return value.encode(encoding="utf-8")


class _MissingEnvironmentValue:
    pass


T = TypeVar("T", Path, URL, bool, bytes, float, int, str)
A = TypeVar("A", Path, URL, bool, bytes, float, int, str)  # - TypeVar standard naming


@dataclass
class _CastCacheRecord(Generic[T]):
    type: type
    raw_value: str
    cast_value: T
    is_optional: bool


Boolean = bool
Bytes = bytes
Float = float
Integer = int
Json = JsonValueType
Path = Path  # - This is for completeness
String = str
Url = URL


EnvironmentValueType = Boolean | Bytes | Float | Integer | Json | Path | String | Url


class Environment(Monostate):
    """Typed OS Environment."""

    _cast_morphisms: ClassVar[dict[type, Callable]] = {
        Boolean: cast_bool,
        Bytes: cast_bytes,
        Float: Float,
        Integer: cast_int,
        Path: Path,
        String: String,
        URL: URL,
    }

    def __init__(self, source_environment: Mapping | None = None) -> None:
        """Typed OS Environment.

        :param source_environment: Source data for applying typing to as the
            environment, defaults to os.environ
        :type source_environment: Optional[Mapping]
        """
        super().__init__()
        if not getattr(self, "_source_env", None):
            self._source_env = dict((source_environment or environ).items())
            self._cast_cache: dict[str, _CastCacheRecord] = {}

    def _cast(
        self,
        value: String,
        cast_type: type[T],
        validator: Callable[[T], Boolean] | None = None,
    ) -> T:
        cast_morphism = self._cast_morphisms[cast_type]
        cast_value = cast_morphism(value)

        if validator is not None and validator(cast_value) is False:
            raise EnvironmentValidationFailure(cast_value)

        return cast_value

    @overload
    def _typed_read(
        self,
        name: String,
        cast_type: type[T],
        default: T | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[T], Boolean] | None = None,
    ) -> T: ...

    @overload
    def _typed_read(
        self,
        name: String,
        cast_type: type[T],
        default: T | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[T], Boolean] | None = None,
        optional: bool = False,
    ) -> T | None: ...

    def _typed_read(
        self,
        name: String,
        cast_type: type[T],
        default: T | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[T], Boolean] | None = None,
        optional: bool = False,
    ) -> T | T | None:
        if name in self._cast_cache:
            return self._cast_cache[name].cast_value

        raw_value = self._source_env.get(name, default)
        if raw_value is _MissingEnvironmentValue and not optional:
            raise MandatoryEnvironmentVariableMissing(name)

        cast_value = (
            None
            if raw_value is _MissingEnvironmentValue
            else self._cast(raw_value, cast_type, validator)
        )

        self._cast_cache[name] = _CastCacheRecord(
            type=cast_type,
            raw_value=raw_value,
            cast_value=cast_value,
            is_optional=optional or default is not _MissingEnvironmentValue,
        )

        return cast_value

    def set(self, name: String, value: EnvironmentValueType) -> None:
        """Set an environment variable value.

        NB. Performs passthrough to os.environ.

        :param name: Environment variable key.
        :type name: str
        :param value: Environment variable value.
        :type value: :class:`EnvironmentValueType`
        :returns: None
        :type: None
        """
        env_value = str(value)
        environ[name] = env_value
        self._source_env[name] = env_value
        self._cast_cache[name] = _CastCacheRecord(
            type=type(value),
            raw_value=str(value),
            cast_value=value,
            is_optional=False,
        )

    @overload
    def str(
        self,
        name: String,
        default: String | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[String], Boolean] | None = None,
    ) -> String: ...

    @overload
    def str(
        self,
        name: String,
        default: String | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[String], Boolean] | None = None,
        optional: bool = False,
    ) -> String | None: ...

    def str(
        self,
        name: String,
        default: String | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[String], Boolean] | None = None,
        optional: bool = False,
    ) -> String | String | None:
        """Read a value from the Environment as a str value."""
        return self._typed_read(name, String, default, validator, optional)

    @overload
    def int(
        self,
        name: String,
        default: Integer | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Integer], Boolean] | None = None,
    ) -> Integer: ...

    @overload
    def int(
        self,
        name: String,
        default: Integer | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Integer], Boolean] | None = None,
        optional: bool = False,
    ) -> Integer | None: ...

    def int(
        self,
        name: String,
        default: Integer | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Integer], Boolean] | None = None,
        optional: bool = False,
    ) -> Integer | Integer | None:
        """Read a value from the Environment as a int value.

        Supports: binary numbers (e.g. 0b110), octal numbers (e.g. 0o234), hex
        numbers (e.g. 0xf234), and decimal numbers (e.g. 480).
        """
        return self._typed_read(name, Integer, default, validator, optional)

    @overload
    def bool(
        self,
        name: String,
        default: Boolean | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Boolean], Boolean] | None = None,
    ) -> Boolean: ...

    @overload
    def bool(
        self,
        name: String,
        default: Boolean | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Boolean], Boolean] | None = None,
        optional: bool = False,
    ) -> Boolean | None: ...

    def bool(
        self,
        name: String,
        default: Boolean | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Boolean], Boolean] | None = None,
        optional: bool = False,
    ) -> Boolean | Boolean | None:
        """Read a value from the Environment as a bool value.

        Considers: "1", "true", "yes", "t", "y", or "on" as `True`
        irrespective of case. Everything else is `False`.
        """
        return self._typed_read(name, Boolean, default, validator, optional)

    @overload
    def float(
        self,
        name: String,
        default: Float | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Float], Boolean] | None = None,
    ) -> Float: ...

    @overload
    def float(
        self,
        name: String,
        default: Float | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Float], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Float: ...

    def float(
        self,
        name: String,
        default: Float | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Float], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Float | Float | None:
        """Read a value from the Environment as a float value."""
        return self._typed_read(name, Float, default, validator, optional)

    @overload
    def bytes(
        self,
        name: String,
        default: Bytes | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Bytes], Boolean] | None = None,
    ) -> Bytes: ...

    @overload
    def bytes(
        self,
        name: String,
        default: Bytes | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Bytes], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Bytes | None: ...

    def bytes(
        self,
        name: String,
        default: Bytes | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Bytes], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Bytes | Bytes | None:
        """Read a value from the Environment as a bytes value.

        Supports hex ("0x61a0"), base64 (e.g. "YQo="), and plain utf-8 strings.
        """
        return self._typed_read(name, Bytes, default, validator, optional)

    @overload
    def path(
        self,
        name: String,
        default: Path | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Path], Boolean] | None = None,
    ) -> Path: ...

    @overload
    def path(
        self,
        name: String,
        default: Path | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Path], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Path | None: ...

    def path(
        self,
        name: String,
        default: Path | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Path], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Path | Path | None:
        """Read a value from the Environment as a path value.

        Supports hex ("0x61a0"), base64 (e.g. "YQo="), and plain utf-8 strings.
        """
        return self._typed_read(name, Path, default, validator, optional)

    @overload
    def url(
        self,
        name: String,
        default: URL | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[URL], Boolean] | None = None,
    ) -> Url: ...

    @overload
    def url(
        self,
        name: String,
        default: URL | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[URL], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Url | None: ...

    def url(
        self,
        name: String,
        default: URL | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[URL], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Url | Url | None:
        """Read a value from the Environment as a URL value."""
        return self._typed_read(name, URL, default, validator, optional)

    @overload
    def json(
        self,
        name: String,
        default: Any | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Json], Boolean] | None = None,
    ) -> Json: ...

    @overload
    def json(
        self,
        name: String,
        default: Any | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Json], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Json | None: ...

    def json(
        self,
        name: String,
        default: Any | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Json], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Json | Json | None:
        """Read a value from environment and parse as a json value."""
        if not isinstance(default, str) and default is not _MissingEnvironmentValue:
            default = json.dumps(default)

        value = self._typed_read(name, String, default, validator, optional)
        if value is None:
            return None
        value_record = self._cast_cache[name]
        value_record.cast_value = json.loads(value)
        value_record.type = JsonValueType  # type: ignore[assignment]
        return value_record.cast_value


class env:  # noqa: N801 - This is a convenience interface
    """Static interface to the Environment class."""

    @staticmethod
    def set(name: String, value: EnvironmentValueType) -> None:
        """Passthrough to Environment instance."""
        Environment().set(name, value)

    @overload
    @staticmethod
    def str(
        name: String,
        default: String | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[String], Boolean] | None = None,
    ) -> String: ...

    @overload
    @staticmethod
    def str(
        name: String,
        default: String | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[String], Boolean] | None = None,
        optional: Boolean = False,
    ) -> String | None: ...

    @staticmethod
    def str(
        name: String,
        default: String | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[String], Boolean] | None = None,
        optional: Boolean = False,
    ) -> String | String | None:
        """Passthrough to an Environment instance."""
        return Environment().str(name, default, validator, optional)

    @overload
    @staticmethod
    def int(
        name: String,
        default: Integer | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Integer], Boolean] | None = None,
    ) -> Integer: ...

    @overload
    @staticmethod
    def int(
        name: String,
        default: Integer | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Integer], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Integer | None: ...

    @staticmethod
    def int(
        name: String,
        default: Integer | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Integer], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Integer | Integer | None:
        """Passthrough to an Environment instance."""
        return Environment().int(name, default, validator, optional)

    @overload
    @staticmethod
    def bool(
        name: String,
        default: Boolean | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Boolean], Boolean] | None = None,
    ) -> Boolean: ...

    @overload
    @staticmethod
    def bool(
        name: String,
        default: Boolean | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Boolean], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Boolean | None: ...

    @staticmethod
    def bool(
        name: String,
        default: Boolean | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Boolean], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Boolean | Boolean | None:
        """Passthrough to an Environment instance."""
        return Environment().bool(name, default, validator, optional)

    @overload
    @staticmethod
    def float(
        name: String,
        default: Float | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Float], Boolean] | None = None,
    ) -> Float: ...

    @overload
    @staticmethod
    def float(
        name: String,
        default: Float | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Float], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Float | None: ...

    @staticmethod
    def float(
        name: String,
        default: Float | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Float], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Float | Float | None:
        """Passthrough to an Environment instance."""
        return Environment().float(name, default, validator, optional)

    @overload
    @staticmethod
    def bytes(
        name: String,
        default: Bytes | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Bytes], Boolean] | None = None,
    ) -> Bytes: ...

    @overload
    @staticmethod
    def bytes(
        name: String,
        default: Bytes | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Bytes], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Bytes | None: ...

    @staticmethod
    def bytes(
        name: String,
        default: Bytes | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Bytes], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Bytes | Bytes | None:
        """Passthrough to an Environment instance."""
        return Environment().bytes(name, default, validator, optional)

    @overload
    @staticmethod
    def path(
        name: String,
        default: Path | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Path], Boolean] | None = None,
    ) -> Path: ...

    @overload
    @staticmethod
    def path(
        name: String,
        default: Path | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Path], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Path | None: ...

    @staticmethod
    def path(
        name: String,
        default: Path | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[Path], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Path | Path | None:
        """Passthrough to an Environment instance."""
        return Environment().path(name, default, validator, optional)

    @overload
    @staticmethod
    def url(
        name: String,
        default: URL | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[URL], Boolean] | None = None,
    ) -> Url: ...

    @overload
    @staticmethod
    def url(
        name: String,
        default: URL | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[URL], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Url | None: ...

    @staticmethod
    def url(
        name: String,
        default: URL | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[URL], Boolean] | None = None,
        optional: Boolean = False,
    ) -> Url | Url | None:
        """Read a value from the Environment as a URL value."""
        return Environment().url(name, default, validator, optional)

    @overload
    @staticmethod
    def json(
        name: String,
        default: Any | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[JsonValueType], Boolean] | None = None,
    ) -> JsonValueType: ...

    @overload
    @staticmethod
    def json(
        name: String,
        default: Any | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[JsonValueType], Boolean] | None = None,
        optional: Boolean = False,
    ) -> JsonValueType | None: ...

    @staticmethod
    def json(
        name: String,
        default: Any | type[_MissingEnvironmentValue] = _MissingEnvironmentValue,
        validator: Callable[[JsonValueType], Boolean] | None = None,
        optional: Boolean = False,
    ) -> JsonValueType | JsonValueType | None:
        """Passthrough to an Environment instance."""
        return Environment().json(name, default, validator, optional)
