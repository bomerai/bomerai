"""JSON Codec with Datetime and UUID support."""

from __future__ import annotations

import contextlib
import dataclasses
import importlib
import inspect
import re
from datetime import UTC, datetime
from json import JSONDecodeError, JSONDecoder, JSONEncoder
from typing import Any
from uuid import UUID

from core.types import JsonScalarValueType, JsonValueType

JsonScalarValueExtendedType = JsonScalarValueType | UUID | datetime
JsonVectorValueExtendedType = list["JsonValueExtendedType"]
JsonMapValueExtendedType = dict[str, "JsonValueExtendedType"]
JsonValueExtendedType = JsonScalarValueExtendedType | JsonVectorValueExtendedType | JsonMapValueExtendedType


__all__ = (
    "JsonExtendedCodec",
    "JsonMapValueExtendedType",
    "JsonScalarValueExtendedType",
    "JsonValueExtendedType",
    "JsonVectorValueExtendedType",
)


class JsonExtendedCodec(JSONDecoder, JSONEncoder):
    """JSON Codec with Datetime and UUID support."""

    DECODER_KWARGS_KEYS = (
        "object_hook",
        "parse_float",
        "parse_int",
        "parse_constant",
        "strict",
        "object_pairs_hook",
    )

    ENCODER_KWARGS_KEYS = (
        "skipkeys",
        "ensure_ascii",
        "check_circular",
        "allow_nan",
        "sort_keys",
        "indent",
        "separators",
        "default",
    )

    # UUID Format
    RFC4122_RE = re.compile(r"^[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}$", re.IGNORECASE | re.UNICODE)

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the instance as both a JSONDecoder and JSONEncoder."""
        JSONDecoder.__init__(
            self,
            **{name: value for name, value in kwargs.items() if name in JsonExtendedCodec.DECODER_KWARGS_KEYS},
        )

        JSONEncoder.__init__(
            self,
            **{name: value for name, value in kwargs.items() if name in JsonExtendedCodec.ENCODER_KWARGS_KEYS},
        )

    def default(self, obj: Any) -> Any:
        """Extend encoding support to handle UUID and datetime."""
        if isinstance(obj, datetime):
            return obj.astimezone(UTC).isoformat()

        if isinstance(obj, UUID):
            return str(obj)

        if dataclasses.is_dataclass(obj):
            type_header = {
                "__type__": {
                    "module": obj.__class__.__module__,
                    "class": obj.__class__.__name__,
                },
            }
            return type_header | dataclasses.asdict(obj)  # type: ignore[call-overload]

        return JSONEncoder.default(self, obj)

    def _decode_extend(self, value: JsonValueType) -> JsonValueExtendedType:
        if isinstance(value, dict) and "__type__" in value:
            type_data = value["__type__"]

            if not isinstance(type_data, dict):
                raise TypeError

            module_path = type_data["module"]
            if not isinstance(module_path, str):
                raise TypeError

            class_name = type_data["class"]
            if not isinstance(class_name, str):
                raise TypeError

            module = importlib.import_module(name=module_path)
            module_classes = inspect.getmembers(module, inspect.isclass)
            klass = next(module_class for name, module_class in module_classes if name == class_name)
            del value["__type__"]
            decode_value = self._decode_extend(value)
            return klass(**decode_value)

        if isinstance(value, dict):
            return {name: self._decode_extend(value) for name, value in value.items()}

        if isinstance(value, list):
            return [self._decode_extend(value) for value in value]

        if isinstance(value, str):
            if JsonExtendedCodec.RFC4122_RE.match(value):
                return UUID(value)

            with contextlib.suppress(ValueError):
                return datetime.fromisoformat(value)

        return value

    def decode(self, string: str, *args: Any, **kwargs: Any) -> JsonValueExtendedType:  # type: ignore[override]
        """Extend decoding to support transforming strings into other types."""
        value = JSONDecoder.decode(self, string, *args, **kwargs)
        try:
            return self._decode_extend(value)
        except (TypeError, KeyError, StopIteration) as exc:
            msg = f"{self.__class__.__name__!r} decoding extension failed"
            raise JSONDecodeError(msg=msg, doc=string, pos=0) from exc
