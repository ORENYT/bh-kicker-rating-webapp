from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django import forms

from kicker.models import Player


class RegistrationForm(UserCreationForm):
    success_url = reverse_lazy("profile")

    class Meta(UserCreationForm.Meta):
        model = Player
        fields = (
            "first_name",
            "last_name",
            "location",
            "username",
            "email",
            "password1",
            "password2",
        )


class PlayerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by Name"}),
    )
