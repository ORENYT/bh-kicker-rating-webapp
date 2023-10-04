from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django import forms

from kicker.models import Player, Game, Match


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
    player_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
    )


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ["player_one_score", "player_two_score"]

    def clean(self):
        cleaned_data = super().clean()
        score1 = cleaned_data.get("player_one_score")
        score2 = cleaned_data.get("player_two_score")

        if score1 < 0:
            raise forms.ValidationError("Score can't be negative")

        if score2 < 0:
            raise forms.ValidationError("Score can't be negative")

        return cleaned_data


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ["location", "player1", "player2"]

    def clean(self):
        cleaned_data = super().clean()
        player1 = cleaned_data.get("player1")
        player2 = cleaned_data.get("player2")

        if player1 == player2:
            raise forms.ValidationError("Player 1 and 2 must be different")

        return cleaned_data
