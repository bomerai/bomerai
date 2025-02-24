from collections.abc import Generator
from unittest.mock import AsyncMock, Mock, PropertyMock, patch

import pytest
from cryptography.fernet import InvalidToken
from django.contrib.admin.sites import AdminSite

from configurable_variables import crypto
from configurable_variables.admin import ConfigurableVariableAdmin, EncryptedValueInput, RotateKeyForm
from configurable_variables.models import ConfigurableVariable


@pytest.fixture(autouse=True)
def mock_post_save() -> Generator:
    with patch("core.db_constants.constants", AsyncMock()):
        yield


class TestEncryptedValueInput:

    def test_format_value_handles_dict(self) -> None:
        widget = EncryptedValueInput()

        assert widget.format_value({"value": "value"}) == {"value": "value"}

    def test_format_value_handles_non_dict(self) -> None:
        widget = EncryptedValueInput()

        assert widget.format_value("value") == {"value": "value"}


@pytest.mark.django_db()
class TestRotateKeyForm:
    def test_save(self) -> None:
        with patch("configurable_variables.crypto.env") as mock_env:
            mock_env.str.return_value = "old_key"
            enc_value = crypto.encrypt(b"value")

        model = ConfigurableVariable.objects.create(name="name", enc_key_hash="enc_key_hash", encrypted_value=enc_value)

        form = RotateKeyForm(data={"old_key": "old_key", "new_key": "new_key"})
        form.full_clean()
        with patch("configurable_variables.crypto.env") as mock_env:
            mock_env.str.return_value = "new_key"
            form.save()
            model.refresh_from_db()
            assert model.value != enc_value

            assert model.value == "value"


