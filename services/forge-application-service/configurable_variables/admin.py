"""Django admin customizations for ConfigurableVariable model."""

from typing import Any, ClassVar

from cryptography.fernet import InvalidToken
from django import forms
from django.contrib import admin, messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import URLPattern, path

from configurable_variables.models import ConfigurableVariable


class EncryptedValueInput(forms.TextInput):
    """Custom widget for encrypted values."""

    template_name = "encrypted_value_input.html"

    def format_value(self, value: str | dict) -> dict[str, str | None]:  # type: ignore[override]
        """Format the value to a dict, as our template expects."""
        if isinstance(value, dict):
            return value
        return {"value": super().format_value(value)}


class RotateKeyForm(forms.Form):
    """Form for rotating encryption keys."""

    old_key = forms.CharField()
    new_key = forms.CharField()

    def save(self) -> None:
        """Rotate the encryption key for all ConfigurableVariable instances."""
        old_key = bytes(self.cleaned_data["old_key"], "utf-8")
        new_key = bytes(self.cleaned_data["new_key"], "utf-8")
        for variable in ConfigurableVariable.objects.all():
            variable.rotate(old_key, new_key)


@admin.register(ConfigurableVariable)
class ConfigurableVariableAdmin(admin.ModelAdmin):
    """Custom admin interface for ConfigurableVariable model."""

    list_display = ("var_name", "can_decrypt", "encrypted_key_hash")

    @admin.display(description="Variable Name")
    def var_name(self, obj: ConfigurableVariable) -> str:
        """Change the column name to `Variable Name` with the `@display()` decorator."""
        return obj.name

    @admin.display(description="Can Decrypt", boolean=True)
    def can_decrypt(self, obj: ConfigurableVariable) -> bool:
        """Check if the current encryption key can decrypt the value. Use the `@display()` decorator so that we can specify `boolean=True`."""
        return obj.can_decrypt()

    @admin.display(description="Encrypted Key Hash")
    def encrypted_key_hash(self, obj: ConfigurableVariable) -> str:
        """Change the column name to `Encrypted Key Hash` with the `@display()` decorator."""
        return obj.enc_key_hash

    def get_urls(self) -> list[URLPattern]:
        """Add a custom URL for rotating encryption keys."""
        urls = super().get_urls()
        my_urls = [path("rotate/", self.admin_site.admin_view(self.rotate_key_view))]

        return my_urls + urls

    def rotate_key_view(self, request: HttpRequest) -> HttpResponse:
        """Handle the rotation of encryption keys."""
        form = RotateKeyForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Encryption key rotated successfully")
                    return HttpResponseRedirect("../")
                except InvalidToken:
                    messages.error(request, "Old key is invalid")
            else:
                messages.error(request, "Invalid form")
        context = {
            "title": "Rotate Encryption Key",
            "form": form,
            "add": True,
            "change": False,
            "has_delete_permission": False,
            "has_change_permission": True,
            "has_absolute_url": False,
            "opts": self.opts,
            "save_as": False,
            "show_save": True,
            **self.admin_site.each_context(request),
        }

        return TemplateResponse(request, "rotate_key.html", context)

    def get_form(
        self,
        request: HttpRequest,  # noqa: ARG002
        obj: ConfigurableVariable | None = None,
        change: bool = False,  # noqa: ARG002, FBT001, FBT002
        **kwargs: dict[str, Any],  # noqa: ARG002
    ) -> type[forms.ModelForm]:
        """Define a custom form in a closure to access the `obj` parameter."""

        def get_initial_value() -> dict[str, str]:
            try:
                return {"value": obj.value} if obj else {}
            except InvalidToken:
                return {"error": "Decryption failed"}

        class ConfigurableVariableForm(forms.ModelForm):
            """Custom form for ConfigurableVariable model."""

            class Meta:
                """Django model form configuration."""

                model = ConfigurableVariable
                fields = ("name",)
                labels: ClassVar = {
                    "name": "Variable Name",
                }

            value = forms.CharField(required=True, widget=EncryptedValueInput, initial=get_initial_value)

            def save(self, commit: bool = True) -> ConfigurableVariable:  # noqa: FBT001, FBT002
                self.instance.value = self.cleaned_data["value"]
                return super().save(commit)

        return ConfigurableVariableForm
