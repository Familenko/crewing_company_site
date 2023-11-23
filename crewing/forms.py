import random

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from crewing.models import VesselType, Vessel, Company, Position
from crewing.validators import validate_IMO_number, validate_name, validate_date_of_joining


class CrewCreationForm(UserCreationForm):
    vessel_type = forms.ModelMultipleChoiceField(
        queryset=VesselType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "position",
            "first_name",
            "last_name",
            "salary",
            "date_of_birth",
            "date_of_joining",
            "date_of_leaving",
            "vessel_type",
            "vessel",
        )

    def clean_first_name(self):
        return validate_name(self.cleaned_data["first_name"])

    def clean_last_name(self):
        return validate_name(self.cleaned_data["last_name"])

    def clean_date_of_joining(self):
        return validate_date_of_joining(self.cleaned_data["date_of_joining"])


class CrewUpdateForm(forms.ModelForm):
    vessel_type = forms.ModelMultipleChoiceField(
        queryset=VesselType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = get_user_model()
        fields = (
            "position",
            "salary",
            "date_of_birth",
            "date_of_joining",
            "date_of_leaving",
            "vessel_type",
            "vessel",
        )


class CrewSearchForm(forms.Form):
    example_user = [
        "john, JOHN, joh",
        "mike, MIKE, MI",
        "alex, ALEX, a",
        "bob, BOB, bo",
        "alice, ALICE, ALI"
    ]

    example_position = [
        "captain, CAPTAIN, cap",
        "chief, CHIEF, ch",
        "mate, MATE, ma",
        "engineer, ENGINEER, en",
        "cook, COOK, co"
    ]

    example_last_name = [
        "johnson, JOHNSON, joh",
        "mike, MIKE, MI",
        "alex, ALEX, a",
        "bob, BOB, bo",
        "alice, ALICE, ALI"
    ]

    example_vessel = [
        "Kara Sea, kara",
        "Pine 5, pine, 5",
        "Hoegh Pusan, hoegh, pusan",
    ]

    def __init__(self, *args, **kwargs):
        super(CrewSearchForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = f"user: {random.choice(self.example_user)}"
        self.fields["position"].widget.attrs["placeholder"] = f"position: {random.choice(self.example_position)}"
        self.fields["last_name"].widget.attrs["placeholder"] = f"last_name: {random.choice(self.example_last_name)}"
        self.fields["vessel"].widget.attrs["placeholder"] = f"vessel: {random.choice(self.example_vessel)}"

    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(),
    )

    position = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(),
    )

    last_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(),
    )

    vessel = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(),
    )

    def filter_queryset(self, queryset):
        username = self.cleaned_data.get("username")
        position = self.cleaned_data.get("position")
        last_name = self.cleaned_data.get("last_name")
        vessel = self.cleaned_data.get("vessel")

        if username:
            queryset = queryset.filter(username__icontains=username)
        if position:
            queryset = queryset.filter(position__name__icontains=position)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if vessel:
            queryset = queryset.filter(vessel__name__icontains=vessel)

        return queryset


class VesselSearchForm(forms.Form):
    example_name = [
        "Kara Sea, kara",
        "Pine 5, pine, 5",
        "Hoegh Pusan, hoegh, pusan",
    ]

    def __init__(self, *args, **kwargs):
        super(VesselSearchForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["placeholder"] = f"name: {random.choice(self.example_name)}"

    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(),
    )

    def filter_queryset(self, queryset):
        name = self.cleaned_data.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


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

    def clean_IMO_number(self):
        return validate_IMO_number(self.cleaned_data["IMO_number"])


class VesselTypeForm(forms.ModelForm):
    class Meta:
        model = VesselType
        fields = "__all__"


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = "__all__"
