from django.contrib import admin

# Register your models here.
from kicker.models import Location, Player

admin.site.register(Location)
admin.site.register(Player)