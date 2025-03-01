"""JSON typing extension.

The python types for JSON are not specific enough for our needs.
"""

from __future__ import annotations

__all__ = (
    "JsonMapValueType",
    "JsonScalarValueType",
    "JsonValueType",
    "JsonVectorValueType",
)

JsonScalarValueType = str | int | float | bool | None

JsonVectorValueType = list["JsonValueType"]

JsonMapValueType = dict[str, "JsonValueType"]

JsonValueType = JsonScalarValueType | JsonVectorValueType | JsonMapValueType
