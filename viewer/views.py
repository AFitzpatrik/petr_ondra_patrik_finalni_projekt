from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.timezone import now
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .forms import CommentForm, EventForm
from viewer.models import Event, Comment, City, Location, Reservation
from viewer.api_weather import get_weather_for_city
from django.db.models import Count


def home(request):
    return render(request, 'home.html')


class EventsListView(ListView):
    template_name = 'events.html'
    model = Event
    context_object_name = 'events'


class CitiesListView(ListView):
    template_name = 'cities.html'
    model = City
    context_object_name = 'cities'

    def get_queryset(self):
        return City.objects.annotate(event_count=Count('locations__events'))


class LocationsListView(ListView):
    template_name = 'locations.html'
    model = Location
    context_object_name = 'locations'


class EventCreateView(PermissionRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'
    success_url = reverse_lazy('events')
    permission_required = 'viewer.add_event'

    def form_valid(self, form):
        form.instance.owner_of_event = self.request.user
        return super().form_valid(form)


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    comments = event.comments.all().order_by('-created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.event = event
                comment.user = request.user
                comment.save()
                return redirect('event_detail', pk=event.pk)
        else:
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'event_detail.html', {
        'event': event,
        'comments': comments,
        'form': form,
    })


class EventUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'event_update_form.html'
    model = Event
    form_class = EventForm
    permission_required = 'viewer.change_event'

    def get_success_url(self):
        return reverse("event_detail", kwargs={"pk": self.object.pk})

    def form_invalid(self, form):
        print('Formulář není validní')
        return super().form_invalid(form)


class EventDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'event_delete_form.html'
    model = Event
    success_url = reverse_lazy('events')
    permission_required = 'viewer.delete_event'


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city_name = self.object.location.city.name
        weather = get_weather_for_city(city_name)
        context['weather'] = weather
        context['comment_form'] = CommentForm()

        if self.request.user.is_authenticated:
            has_reservation = self.object.reservations.filter(user=self.request.user).exists()
        else:
            has_reservation = False

        context['has_reservation'] = has_reservation

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = self.object
            comment.user = request.user
            comment.save()
            return redirect('event_detail', pk=self.object.pk)

        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)


def search(request):
    search = request.GET.get('search', '').strip()
    filter_type = request.GET.get('filter', 'all')

    events = Event.objects.all()
    if search:
        events = events.filter(name__icontains=search)

    now_time = now()
    if filter_type == 'future':
        events = events.filter(start_date_time__gte=now_time)
    elif filter_type == 'active_future':
        events = events.filter(end_date_time__gte=now_time)

    context = {
        'events': events.order_by('start_date_time'),
        'search': search,
        'filter': filter_type
    }
    return render(request, 'search.html', context)


class ProfileDetailView(DetailView):
    model = User
    template_name = 'profile_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['reservations'] = Reservation.objects.filter(user=user)
        return context

@login_required
def make_reservation(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.available_spots <= 0:
        messages.error(request, "Událost je plně obsazena.")
    else:
        reservation, created = Reservation.objects.get_or_create(user=request.user, event=event)
        if created:
            messages.success(request, "Rezervace byla úspěšně vytvořena.")
        else:
            messages.info(request, "Už máš rezervaci na tuto událost.")

    return redirect('event_detail', pk=event_id)

@login_required
def cancel_reservation(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reservation = Reservation.objects.filter(user=request.user, event=event).first()

    if reservation:
        reservation.delete()
        messages.success(request, "Rezervace byla zrušena.")
    else:
        messages.info(request, "Nemáš rezervaci na tuto událost.")

    return redirect('event_detail', pk=event_id)