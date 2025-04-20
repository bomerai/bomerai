"""
This module provides a utility class for wrapping dictionaries and allowing attribute-style access.
"""

from typing import Any, Dict, Optional, TypeVar, Generic, Type, cast


T = TypeVar("T")


class DictWrapper(Generic[T]):
    """
    A utility class that wraps dictionaries and allows attribute-style access.

    Example:
        >>> data = {"foo": "bar", "nested": {"baz": 123}}
        >>> wrapper = DictWrapper(data)
        >>> wrapper.foo
        'bar'
        >>> wrapper.nested.baz
        123
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize the wrapper with a dictionary.

        Args:
            data: The dictionary to wrap
        """
        self._data = data

    def __getattr__(self, name: str) -> Any:
        """
        Allow attribute-style access to dictionary keys.

        Args:
            name: The attribute name (key in the dictionary)

        Returns:
            The value associated with the key

        Raises:
            AttributeError: If the key doesn't exist in the dictionary
        """
        if name in self._data:
            value = self._data[name]
            if isinstance(value, dict):
                return DictWrapper(value)
            return value

        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def __getitem__(self, key: str) -> Any:
        """
        Allow dictionary-style access to keys.

        Args:
            key: The key in the dictionary

        Returns:
            The value associated with the key

        Raises:
            KeyError: If the key doesn't exist in the dictionary
        """
        if key in self._data:
            value = self._data[key]
            if isinstance(value, dict):
                return DictWrapper(value)
            return value

        raise KeyError(key)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the dictionary with a default if the key doesn't exist.

        Args:
            key: The key in the dictionary
            default: The default value to return if the key doesn't exist

        Returns:
            The value associated with the key or the default value
        """
        if key in self._data:
            value = self._data[key]
            if isinstance(value, dict):
                return DictWrapper(value)
            return value

        return default

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the wrapper back to a dictionary.

        Returns:
            The underlying dictionary
        """
        return self._data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DictWrapper":
        """
        Create a wrapper from a dictionary.

        Args:
            data: The dictionary to wrap

        Returns:
            A new DictWrapper instance
        """
        return cls(data)

    def __repr__(self) -> str:
        """
        Return a string representation of the wrapper.

        Returns:
            A string representation of the wrapper
        """
        return f"{self.__class__.__name__}({self._data})"


class TypedDictWrapper(DictWrapper[T]):
    """
    A wrapper for dictionaries that provides type hints for attribute access.

    Example:
        class UserData(TypedDictWrapper[UserData]):
            name: str
            age: int
            address: Dict[str, str]

        data = {"name": "John", "age": 30, "address": {"street": "123 Main St"}}
        user = UserData(data)
        user.name  # Type hint: str
        user.age  # Type hint: int
        user.address.street  # Type hint: str
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize the wrapper with a dictionary.

        Args:
            data: The dictionary to wrap
        """
        super().__init__(data)

    def __getattr__(self, name: str) -> Any:
        """
        Allow attribute-style access to dictionary keys with type hints.

        Args:
            name: The attribute name (key in the dictionary)

        Returns:
            The value associated with the key

        Raises:
            AttributeError: If the key doesn't exist in the dictionary
        """
        value = super().__getattr__(name)
        if isinstance(value, dict):
            # Create a new instance of the same class for nested dictionaries
            return self.__class__(value)
        return value
