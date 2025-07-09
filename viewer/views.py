from django.shortcuts import render
from django.views.generic import ListView

from viewer.models import Event

def home(request):
    return render(request, 'home.html')


class EventsListView(ListView):
    template_name = 'events.html'
    model = Event
    context_object_name = 'events'

