from datetime import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now, make_aware
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated

from api.serializers import EventsSerializer
from viewer.models import Event


class Events(ListModelMixin, GenericAPIView):
    serializer_class = EventsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(start_date_time__gte=now()).order_by('start_date_time')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AllEvents(ListModelMixin, GenericAPIView):
    queryset = Event.objects.all().order_by('start_date_time')
    serializer_class = EventsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FilteredEvents(ListModelMixin, GenericAPIView):
    serializer_class = EventsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        start_param = self.request.query_params.get('start')
        end_param = self.request.query_params.get('end')
        start = parse_datetime(start_param)
        end = parse_datetime(end_param)

        if start and start.tzinfo is None:
            start = make_aware(start, timezone=timezone.utc)
        if end and end.tzinfo is None:
            end = make_aware(end, timezone=timezone.utc)

        queryset = Event.objects.all().order_by('start_date_time')

        if start:
            queryset = queryset.filter(start_date_time__gte=start)
        if end:
            queryset = queryset.filter(start_date_time__lte=end)

        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

