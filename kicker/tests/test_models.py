import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from kicker.models import Location


class ModelTest(TestCase):
    def setUp(self) -> None:
        self.location = Location.objects.create(
            name="Test Location",
            address="Test Address",
            working_hours="-",
        )
        self.player = get_user_model().objects.create_user(
            username="test user",
            first_name="test first_name",
            last_name="test last_name",
            password="testuser",
            location=self.location
        )

    def test_player_correct_str_display(self):
        self.assertEqual(
            str(self.player), "test first_name test last_name"
        )

    def test_location_correct_str_display(self):
        self.assertEqual(
            str(self.location), "Test Location"
        )

    def test_default_player_data_added(self):
        self.assertFalse(self.player.is_pro)
        self.assertEqual(self.player.rating, 1000)

    def test_data_and_timezone_of_player(self):
        self.assertEqual(self.player.registration_date,
                         datetime.datetime.now(tz=datetime.timezone.utc))
