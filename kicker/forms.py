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
        fields = ['player_one_score', 'player_two_score']


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['location', 'player1', 'player2']
