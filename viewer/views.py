from django.shortcuts import render
from django.utils.timezone import now
from django.views.generic import ListView
from django.views.generic import DetailView

from viewer.api_weather import get_weather_for_city
from viewer.models import Event, City, Location


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city_name = self.object.location.city.name
        weather = get_weather_for_city(city_name)
        context['weather'] = weather
        return context

class CitiesListView(ListView):
    template_name = 'cities.html'
    model = City
    context_object_name = 'cities'

class LocationsListView(ListView):
    template_name = 'locations.html'
    model = Location
    context_object_name = 'locations'


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



