import random
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect

from crewing.models import Crew, Vessel, Company, VesselType, Position
from crewing.forms import VesselForm, CompanyForm, VesselTypeForm, PositionForm, CrewCreationForm, CrewSearchForm, \
    CrewUpdateForm, VesselSearchForm


@login_required
def index(request):

    history_data = [
        "Did you know that Odessa, a bustling port city on the Black Sea in Ukraine, is home to the famous Potemkin Steps? These grand stairs, consisting of 192 steps, were immortalized in the iconic 1925 silent film 'Battleship Potemkin.' The staircase provides a stunning panoramic view of the city and the sea, making it a must-visit landmark for both locals and tourists alike.",
        "Another interesting fact about Odessa is that it's often referred to as the 'Pearl of the Black Sea.' This nickname reflects the city's captivating beauty, rich cultural heritage, and vibrant atmosphere. Odessa is known for its historic architecture, diverse cuisine, and lively arts scene, making it a unique and charming destination for visitors from around the world.",
        "Odessa is home to the world's longest continuous urban catacomb network. The Odessa Catacombs, originally limestone mines, have a total estimated length of around 2,500 kilometers (about 1,553 miles). These catacombs served various purposes throughout history, including as hiding places for partisans during World War II. Today, they remain a mysterious and intriguing underground labyrinth, drawing adventurous explorers and historians to uncover their secrets.",
        "Odessa is also known for its vibrant nightlife scene, with numerous bars, clubs, and restaurants lining the city's streets. The city's nightlife is especially popular among tourists, who flock to Odessa's beaches and clubs during the summer months. In fact, Odessa is often referred to as the 'Las Vegas of the Black Sea' due to its lively nightlife and entertainment options.",
        "Odessa is home to the world's largest underground shopping mall. The Odessa Catacombs, originally limestone mines, have a total estimated length of around 2,500 kilometers (about 1,553 miles). These catacombs served various purposes throughout history, including as hiding places for partisans during World War II. Today, they remain a mysterious and intriguing underground labyrinth, drawing adventurous explorers and historians to uncover their secrets.",
        "Odessa is known for its unique and humorous monument to a fictional character. In the city center, you can find a statue of a literary figure named 'Duke de Richelieu.' What makes it interesting is that this character never actually existed in real life. The Duke was created by a French novelist, and the monument was erected to honor the city's founder, Armand-Emmanuel du Plessis, Duc de Richelieu, the French military and political figure. It adds a touch of whimsy to the city's cultural landscape."
    ]

    history = random.choice(history_data)

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
        "history": history,
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
        queryset = Crew.objects.all()

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
        sailors_leaving_soon = Crew.objects.filter(date_of_leaving__gte=one_month_ago)

        context["sailors_leaving_soon"] = sailors_leaving_soon

        placeholder_vessel = self.request.GET.get("vessel")
        context["search_form"] = VesselSearchForm(
            initial={
                "vessel": placeholder_vessel,
            })

        return context

    def get_queryset(self):
        queryset = Vessel.objects.all()

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for vessel_type in context['vessel_type_list']:
            vessel_type.vessels.set(Vessel.objects.filter(vessel_type=vessel_type)[:3])

        return context


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