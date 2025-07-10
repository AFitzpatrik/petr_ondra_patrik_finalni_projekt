from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.views.generic import DetailView

from viewer.models import Event, City, Location
from .forms import EventForm

def home(request):
    return render(request, 'home.html')


class EventsListView(ListView):
    template_name = 'events.html'
    model = Event
    context_object_name = 'events'


class EventDetailView(DetailView): #Eventdetail
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'

class CitiesListView(ListView):
    template_name = 'cities.html'
    model = City
    context_object_name = 'cities'

class LocationsListView(ListView):
    template_name = 'locations.html'
    model = Location
    context_object_name = 'locations'

class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'
    success_url = reverse_lazy('events')

    def form_valid(self, form):
        form.instance.owner_of_event = self.request.user
        return super().form_valid(form)
