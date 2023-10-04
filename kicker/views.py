from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from kicker.forms import (
    RegistrationForm,
    PlayerSearchForm,
    GameForm,
    MatchForm,
)
from kicker.models import Player, Location


def index(request):
    context = {}
    return render(request, "index.html", context=context)


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
            reverse_lazy("kicker:profile", args=[self.object.id])
        )

    def form_invalid(self, form):
        return super().form_invalid(form)


class PlayerLoginView(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy("kicker:table")


class PlayerDetailView(generic.DetailView):
    model = Player
    template_name = "profile.html"
    context_object_name = "player"


class LocationDetailView(generic.DetailView):
    model = Location
    template_name = "location.html"
    context_object_name = "location"


class TableListView(generic.ListView):
    model = Player
    paginate_by = 5
    template_name = "table.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TableListView, self).get_context_data(**kwargs)
        first_name = self.request.GET.get("first_name")
        last_name = self.request.GET.get("last_name")
        context["search_form"] = PlayerSearchForm(
            initial={
                "first_name": first_name,
                "last_name": last_name,
            }
        )
        return context

    def get_queryset(self):
        queryset = Player.objects.all()
        form = PlayerSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data["player_name"]
            return queryset.filter(
                Q(first_name__icontains=name) | Q(last_name__icontains=name)
            ).order_by("-rating")
        return queryset


class PlayerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Player
    fields = ("first_name", "last_name", "location")
    template_name = "update.html"
    success_url = reverse_lazy("kicker:table")

    def form_valid(self, form):
        if self.object.id == self.request.user.id:
            form.save()
            return HttpResponseRedirect(
                reverse_lazy("kicker:profile", args=[self.object.id])
            )
        else:
            return self.render_to_response(
                self.get_context_data(form=form, show_modal=True)
            )


def choose_total_games(request):
    if request.method == "POST":
        num_games = request.POST.get("num_games")
        if num_games in ("1", "3", "5"):
            return redirect(f"/match/{num_games}/")

    return render(request, "games.html")


def determine_winner(game_forms, match_form) -> Player:
    player_one_wins = 0
    player_two_wins = 0
    match_data = match_form.cleaned_data
    for game in game_forms:
        cleaned_data = game.cleaned_data
        player_one_score = cleaned_data.get("player_one_score")
        player_two_score = cleaned_data.get("player_two_score")
        if player_one_score > player_two_score:
            player_one_wins += 1
        else:
            player_two_wins += 1
    if player_two_wins > player_one_wins:
        winner = match_data["player2"]
        looser = match_data["player1"]
    else:
        winner = match_data["player1"]
        looser = match_data["player2"]
    looser.rating -= 5
    looser.save()
    winner.rating += 5
    winner.save()
    return winner


def create_match(request, num_games):
    num_games = int(num_games)

    if not request.user.is_superuser:
        return redirect("kicker:table")

    if request.method == "POST":
        match_form = MatchForm(request.POST)
        game_forms = [
            GameForm(request.POST, prefix=f"game_form_{i}")
            for i in range(num_games)
        ]

        if match_form.is_valid() and all(
                [form.is_valid() for form in game_forms]
        ):
            with transaction.atomic():
                match = match_form.save()
                for game_form in game_forms:
                    game = game_form.save(commit=False)
                    game.match = match
                    game.save()
                    match.games.add(game)
                    match.winner = determine_winner(game_forms, match_form)
                match.save()
            return redirect("kicker:table")
    else:
        match_form = MatchForm()
        game_forms = [
            GameForm(prefix=f"game_form_{i}") for i in range(num_games)
        ]

    return render(
        request,
        "match.html",
        {
            "match_form": match_form,
            "game_forms": game_forms,
            "num_games": num_games,
        },
    )
