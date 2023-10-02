from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import generic

from kicker.forms import RegistrationForm
from kicker.models import Player, Location


def index(request):
    context = {}
    return render(request, "table.html", context=context)


def register(request):
    form = RegistrationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("kicker:profile")
    return render(request, "register.html", {'form': form})


class LoginView(generic.CreateView):
    model = Player
    form_class = ""
    template_name = "login.html"


class PlayerDetailView(generic.DetailView):
    model = Player
    template_name = "profile.html"
    context_object_name = "player"
    # queryset = Player.objects.all().prefetch_related("player__games")


class LocationDetailView(generic.DetailView):
    model = Location
    template_name = "location.html"
    context_object_name = "location"
