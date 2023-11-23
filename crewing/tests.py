import datetime

from django.test import TestCase
from django.urls import reverse

from crewing.models import Vessel, Company, VesselType, Position, Crew


class CrewingTest(TestCase):
    def setUp(self) -> None:
        self.user = Crew.objects.create_user(
            username="Test username", password="12345")
        self.client.login(username="Test username", password="12345")

        self.vessel_type = VesselType.objects.create(
            name="Test Vessel Type",
        )

        self.position = Position.objects.create(
            name="Test Position",
        )

        self.company = Company.objects.create(
            name="Test Company",
            country="Test Country",
        )

        self.vessel = Vessel.objects.create(
            name="Test Vessel",
            IMO_number=1234567,
            vessel_type=self.vessel_type,
            company=self.company,
        )

    def test_vessel_search_form(self):
        response = self.client.get(reverse("crewing:vessel-list"), {"vessel": "Test Vessel"})
        self.assertEqual(response.context["vessel_list"][0].name, "Test Vessel")

    def test_user_leaving_soon(self):
        self.user.date_of_leaving = datetime.datetime.now() - datetime.timedelta(days=30)
        self.user.vessel = self.vessel
        self.user.save()

        response = self.client.get(reverse("crewing:vessel-list"))

        self.assertEqual(response.context["vessel_list"][0].name, "Test Vessel")

    def test_sailors_leaving_soon_count(self):
        self.user.date_of_leaving = datetime.datetime.now() - datetime.timedelta(days=30)
        self.user.vessel = self.vessel
        self.user.save()

        response = self.client.get(reverse("crewing:vessel-list"))

        sailors_leaving_soon = response.context["sailors_leaving_soon"]
        self.assertEqual(sailors_leaving_soon.count(), 1)

    def test_sailors_leaving_soon_username(self):
        self.user.date_of_leaving = datetime.datetime.now() - datetime.timedelta(days=30)
        self.user.vessel = self.vessel
        self.user.save()

        response = self.client.get(reverse("crewing:vessel-list"))

        sailors_leaving_soon = response.context["sailors_leaving_soon"]
        self.assertEqual(sailors_leaving_soon[0].username, "Test username")
