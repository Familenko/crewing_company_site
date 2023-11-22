import random

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from crewing.models import VesselType, Vessel, Company, Position


class CrewForm(UserCreationForm):
    vessel_type = forms.ModelChoiceField(
        queryset=VesselType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "position",
            "salary",
            "date_of_birth",
            "date_of_joining",
            "date_of_leaving",
            "vessel_type",
            "vessel",
        )


class CompanyForm(forms.ModelForm):
    vessels = forms.ModelMultipleChoiceField(
        queryset=Vessel.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Company
        fields = "__all__"


class VesselForm(forms.ModelForm):
    class Meta:
        model = Vessel
        fields = "__all__"


class VesselTypeForm(forms.ModelForm):
    class Meta:
        model = VesselType
        fields = "__all__"


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = "__all__"
