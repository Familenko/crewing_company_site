from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class VesselType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "vessel_type"
        verbose_name_plural = "vessel_types"
        ordering = ["name"]


class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)
    responsibility = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "position"
        verbose_name_plural = "positions"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("crewing:position-detail", kwargs={"pk": self.pk})


class Crew(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='sailors', null=True, blank=True)
    salary = models.IntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    date_of_leaving = models.DateField(null=True, blank=True)
    vessel_type = models.ManyToManyField(VesselType, related_name='sailors')
    vessel = models.ForeignKey('Vessel', on_delete=models.DO_NOTHING, related_name='sailors', null=True, blank=True)

    class Meta:
        verbose_name_plural = "sailors"
        verbose_name = "sailor"
        ordering = ["-position"]

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("crewing:crew-detail", kwargs={"pk": self.pk})


class Vessel(models.Model):
    name = models.CharField(max_length=50)
    IMO_number = models.IntegerField(unique=True)
    vessel_type = models.ForeignKey(VesselType, on_delete=models.CASCADE, related_name='vessels')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='vessels')

    class Meta:
        verbose_name_plural = "vessels"
        verbose_name = "vessel"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("crewing:vessel-detail", kwargs={"pk": self.pk})


class Company(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "companies"
        verbose_name = "company"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("crewing:company-detail", kwargs={"pk": self.pk})
