from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.utils.timezone import now
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from .forms import (
    CommentForm,
    CityModelForm,
    CountryModelForm,
    EventForm,
    TypeModelForm,
    LocationModelForm,
)
from viewer.models import Event, Comment, Country, City, Location, Reservation, Type
from viewer.api_weather import get_weather_for_city
from viewer.api_country import get_country_info
from django.db.models import Count
from django.http import Http404


def home(request):
    return render(request, "home.html")


class EventsListView(ListView):
    template_name = "events.html"
    model = Event
    context_object_name = "events"
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.GET.get("city")
        type = self.request.GET.get("type")
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        country_name = self.request.GET.get("country_name")

        if city:
            queryset = queryset.filter(location__city__name__icontains=city)

        if type:
            queryset = queryset.filter(type__name__icontains=type)

        if start_date:
            queryset = queryset.filter(start_date_time__date__gte=start_date)

        if end_date:
            queryset = queryset.filter(end_date_time__date__lte=end_date)

        if country_name:
            queryset = queryset.filter(
                location__city__country__name__iexact=country_name
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["city"] = self.request.GET.get("city", "")
        context["type"] = self.request.GET.get("type", "")
        context["start_date"] = self.request.GET.get("start_date", "")
        context["end_date"] = self.request.GET.get("end_date", "")
        context["country_name"] = self.request.GET.get("country_name", "")
        return context


class CitiesListView(ListView):
    template_name = "cities.html"
    model = City
    context_object_name = "cities"


class LocationsListView(ListView):
    template_name = "locations.html"
    model = Location
    context_object_name = "locations"


class EventCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "event_form.html"
    success_url = reverse_lazy("events")
    permission_required = "viewer.add_event"
    login_url = "login"
    raise_exception = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Přidáme města pro modal lokace
        context['cities'] = City.objects.all()
        return context

    def form_valid(self, form):
        form.instance.owner_of_event = self.request.user
        return super().form_valid(form)


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    comments = event.comments.all().order_by("-created_at")

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.event = event
                comment.user = request.user
                comment.save()
                return redirect("event_detail", pk=event.pk)
        else:
            return redirect("login")
    else:
        form = CommentForm()

    return render(
        request,
        "event_detail.html",
        {
            "event": event,
            "comments": comments,
            "form": form,
        },
    )


class EventUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = "event_update_form.html"
    model = Event
    form_class = EventForm
    permission_required = "viewer.change_event"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner_of_event != request.user and not request.user.is_superuser:
            return HttpResponseForbidden("Nemáte oprávnění upravovat tuto událost.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("event_detail", kwargs={"pk": self.object.pk})

    def form_invalid(self, form):
        print("Formulář není validní")
        return super().form_invalid(form)


class EventDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = "event_delete_form.html"
    model = Event
    success_url = reverse_lazy("events")
    permission_required = "viewer.delete_event"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner_of_event != request.user and not request.user.is_superuser:
            return HttpResponseForbidden("Nemáte oprávnění mazat tuto událost.")
        return super().dispatch(request, *args, **kwargs)


class EventDetailView(DetailView):
    model = Event
    template_name = "event_detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city_name = self.object.location.city.name
        weather = get_weather_for_city(city_name)
        context["weather"] = weather
        context["comment_form"] = CommentForm()

        if self.request.user.is_authenticated:
            has_reservation = self.object.reservations.filter(
                user=self.request.user
            ).exists()
        else:
            has_reservation = False

        context["has_reservation"] = has_reservation

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect("login")

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = self.object
            comment.user = request.user
            comment.save()
            return redirect("event_detail", pk=self.object.pk)

        context = self.get_context_data()
        context["comment_form"] = form
        return self.render_to_response(context)


class CountryListView(ListView):
    template_name = "countries.html"
    model = Country
    context_object_name = "countries"

    def get_queryset(self):
        return Country.objects.annotate(
            event_count=Count("cities__locations__events", distinct=True)
        ).order_by("name")


class CountryDetailView(DetailView):
    template_name = "country_detail.html"
    model = Country
    context_object_name = "country"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["api_data"] = get_country_info(self.object.name)
        return context


class CountryCreateView(CreateView):
    model = Country
    form_class = CountryModelForm
    template_name = "country_form.html"
    success_url = reverse_lazy("countries")

    def form_invalid(self, form):
        messages.error(self.request, "Formulář nebyl správně vyplněn.")
        return super().form_invalid(form)


class CountryUpdateView(LoginRequiredMixin, UpdateView):
    model = Country
    form_class = CountryModelForm
    template_name = "country_form.html"
    success_url = reverse_lazy("countries")


class CountryDeleteView(LoginRequiredMixin, DeleteView):
    model = Country
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy("countries")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.cities.filter(locations__events__isnull=False).exists():
            messages.error(self.request, "Nelze smazat stát, protože obsahuje události.")
            raise Http404("Nelze smazat stát s událostmi.")

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_label"] = "stát"
        context["cancel_url"] = reverse("countries")
        return context


class CityCreateView(LoginRequiredMixin, CreateView):
    model = City
    form_class = CityModelForm
    template_name = "city_form.html"
    success_url = reverse_lazy("cities")

    def form_invalid(self, form):
        messages.error(self.request, "Formulář nebyl správně vyplněn.")
        return super().form_invalid(form)


class CityUpdateView(UpdateView):
    model = City
    form_class = CityModelForm
    template_name = "city_form.html"
    success_url = reverse_lazy("cities")


class CityDeleteView(LoginRequiredMixin, DeleteView):
    model = City
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy("cities")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_label"] = "město"
        context["cancel_url"] = reverse("cities")
        return context


def search(request):
    search = request.GET.get("search", "").strip()
    filter_type = request.GET.get("filter", "all")

    events = Event.objects.all()
    if search:
        events = events.filter(name__icontains=search)

    now_time = now()
    if filter_type == "future":
        events = events.filter(start_date_time__gte=now_time)
    elif filter_type == "active_future":
        events = events.filter(end_date_time__gte=now_time)

    context = {
        "events": events.order_by("start_date_time"),
        "search": search,
        "filter": filter_type,
    }
    return render(request, "search.html", context)


class ProfileDetailView(DetailView):
    model = User
    template_name = "profile_detail.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context["reservations"] = Reservation.objects.filter(user=user)

        # Zobrazení vytvořených událostí pro administrátora
        if user.is_superuser:
            context["created_events"] = Event.objects.filter(owner_of_event=user)

        # Zobrazení rezervovaných událostí pro uživatele
        context["my_events"] = Event.objects.filter(reservations__user=user)

        return context


@login_required
def make_reservation(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.available_spots <= 0:
        messages.error(request, "Událost je plně obsazena.")
    else:
        reservation, created = Reservation.objects.get_or_create(
            user=request.user, event=event
        )
        if created:
            messages.success(request, "Rezervace byla úspěšně vytvořena.")
        else:
            messages.info(request, "Už máš rezervaci na tuto událost.")

    return redirect("event_detail", pk=event_id)


@login_required
def cancel_reservation(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reservation = Reservation.objects.filter(user=request.user, event=event).first()

    if reservation:
        reservation.delete()
        messages.success(request, "Rezervace byla zrušena.")
    else:
        messages.info(request, "Nemáš rezervaci na tuto událost.")

    return redirect("event_detail", pk=event_id)


class TypeCreateView(PermissionRequiredMixin, CreateView):
    model = Type
    form_class = TypeModelForm
    template_name = "type_form.html"
    success_url = reverse_lazy("event_create")
    permission_required = "viewer.add_type"

    def form_valid(self, form):
        response = super().form_valid(form)

        # Kontrola, zda je to AJAX požadavek
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Typ byl úspěšně vytvořen!'
            })

        return response

    def form_invalid(self, form):
        # Kontrola, zda je to AJAX požadavek
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Vrátit HTML s chybami pro modal
            html = render_to_string('type_form.html', {
                'form': form
            }, request=self.request)
            return JsonResponse({
                'success': False,
                'html': html
            })

        messages.error(self.request, "Název typu je neplatný nebo již existuje.")
        return super().form_invalid(form)


class LocationCreateView(PermissionRequiredMixin, CreateView):
    model = Location
    form_class = LocationModelForm
    template_name = "location_form.html"
    success_url = reverse_lazy("event_create")
    permission_required = "viewer.add_location"

    def form_valid(self, form):
        response = super().form_valid(form)

        # Kontrola, zda je to AJAX požadavek
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Lokace byla úspěšně vytvořena!'
            })

        return response

    def form_invalid(self, form):
        # Kontrola, zda je to AJAX požadavek
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Vrátit HTML s chybami pro modal
            html = render_to_string('location_form.html', {
                'form': form
            }, request=self.request)
            return JsonResponse({
                'success': False,
                'html': html
            })

        messages.error(
            self.request,
            "Místo s tímto názvem a adresou už existuje nebo nejsou vyplněna všechna pole.",
        )
        return super().form_invalid(form)
