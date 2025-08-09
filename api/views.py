from datetime import timezone
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now, make_aware, get_current_timezone
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveDestroyAPIView
from rest_framework.mixins import ListModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from api.serializers import EventsSerializer
from viewer.models import Event


class EventsAPI(ListModelMixin, GenericAPIView):
    serializer_class = EventsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(start_date_time__gte=now()).order_by('start_date_time')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AllEventsAPI(ListModelMixin, GenericAPIView):
    queryset = Event.objects.all().order_by('start_date_time')
    serializer_class = EventsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FilteredEventsAPI(ListModelMixin, GenericAPIView):
    serializer_class = EventsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        start_param = self.request.query_params.get('start')
        end_param = self.request.query_params.get('end')
        start = parse_datetime(start_param) if start_param else None
        end = parse_datetime(end_param) if end_param else None

        current_tz = get_current_timezone()

        if start and start.tzinfo is None:
            start = make_aware(start, timezone=current_tz)
        if end and end.tzinfo is None:
            end = make_aware(end, timezone=current_tz)

        queryset = Event.objects.all().order_by('start_date_time')

        if start and end:
            queryset = queryset.filter(
                end_date_time__gte=start,
                start_date_time__lte=end
            )
        elif start:
            queryset = queryset.filter(end_date_time__gte=start)
        elif end:
            queryset = queryset.filter(start_date_time__lte=end)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
