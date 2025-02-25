import pytest

from core.error import EnvironmentValidationFailure, MandatoryEnvironmentVariableMissing


class TestErorr:
    def test_error_structure(self) -> None:
        assert issubclass(MandatoryEnvironmentVariableMissing, EnvironmentError)
        assert issubclass(EnvironmentValidationFailure, EnvironmentError)

    def test_formatted_erros(self) -> None:
        value = "value"
        with pytest.raises(
            EnvironmentValidationFailure,
            match="Invalid environment variable value 'value'",
        ):
            raise EnvironmentValidationFailure(value)

        key = "VAR"
        with pytest.raises(
            MandatoryEnvironmentVariableMissing,
            match="Mandatory environment variable 'VAR' is missing",
        ):
            raise MandatoryEnvironmentVariableMissing(key)