class TestConfigurableVariableAdmin:
    def test_var_name(self) -> None:
        admin = ConfigurableVariableAdmin(ConfigurableVariable, AdminSite())

        assert admin.var_name(ConfigurableVariable(name="name")) == "name"

    def test_can_decrypt(self) -> None:
        admin = ConfigurableVariableAdmin(ConfigurableVariable, AdminSite())

        mock_configurable_variable = Mock()
        admin.can_decrypt(mock_configurable_variable)

        assert mock_configurable_variable.can_decrypt.call_count == 1

    def test_encrypted_key_hash(self) -> None:
        admin = ConfigurableVariableAdmin(ConfigurableVariable, AdminSite())

        assert admin.encrypted_key_hash(ConfigurableVariable(name="name", enc_key_hash="key_hash")) == "key_hash"

    def test_get_urls(self) -> None:
        admin = ConfigurableVariableAdmin(ConfigurableVariable, AdminSite())

        urls = admin.get_urls()

        assert len(urls) >= 1
        # this is hacky, especially the nested quotes, but it's the best I've got
        assert len([url for url in urls if url.pattern.describe() == "'rotate/'"]) == 1

    def test_rotate_key_view_get(self) -> None:
        admin = ConfigurableVariableAdmin(ConfigurableVariable, AdminSite())

        request = Mock()
        request.method = "GET"
        request.POST = {}
        request.META = {
            "SCRIPT_NAME": "",
        }

        with patch("configurable_variables.admin.TemplateResponse") as mock_template_response:
            admin.rotate_key_view(request)

            assert mock_template_response.call_count == 1
            assert mock_template_response.call_args[0][0] == request
            assert mock_template_response.call_args[0][1] == "rotate_key.html"
            assert mock_template_response.call_args[0][2]["title"] == "Rotate Encryption Key"

    def test_rotate_key_view_post_success(self) -> None:
        admin = ConfigurableVariableAdmin(ConfigurableVariable, AdminSite())

        request = Mock()
        request.method = "POST"
        request.POST = {"old_key": "old_key", "new_key": "new_key"}
        request.META = {
            "SCRIPT_NAME": "",
        }

        with (
            patch("configurable_variables.admin.RotateKeyForm") as mock_rotate_key_form,
            patch("configurable_variables.admin.HttpResponseRedirect") as mock_http_response_redirect,
        ):
            mock_rotate_key_form.return_value.is_valid.return_value = True

            admin.rotate_key_view(request)

            assert mock_rotate_key_form.call_count == 1
            assert mock_rotate_key_form.call_args[0][0] == request.POST
            assert mock_rotate_key_form.return_value.is_valid.call_count == 1
            assert mock_rotate_key_form.return_value.save.call_count == 1

            assert mock_http_response_redirect.call_count == 1
            assert mock_http_response_redirect.call_args[0][0] == "../"

    def test_rotate_key_view_post_invalid_form(self) -> None:
        admin = ConfigurableVariableAdmin(ConfigurableVariable, AdminSite())

        request = Mock()
        request.method = "POST"
        request.POST = {"old_key": "old_key", "new_key": "new_key"}
        request.META = {
            "SCRIPT_NAME": "",
        }

        with (
            patch("configurable_variables.admin.RotateKeyForm") as mock_rotate_key_form,
            patch("configurable_variables.admin.TemplateResponse") as mock_template_response,
            patch("configurable_variables.admin.messages") as mock_messages,
        ):
            mock_rotate_key_form.return_value.is_valid.return_value = False

            admin.rotate_key_view(request)

            assert mock_rotate_key_form.call_count == 1
            assert mock_rotate_key_form.call_args[0][0] == request.POST
            assert mock_rotate_key_form.return_value.is_valid.call_count == 1
            assert mock_rotate_key_form.return_value.save.call_count == 0

            assert mock_messages.error.call_count == 1

            assert mock_template_response.call_count == 1

    def test_rotate_key_view_post_invalid_token(self) -> None:
        admin = ConfigurableVariableAdmin(ConfigurableVariable, AdminSite())

        request = Mock()
        request.method = "POST"
        request.POST = {"old_key": "old_key", "new_key": "new_key"}
        request.META = {
            "SCRIPT_NAME": "",
        }

        with (
            patch("configurable_variables.admin.RotateKeyForm") as mock_rotate_key_form,
            patch("configurable_variables.admin.TemplateResponse") as mock_template_response,
            patch("configurable_variables.admin.messages") as mock_messages,
        ):
            mock_rotate_key_form.return_value.is_valid.return_value = True
            mock_rotate_key_form.return_value.save.side_effect = InvalidToken()

            admin.rotate_key_view(request)

            assert mock_messages.error.call_count == 1

            assert mock_template_response.call_count == 1


class TestGetForm:
    def test_get_initial_value_with_object(self) -> None:
        admin = ConfigurableVariableAdmin(ConfigurableVariable, AdminSite())

        mock_configurable_variable = Mock()
        mock_configurable_variable.value = "abc123"

        form = admin.get_form(Mock(), obj=mock_configurable_variable)()

        assert form["value"].initial == {"value": "abc123"}

    def test_get_initial_value_with_none(self) -> None:
        admin = ConfigurableVariableAdmin(ConfigurableVariable, AdminSite())

        form = admin.get_form(Mock(), obj=None)()

        assert form["value"].initial == {}

    def test_get_initial_value_handles_invalid_token(self) -> None:
        admin = ConfigurableVariableAdmin(ConfigurableVariable, AdminSite())

        with patch.object(ConfigurableVariable, "value", new_callable=PropertyMock) as mock_value:
            mock_value.side_effect = InvalidToken()

            form = admin.get_form(Mock(), obj=ConfigurableVariable())()

            assert form["value"].initial == {"error": "Decryption failed"}

    @pytest.mark.django_db()
    def test_save(self) -> None:
        admin = ConfigurableVariableAdmin(ConfigurableVariable, AdminSite())

        data = {
            "name": "name",
            "value": "value",
        }
        with patch.object(ConfigurableVariable, "value", new_callable=PropertyMock) as mock_value:
            form = admin.get_form(Mock(), obj=ConfigurableVariable())(data=data)

            form.full_clean()
            form.save()

            assert mock_value.call_count == 1
            assert mock_value.call_args[0][0] == "value"
