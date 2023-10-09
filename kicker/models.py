from django.contrib.auth.models import AbstractUser
from django.db import models


class Player(AbstractUser):
    rating = models.IntegerField(default=1000)
    is_pro = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(
        "Location",
        null=True,
        on_delete=models.SET_NULL,
        related_name="players",
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Game(models.Model):
    player_one_score = models.IntegerField()
    player_two_score = models.IntegerField()
    match = models.ForeignKey(
        "Match", related_name="games", on_delete=models.CASCADE
    )


class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    working_hours = models.TextField()
    admins = models.ManyToManyField(Player, related_name="locations")

    def __str__(self) -> str:
        return self.name


class Match(models.Model):
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, related_name="matches"
    )
    date = models.DateTimeField(auto_now_add=True)
    player1 = models.ForeignKey(
        Player,
        on_delete=models.SET_NULL,
        null=True,
        related_name="first_player_matches",
    )
    player2 = models.ForeignKey(
        Player,
        on_delete=models.SET_NULL,
        null=True,
        related_name="second_player_matches",
    )
    winner = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True, related_name="matches"
    )

    class Meta:
        ordering = ["date"]
