from django.contrib.auth import get_user_model
from django.test import TestCase

from kicker.forms import MatchForm, RegistrationForm
from kicker.models import Location


class TestFormsValidation(TestCase):

    def setUp(self) -> None:
        self.location = Location.objects.create(
            name="Test Location",
            address="Test Address",
            working_hours="-",
        )
        self.test_player1 = get_user_model().objects.create_user(
            username="testuser1",
            first_name="test first_name",
            last_name="test last_name",
            password="test123user",
        )
        self.test_player2 = get_user_model().objects.create_user(
            username="testuser2",
            first_name="test first_name",
            last_name="test last_name",
            password="test123user",
        )

    def test_form_match_is_valid(self) -> None:
        form = MatchForm(data={
            "player1": self.test_player1,
            "player2": self.test_player2,
            "location": self.location
        })
        self.assertTrue(form.is_valid())

    def test_players_can_not_be_same(self):
        form = MatchForm(data={
            "player1": self.test_player1,
            "player2": self.test_player1,
            "location": self.location
        })
        self.assertFalse(form.is_valid())

    def test_registration_form_player_creation_is_valid(self):
        form_data = {
            "first_name": "test",
            "last_name": "user3",
            "location": self.location,
            "username": "testuser3",
            "email": "testuser@test.com",
            "password1": "pass123pass",
            "password2": "pass123pass",
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
