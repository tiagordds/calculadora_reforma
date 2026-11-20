from django import forms
from django.core.exceptions import ValidationError


class PenForm(forms.Form):
    confirm_cbs = forms.ChoiceField(
        choices=[("yes", "Confirmo o uso de CBS hipotética de 10% neste exemplo.")],
        error_messages={"required": "Confirme a hipótese de CBS para calcular.",
                        "invalid_choice": "A confirmação da hipótese é inválida."},
    )

    def clean(self):
        cleaned = super().clean()
        allowed = {"csrfmiddlewaretoken", "confirm_cbs"}
        if set(self.data) - allowed or any(len(values) != 1 for _, values in self.data.lists()):
            raise ValidationError("Envie somente a confirmação do exemplo apresentado.")
        return cleaned
