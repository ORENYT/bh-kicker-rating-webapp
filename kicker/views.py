from django.shortcuts import render
from django.views import generic

from kicker.forms import RegistrationForm
from kicker.models import Player, Location


def index(request):
    context = {}
    return render(request, "base.html", context=context)


class RegistrationView(generic.CreateView):
    model = Player
    form_class = RegistrationForm
    template_name = "register.html"


class PlayerDetailView(generic.DetailView):
    model = Player
    template_name = "profile.html"
    context_object_name = "player"
    # queryset = Player.objects.all().prefetch_related("player__games")


class LocationDetailView(generic.DetailView):
    model = Location
    template_name = "location.html"
    context_object_name = "location"
