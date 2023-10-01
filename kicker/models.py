from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class Player(AbstractUser):
    rating = models.IntegerField()
    is_pro = models.BooleanField(default=False)

    class Meta:
        verbose_name = "player"
        verbose_name_plural = "players"


class Game(models.Model):
    player1 = models.ForeignKey(Player, on_delete=models.SET_NULL,
                                null=True,  related_name="first_player_games")
    player2 = models.ForeignKey(Player, on_delete=models.SET_NULL,
                                null=True,  related_name="second_player_games")
    player_one_score = models.IntegerField()
    player2_score = models.IntegerField()


class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    working_hours = models.TextField()


class Match(models.Model):
    games = models.ManyToManyField(Game)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]
