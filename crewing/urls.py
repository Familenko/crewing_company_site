from django.urls import path

from .views import index, VesselListView, CrewListView

urlpatterns = [
    path("", index, name="index"),
    path("vessels/", VesselListView.as_view(), name="vessel-list"),
    path("crew/", CrewListView.as_view(), name="crew-list"),
]

app_name = "crewing"
