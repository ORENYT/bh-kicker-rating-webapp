from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from kicker.models import Player


class RegistrationForm(UserCreationForm):
    success_url = reverse_lazy("profile")

    class Meta(UserCreationForm.Meta):
        model = Player
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "is_pro",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data["is_pro"]:
            user.rating = 1500
        else:
            user.rating = 1000
        if commit:
            user.save()
        return user
