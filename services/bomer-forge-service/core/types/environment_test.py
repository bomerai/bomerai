from base64 import b16encode, b64encode
from collections.abc import Generator
from pathlib import Path
from random import choice, randbytes, randint

import pytest
from urlpath import URL

from core.error import EnvironmentValidationFailure, MandatoryEnvironmentVariableMissing
from core.types.environment import Environment, env


class TestEnvironment:
    @pytest.fixture(autouse=True)
    def flush_env(self) -> Generator[None, None, None]:
        """Run each test in a clean environment, and restore the original environment after each test."""
        cached_source_env = Environment()._source_env
        Environment()._source_env = {}
        yield
        Environment()._source_env = cached_source_env

    def test__typed_read(self) -> None:
        Environment(source_environment={"MOCK_KEY": "mock-value"})

        assert Environment()._typed_read(name="MOCK_KEY", cast_type=str, optional=True) == "mock-value"

        with pytest.raises(MandatoryEnvironmentVariableMissing, match="MISSING_KEY"):
            Environment()._typed_read(name="MISSING_KEY", cast_type=str, optional=False)

        assert Environment()._typed_read(name="MISSING_KEY", cast_type=str, optional=True) is None

    def test_missing(self) -> None:
        with pytest.raises(MandatoryEnvironmentVariableMissing):
            Environment(source_environment={}).str("MISSING_KEY")

    def test_cast_str(self) -> None:
        assert Environment(source_environment={"MOCK_KEY": "hello-world"}).str("MOCK_KEY") == "hello-world"
        assert Environment().str("MISSING_KEY", optional=True) is None

    def test_cast_int(self) -> None:
        number = randint(-100000, 100000)
        Environment(
            source_environment={
                "INT_KEY": str(number),
                "BINARY_KEY": bin(number),
                "OCTAL_KEY": oct(number),
                "HEX_KEY": hex(number),
                "BAD_NUMBER_KEY": "not-a-number",
            },
        )

        assert Environment().int("INT_KEY") == number
        assert Environment().int("BINARY_KEY") == number
        assert Environment().int("OCTAL_KEY") == number
        assert Environment().int("HEX_KEY") == number
        assert Environment().int("MISSING_VALUE_DEFAULT", number) == number

        with pytest.raises(
            ValueError,
            match=r"invalid literal for int\(\) with base 10: 'not-a-number'",
        ):
            Environment().int("BAD_NUMBER_KEY")

        assert Environment().int("MISSING_KEY", optional=True) is None

    def test_cast_bool(self) -> None:
        Environment(
            source_environment={
                "TRUE_VALUE": str(choice(("1", "true", "yes", "t", "y", "on"))),
                "FALSE_VALUE": str(choice(("2", "trrue", "ye", "f", "n", "off"))),
            },
        )

        assert Environment().bool("TRUE_VALUE") is True
        assert Environment().bool("MISSING_TRUE_VALUE", True) is True

        assert Environment().bool("FALSE_VALUE") is False
        assert Environment().bool("MISSING_FALSE_VALUE", False) is False

        assert Environment().bool("MISSING_KEY", optional=True) is None

    def test_cast_float(self) -> None:
        number = float(randint(-100000, 100000)) / randint(-100000, 100000) * 1000

        Environment(source_environment={"FLOAT_KEY": number})

        assert Environment().float("FLOAT_KEY") == number
        assert Environment().float("MISSING_FLOAT_KEY", number) == number
        assert Environment().float("MISSING_KEY", optional=True) is None

    def test_cast_bytes(self) -> None:
        raw_bytes = randbytes(randint(1, 128))
        Environment(
            source_environment={
                "B16_BYTES": b16encode(raw_bytes).decode(encoding="utf-8"),
                "B64_BYTES": b64encode(raw_bytes).decode(encoding="utf-8"),
                "S_BYTES": bytes.decode(b"Hello world", encoding="utf-8"),
            },
        )

        assert Environment().bytes("B16_BYTES") == raw_bytes
        assert Environment().bytes("B64_BYTES") == raw_bytes
        assert Environment().bytes("S_BYTES") == b"Hello world"
        assert Environment().bytes("BAD_KEY", raw_bytes) == raw_bytes
        assert Environment().bytes("MISSING_KEY", optional=True) is None

    def test_cast_path(self) -> None:
        path = "/path/to/foo"
        Environment(source_environment={"PATH_KEY": path})

        assert str(Environment().path("PATH_KEY")) == path
        assert isinstance(Environment().path("PATH_KEY"), Path)
        assert Environment().path("MISSING_KEY", optional=True) is None

    def test_cast_json(self) -> None:
        Environment(
            source_environment={
                "JSON_STR": '"Hello test value"',
                "JSON_INT": "2578934",
                "JSON_FLOAT": "-531.5",
                "JSON_BOOL": "true",
                "JSON_NONE": "null",
                "JSON_LIST": '["a", "b", 10, {"1": 2}]',
                "JSON_DICT": '{"a": 1, "b": [1, 2, 3]}',
            },
        )

        assert Environment().json("JSON_STR") == "Hello test value"
        assert Environment().json("JSON_INT") == 2578934
        assert Environment().json("JSON_FLOAT") == -531.5
        assert Environment().json("JSON_BOOL") is True
        assert Environment().json("JSON_NONE") is None
        assert Environment().json("JSON_LIST") == ["a", "b", 10, {"1": 2}]
        assert Environment().json("JSON_DICT") == {"a": 1, "b": [1, 2, 3]}
        assert Environment().json("MISSING_KEY", optional=True) is None
        assert Environment().json("ENCODE_DEFAULT", {"foo": "bar"}) == {"foo": "bar"}

    def test_cast_url(self) -> None:
        Environment(
            source_environment={
                "VALID_URL": "https://www.foo.com/bar?field=value#fragment",
            },
        )

        assert Environment().url("VALID_URL") == URL("https://www.foo.com/bar?field=value#fragment")
        assert Environment().url("MISSING_KEY", optional=True) is None

    def test_set(self) -> None:
        from os import environ

        env = Environment(source_environment={})
        env.set("FOO", URL("https://www.google.com"))
        assert env.url("FOO") == URL("https://www.google.com")
        assert environ["FOO"] == "https://www.google.com"

    def test_validators(self) -> None:
        Environment(source_environment={"NOT_NEGATIVE": "-10"})
        with pytest.raises(EnvironmentValidationFailure):
            Environment().int("NOT_NEGATIVE", validator=lambda x: x > 0)

    def test_static_interface(self) -> None:
        int_var = randint(-100000, 100000)
        float_var = float(randint(-100000, 100000)) / randint(-100000, 100000) * 1000
        raw_bytes = randbytes(randint(1, 128))

        Environment(
            source_environment={
                "BOOL_VAR": "False",
                "BYTES_VAR": b16encode(raw_bytes).decode(encoding="utf-8"),
                "FLOAT_VAR": str(float_var),
                "INT_VAR": str(int_var),
                "JSON_VAR": "[1, 2, 3]",
                "PATH_VAR": "/foo/bar/bash",
                "STR_VAR": "mock-str-var-value",
                "URL_VAR": "https://foo.com",
            },
        )

        env.set("SET_VAR", "hello-word")
        assert env.str("SET_VAR", "hello-world")

        assert env.str("STR_VAR") == "mock-str-var-value"
        assert env.int("INT_VAR") == int_var
        assert env.bool("BOOL_VAR") is False
        assert env.float("FLOAT_VAR") == float_var
        assert env.bytes("BYTES_VAR") == raw_bytes
        assert env.path("PATH_VAR") == Path("/foo/bar/bash")
        assert env.json("JSON_VAR") == [1, 2, 3]
        assert env.url("URL_VAR") == URL("https://foo.com")
