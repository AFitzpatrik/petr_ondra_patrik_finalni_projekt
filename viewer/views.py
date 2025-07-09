from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView

from viewer.models import Event

def home(request):
    return render(request, 'home.html')


class EventsListView(ListView):
    template_name = 'events.html'
    model = Event
    context_object_name = 'events'


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'

