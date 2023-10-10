from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kicker.admin import LocationAdmin
from kicker.models import Location


class TestAdminPanel(TestCase):
    def setUp(self) -> None:
        admin = get_user_model().objects.create_superuser(
            username="testadmin",
            password="testadmin"
        )
        self.client.force_login(admin)
        self.admin_site = AdminSite()
        self.location_admin = LocationAdmin(Location, self.admin_site)

    def test_location_is_on_admin_page_and_admins_not_required(self):
        url = reverse("admin:kicker_location_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        form = self.location_admin.get_form(response)(instance=None)
        self.assertFalse(form.base_fields["admins"].required)
