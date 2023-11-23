from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect

from crewing.models import Crew, Vessel, Company, VesselType, Position
from crewing.forms import (
    VesselForm,
    CompanyForm,
    VesselTypeForm,
    PositionForm,
    CrewCreationForm,
    CrewSearchForm,
    CrewUpdateForm,
    VesselSearchForm
)


@login_required
def index(request):

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


@login_required
def toggle_assign_to_vessel(request, pk):
    sailor = get_object_or_404(Crew, id=request.user.id)
    vessel = get_object_or_404(Vessel, id=pk)

    if vessel == sailor.vessel:
        sailor.vessel = None
    else:
        sailor.vessel = vessel
    sailor.save()

    return HttpResponseRedirect(reverse_lazy("crewing:vessel-detail", args=[pk]))


class CrewListView(LoginRequiredMixin, generic.ListView):
    model = Crew
    context_object_name = "crew_list"
    template_name = "crewing/crew/list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CrewListView, self).get_context_data(**kwargs)
        placeholder_username = self.request.GET.get("username")
        placeholder_position = self.request.GET.get("position")
        placeholder_last_name = self.request.GET.get("last_name")
        placeholder_vessel = self.request.GET.get("vessel")
        context["search_form"] = CrewSearchForm(
            initial={
                "username": placeholder_username,
                "position": placeholder_position,
                "last_name": placeholder_last_name,
                "vessel": placeholder_vessel,
            })
        return context

    def get_queryset(self):
        queryset = Crew.objects.all(
        ).select_related('position', 'vessel')

        search_form = CrewSearchForm(self.request.GET)
        if search_form.is_valid():
            queryset = search_form.filter_queryset(queryset)

        return queryset


class VesselListView(LoginRequiredMixin, generic.ListView):
    model = Vessel
    context_object_name = "vessel_list"
    template_name = "crewing/vessel/list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        one_month_ago = datetime.now() - timedelta(days=30)
        sailors_leaving_soon = Crew.objects.filter(date_of_leaving__lte=one_month_ago)

        context["sailors_leaving_soon"] = sailors_leaving_soon

        placeholder_vessel = self.request.GET.get("vessel")
        context["search_form"] = VesselSearchForm(
            initial={
                "vessel": placeholder_vessel,
            })

        return context

    def get_queryset(self):
        queryset = Vessel.objects.all(
        ).select_related('vessel_type', 'company')

        search_form = VesselSearchForm(self.request.GET)
        if search_form.is_valid():
            queryset = search_form.filter_queryset(queryset)

        return queryset


class CompanyListView(LoginRequiredMixin, generic.ListView):
    model = Company
    context_object_name = "company_list"
    template_name = "crewing/company/list.html"
    paginate_by = 5

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
    paginate_by = 5
    queryset = VesselType.objects.all().prefetch_related(
        Prefetch('vessels', queryset=Vessel.objects.all().order_by('name'))
    )


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    context_object_name = "position_list"
    template_name = "crewing/position/list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        positions = context['position_list']

        positions_workers_count = {}

        for position in positions:
            workers_count = Crew.objects.filter(position=position).count()

            positions_workers_count[position.id] = workers_count

        context['workers_count'] = positions_workers_count

        return context


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position
    template_name = "crewing/position/detail.html"

    def get_queryset(self):
        return Position.objects.prefetch_related('sailors')


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
    form_class = CrewCreationForm
    success_url = reverse_lazy("crewing:crew-list")


class CrewUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Crew
    form_class = CrewUpdateForm
    success_url = reverse_lazy("crewing:crew-list")


class CrewDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Crew
    success_url = reverse_lazy("crewing:crew-list")


class VesselCreateView(LoginRequiredMixin, generic.CreateView):
    model = Vessel
    form_class = VesselForm
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