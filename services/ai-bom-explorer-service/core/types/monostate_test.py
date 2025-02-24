from .monostate import Monostate


class Mock(Monostate):
    pass


class TestMonostate:
    def test_shared_state(self) -> None:
        mock = Mock()
        mock.test_value = "Test string value"  # type: ignore[attr-defined]

        assert mock is not Mock()
        assert mock.test_value is Mock().test_value  # type: ignore[attr-defined]

    def test_persistant_state(self) -> None:
        Mock().test_value = "Test string value"  # type: ignore[attr-defined]
