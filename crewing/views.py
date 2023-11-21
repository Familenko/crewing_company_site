from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from crewing.models import Crew, Vessel, Company


@login_required
def index(request):
    """View function for the home page of the site."""

    num_sailors = Crew.objects.count()
    num_vessels = Vessel.objects.count()
    num_companies = Company.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_sailors": num_sailors,
        "num_vessels": num_vessels,
        "num_companies": num_companies,
        "num_visits": num_visits + 1,
    }

    return render(request, "crewing/index.html", context=context)


class CrewListView(LoginRequiredMixin, generic.ListView):
    model = Crew
    context_object_name = "crew_list"
    template_name = "crewing/crew_list.html"
    paginate_by = 10


class VesselListView(LoginRequiredMixin, generic.ListView):
    model = Vessel
    context_object_name = "vessel_list"
    template_name = "crewing/vessel_list.html"
    paginate_by = 10


class CompanyListView(LoginRequiredMixin, generic.ListView):
    model = Company
    context_object_name = "company_list"
    template_name = "crewing/company_list.html"
    paginate_by = 10


