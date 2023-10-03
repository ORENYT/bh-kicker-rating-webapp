from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class Player(AbstractUser):
    rating = models.IntegerField(default=1000)
    is_pro = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey("Location", null=True,
                                 on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "player"
        verbose_name_plural = "players"


class Game(models.Model):
    player_one_score = models.IntegerField()
    player_two_score = models.IntegerField()


class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    working_hours = models.TextField()
    admins = models.ManyToManyField(Player, related_name="administers")

    def __str__(self) -> str:
        return self.name


class Match(models.Model):
    games = models.ManyToManyField(Game)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    player1 = models.ForeignKey(Player, on_delete=models.SET_NULL,
                                null=True, related_name="first_player_games")
    player2 = models.ForeignKey(Player, on_delete=models.SET_NULL,
                                null=True, related_name="second_player_games")
    winner = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["date"]
