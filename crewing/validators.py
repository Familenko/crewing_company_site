import datetime

from django.core.exceptions import ValidationError


def validate_IMO_number(imo_number):
    if len(str(imo_number)) != 7:
        raise ValidationError("IMO number should consist of 7 characters")

    return imo_number


def validate_name(name):
    if not name.istitle():
        raise ValidationError("Name should start with a capital letter")

    return name


def validate_date_of_joining(date_of_joining):
    if date_of_joining < datetime.datetime.now().date():
        raise ValidationError("Date of joining should be in the future")

    return date_of_joining
