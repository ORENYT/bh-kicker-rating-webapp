from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

URLS = [
    reverse("kicker:index"),
    reverse("kicker:table"),
    reverse("kicker:register"),
    reverse("kicker:login"),
]


class PublicViewsTest(TestCase):
    def test_login_not_required(self):
        for url in URLS:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
