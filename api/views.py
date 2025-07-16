from django.utils.dateparse import parse_datetime
from django.utils.timezone import now
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from api.serializers import EventsSerializer
from viewer.models import Event


class Events(ListModelMixin, GenericAPIView):
    serializer_class = EventsSerializer

    def get_queryset(self):
        return Event.objects.filter(start_date_time__gte=now()).order_by('start_date_time')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AllEvents(ListModelMixin, GenericAPIView):
    queryset = Event.objects.all().order_by('start_date_time')
    serializer_class = EventsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FilteredEvents(ListModelMixin, GenericAPIView):
    serializer_class = EventsSerializer

    def get_queryset(self):
        queryset = Event.objects.all().order_by('start_date_time')
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')

        if start:
            dt = parse_datetime(start)
            if dt:
                queryset = queryset.filter(start_date_time__gte=dt)

        if end:
            dt = parse_datetime(end)
            if dt:
                queryset = queryset.filter(start_date_time__lte=dt)

        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)