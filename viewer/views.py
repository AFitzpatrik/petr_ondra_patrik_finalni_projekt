from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.utils.timezone import now
from django.views.generic import ListView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from .forms import CommentForm
from viewer.models import Event, Comment

from viewer.api_weather import get_weather_for_city
from viewer.models import Event, City, Location
from .forms import EventForm

def home(request):
    return render(request, 'home.html')


class EventsListView(ListView):
    template_name = 'events.html'
    model = Event
    context_object_name = 'events'

"""
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
"""
class CitiesListView(ListView):
    template_name = 'cities.html'
    model = City
    context_object_name = 'cities'

class LocationsListView(ListView):
    template_name = 'locations.html'
    model = Location
    context_object_name = 'locations'

class EventCreateView(LoginRequiredMixin,CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'
    success_url = reverse_lazy('events')

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
                return redirect('event-detail', pk=event.pk)
        else:
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'event_detail.html', {
        'event': event,
        'comments': comments,
        'form': form,
    })

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
            return redirect('event-detail', pk=self.object.pk)

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



