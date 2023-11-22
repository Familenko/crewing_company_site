from django.urls import path

from .views import (index,
                    VesselListView,
                    CrewListView,
                    VesselTypeListView,
                    CompanyListView,
                    PositionListView,
                    CrewDetailView,
                    VesselDetailView,
                    CompanyDetailView,)

urlpatterns = [
    path("", index, name="index"),

    path("vessels/", VesselListView.as_view(), name="vessel-list"),
    path("vessels/<int:pk>/", VesselDetailView.as_view(), name="vessel-detail"),

    path("vessel_types/", VesselTypeListView.as_view(), name="vessel-type-list"),

    path("crew/", CrewListView.as_view(), name="crew-list"),
    path("crew/<int:pk>/", CrewDetailView.as_view(), name="crew-detail"),

    path("company/", CompanyListView.as_view(), name="company-list"),
    path("company/<int:pk>/", CompanyDetailView.as_view(), name="company-detail"),

    path("position/", PositionListView.as_view(), name="position-list")
]

app_name = "crewing"
