from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Crew, VesselType, Vessel, Company, Position


@admin.register(Crew)
class CrewAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",
                                             "salary",
                                             "date_of_birth",
                                             "date_of_joining",
                                             "date_of_leaving",
                                             "vessel",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",
                                         "salary",
                                         "date_of_birth",
                                         "date_of_joining",
                                         "date_of_leaving",
                                         "vessel_type",
                                         "vessel")}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (("Additional info", {"fields": ("first_name",
                                         "last_name",
                                         "position",
                                         "vessel")},),)
    )


@admin.register(Vessel)
class VesselAdmin(admin.ModelAdmin):
    search_fields = ("name", "vessel_type",)
    list_filter = ("name", "vessel_type", "company",)
    list_display = ("name", "vessel_type", "company", "sailors_names",)

    def sailors_names(self, obj):
        return ", ".join([sailor.username for sailor in obj.sailors.all()])


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("country",)


admin.site.register(VesselType)
admin.site.register(Position)
