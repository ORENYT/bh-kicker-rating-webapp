from urllib import request

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from kicker.forms import RegistrationForm
from kicker.models import Player, Location


def index(request):
    context = {}
    return render(request, "blank.html", context=context)


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy("kicker:table"))


class RegisterView(generic.CreateView):
    model = Player
    form_class = RegistrationForm
    template_name = "register.html"
    success_url = reverse_lazy("kicker:table")

    def form_valid(self, form):
        location_id = self.request.POST.get("location")
        if location_id:
            location = Location.objects.get(pk=location_id)
            form.instance.location = location
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "You have signed up successfully.")
        return HttpResponseRedirect(
            reverse_lazy("kicker:profile", args=[self.object.id]))

    def form_invalid(self, form):
        return super().form_invalid(form)


class PlayerLoginView(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy("kicker:table")


class PlayerDetailView(generic.DetailView):
    model = Player
    template_name = "profile.html"
    context_object_name = "player"
    # queryset = Player.objects.all().prefetch_related("player__games")


class LocationDetailView(generic.DetailView):
    model = Location
    template_name = "location.html"
    context_object_name = "location"


class TableListView(generic.ListView):
    model = Player
    paginate_by = 4
    template_name = "table.html"
    ordering = ["-rating"]
