from django.urls import path

from .views import (
    index,
    toggle_assign_to_vessel,

    VesselListView,
    VesselDetailView,
    VesselCreateView,
    VesselUpdateView,
    VesselDeleteView,

    CrewListView,
    CrewDetailView,
    CrewCreateView,
    CrewUpdateView,
    CrewDeleteView,

    VesselTypeListView,
    VesselTypeCreateView,
    VesselTypeUpdateView,
    VesselTypeDeleteView,

    PositionListView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    PositionDetailView,

    CompanyDetailView,
    CompanyListView,
    CompanyCreateView,
    CompanyUpdateView,
    CompanyDeleteView,
)

urlpatterns = [
    path("", index, name="index"),

    path("vessels/", VesselListView.as_view(), name="vessel-list"),
    path("vessels/<int:pk>/", VesselDetailView.as_view(), name="vessel-detail"),
    path("vessels/create/", VesselCreateView.as_view(), name="vessel-create"),
    path("vessels/<int:pk>/update/", VesselUpdateView.as_view(), name="vessel-update"),
    path("vessels/<int:pk>/delete/", VesselDeleteView.as_view(), name="vessel-delete"),
    path("vessels/<int:pk>/toggle-assign/", toggle_assign_to_vessel, name="toggle-vessel-assign"),

    path("vessel_types/", VesselTypeListView.as_view(), name="vessel-type-list"),
    path("vessel_types/create/", VesselTypeCreateView.as_view(), name="vessel-type-create"),
    path("vessel_types/<int:pk>/update/", VesselTypeUpdateView.as_view(), name="vessel-type-update"),
    path("vessel_types/<int:pk>/delete/", VesselTypeDeleteView.as_view(), name="vessel-type-delete"),

    path("crew/", CrewListView.as_view(), name="crew-list"),
    path("crew/<int:pk>/", CrewDetailView.as_view(), name="crew-detail"),
    path("crew/create/", CrewCreateView.as_view(), name="crew-create"),
    path("crew/<int:pk>/update/", CrewUpdateView.as_view(), name="crew-update"),
    path("crew/<int:pk>/delete/", CrewDeleteView.as_view(), name="crew-delete"),

    path("company/", CompanyListView.as_view(), name="company-list"),
    path("company/<int:pk>/", CompanyDetailView.as_view(), name="company-detail"),
    path("company/create/", CompanyCreateView.as_view(), name="company-create"),
    path("company/<int:pk>/update/", CompanyUpdateView.as_view(), name="company-update"),
    path("company/<int:pk>/delete/", CompanyDeleteView.as_view(), name="company-delete"),

    path("position/", PositionListView.as_view(), name="position-list"),
    path("position/<int:pk>/", PositionDetailView.as_view(), name="position-detail"),
    path("position/create/", PositionCreateView.as_view(), name="position-create"),
    path("position/<int:pk>/update/", PositionUpdateView.as_view(), name="position-update"),
    path("position/<int:pk>/delete/", PositionDeleteView.as_view(), name="position-delete"),
]

app_name = "crewing"
