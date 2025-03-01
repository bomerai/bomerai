from unittest.mock import patch

from celery.signals import setup_logging


def test_receiver_setup_logging() -> None:
    with patch("celery_worker.celery.configure_logging") as mock_configure_logging:

        # Trigger the signal manually
        setup_logging.send(sender=None)

        # Assert configure_logging was called
        mock_configure_logging.assert_called_once()
