import math

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from kicker.views import TableListView

TABLE_LIST_URL = reverse("kicker:table")


class TestSearch(TestCase):
    def setUp(self) -> None:
        players = []
        for i in range(6):
            player = get_user_model().objects.create_user(
                username=f"player{i}",
                first_name=f"Name{i}",
                last_name=f"Last{i}",
                password=f"1q2Aafdojpass{i}",
                rating=f"100{i}"
            )
            players.append(player)
        self.players = players
        self.client.force_login(players[0])

    def test_view_uses_correct_template(self):
        response = self.client.get(TABLE_LIST_URL)
        self.assertTemplateUsed(response, "table.html")

    def test_empty_search_return_all_data(self):
        form_data = {"player_name": ""}
        per_page = TableListView.paginate_by
        total_pages = math.ceil(len(self.players) / per_page)

        url = TABLE_LIST_URL
        response = self.client.get(url, data=form_data)

        context = response.context_data
        queryset = context["object_list"]

        self.assertEqual(queryset.count(), per_page)
        self.assertTrue(context["is_paginated"])
        self.assertEqual(
            str(context["page_obj"]), f"<Page 1 of {total_pages}>"
        )

    def test_search_should_return_all_matches_despite_register(self):
        form_data = {"player_name": "E"}
        per_page = TableListView.paginate_by
        total_pages = math.ceil(len(self.players) / per_page)

        url = TABLE_LIST_URL
        response = self.client.get(url, data=form_data)

        context = response.context_data
        queryset = context["object_list"]

        self.assertEqual(queryset.count(), per_page)
        self.assertTrue(context["is_paginated"])
        self.assertEqual(
            str(context["page_obj"]), f"<Page 1 of {total_pages}>"
        )

    def test_search_should_return_nothing_if_no_matches(self):
        form_data = {"player_name": f"player{len(self.players)}"}

        url = TABLE_LIST_URL
        response = self.client.get(url, data=form_data)

        context = response.context_data
        queryset = context["object_list"]

        self.assertEqual(queryset.count(), 0)

    def test_should_return_correst_user_on_unique_playername_input(self):
        form_data = {"player_name": "Name1"}

        url = TABLE_LIST_URL
        response = self.client.get(url, data=form_data)

        context = response.context_data
        queryset = context["object_list"]

        self.assertEqual(queryset.count(), 1)
