"""kicker_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from kicker.views import (
    index,
    logout_view,
    TableListView,
    PlayerDetailView,
    LocationDetailView,
    RegisterView,
    PlayerLoginView,
    PlayerUpdateView,
    choose_total_games,
    create_match
)

urlpatterns = [
    path("", index, name="index"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/<int:pk>/", PlayerDetailView.as_view(), name="profile"),
    path("location/<int:pk>/", LocationDetailView.as_view(), name="location"),
    path("table/", TableListView.as_view(), name="table"),
    path("logout/", logout_view, name="logout"),
    path("login/", PlayerLoginView.as_view(), name="login"),
    path("profile/<int:pk>/update/", PlayerUpdateView.as_view(), name="update"),
    path("games/", choose_total_games, name="games"),
    path("match/<int:num_games>/", create_match, name='match_create'),
]

app_name = "kicker"
