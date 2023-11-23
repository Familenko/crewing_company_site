import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from crewing.models import Vessel, Company, VesselType, Position, Crew


class CrewingTest(TestCase):
    def setUp(self) -> None:
        self.user = Crew.objects.create_user(
            username="Test", password="12345")
        self.client.login(username="Test", password="12345")

        self.vessel_type = VesselType.objects.create(
            name="Bulker",
        )

        self.position = Position.objects.create(
            name="Master",
        )

        self.company = Company.objects.create(
            name="Test Company",
            country="Test Country",
        )

        self.vessel = Vessel.objects.create(
            name="Test",
            IMO_number=1234567,
            vessel_type="Bulker",
            company="Test Company",
        )
    #
    # def test_sailors_leaving_soon(self):
    #     self.user.date_of_leaving = datetime.datetime(2020, 1, 1)
    #     self.user.vessel = self.vessel
    #     self.user.save()
    #
    #     response = self.client.get("/crewing/vessel/")
    #     self.assertEqual(response.context["sailors_leaving_soon"].count(), 1)


