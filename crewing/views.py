from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from crewing.models import Crew, Vessel, Company, VesselType, Position
from crewing.forms import CrewForm, VesselForm, CompanyForm, VesselTypeForm, PositionForm


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
    template_name = "crewing/crew/list.html"
    paginate_by = 10


class VesselListView(LoginRequiredMixin, generic.ListView):
    model = Vessel
    context_object_name = "vessel_list"
    template_name = "crewing/vessel/list.html"
    paginate_by = 10


class CompanyListView(LoginRequiredMixin, generic.ListView):
    model = Company
    context_object_name = "company_list"
    template_name = "crewing/company/list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        companies = context['company_list']

        companies_vessels_count = {}
        companies_workers_count = {}

        for company in companies:
            vessels = company.vessels.all()

            workers_count = Crew.objects.filter(vessel__in=vessels).count()

            companies_vessels_count[company.id] = vessels.count()
            companies_workers_count[company.id] = workers_count

        context['vessels_count'] = companies_vessels_count
        context['workers_count'] = companies_workers_count

        return context


class VesselTypeListView(LoginRequiredMixin, generic.ListView):
    model = VesselType
    context_object_name = "vessel_type_list"
    template_name = "crewing/vessel_type/list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for vessel_type in context['vessel_type_list']:
            vessel_type.vessels.set(Vessel.objects.filter(vessel_type=vessel_type)[:3])

        return context


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    context_object_name = "position_list"
    template_name = "crewing/position/list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        positions = context['position_list']

        positions_workers_count = {}

        for position in positions:
            workers_count = Crew.objects.filter(position=position).count()

            positions_workers_count[position.id] = workers_count

        context['workers_count'] = positions_workers_count

        return context


class CrewDetailView(LoginRequiredMixin, generic.DetailView):
    model = Crew
    template_name = "crewing/crew/detail.html"

    def get_queryset(self):
        return Crew.objects.select_related('position', 'vessel').prefetch_related('vessel_type')


class VesselDetailView(LoginRequiredMixin, generic.DetailView):
    model = Vessel
    template_name = "crewing/vessel/detail.html"

    def get_queryset(self):
        return Vessel.objects.select_related('vessel_type', 'company')


class CompanyDetailView(LoginRequiredMixin, generic.DetailView):
    model = Company
    template_name = "crewing/company/detail.html"


class CrewCreateView(LoginRequiredMixin, generic.CreateView):
    model = Crew
    form_class = CrewForm
    fields = "__all__"
    success_url = reverse_lazy("crewing:crew-list")


class CrewUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Crew
    form_class = CrewForm
    fields = "__all__"
    success_url = reverse_lazy("crewing:crew-list")


class CrewDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Crew
    success_url = reverse_lazy("crewing:crew-list")


class VesselCreateView(LoginRequiredMixin, generic.CreateView):
    model = Vessel
    form_class = VesselForm
    fields = "__all__"
    success_url = reverse_lazy("crewing:vessel-list")


class VesselUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Vessel
    form_class = VesselForm
    fields = "__all__"
    success_url = reverse_lazy("crewing:vessel-list")


class VesselDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Vessel
    success_url = reverse_lazy("crewing:vessel-list")


class CompanyCreateView(LoginRequiredMixin, generic.CreateView):
    model = Company
    form_class = CompanyForm
    fields = "__all__"
    success_url = reverse_lazy("crewing:company-list")


class CompanyUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Company
    form_class = CompanyForm
    fields = "__all__"
    success_url = reverse_lazy("crewing:company-list")


class CompanyDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Company
    success_url = reverse_lazy("crewing:company-list")


class VesselTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = VesselType
    form_class = VesselTypeForm
    fields = "__all__"
    success_url = reverse_lazy("crewing:vessel-type-list")


class VesselTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = VesselType
    form_class = VesselTypeForm
    fields = "__all__"
    success_url = reverse_lazy("crewing:vessel-type-list")


class VesselTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = VesselType
    success_url = reverse_lazy("crewing:vessel-type-list")


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    form_class = PositionForm
    fields = "__all__"
    success_url = reverse_lazy("crewing:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    form_class = PositionForm
    fields = "__all__"
    success_url = reverse_lazy("crewing:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("crewing:position-list")