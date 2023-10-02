from django.contrib import admin

# Register your models here.
from kicker.models import Location, Player, Match

admin.site.register(Location)
admin.site.register(Player)
admin.site.register(Match)
