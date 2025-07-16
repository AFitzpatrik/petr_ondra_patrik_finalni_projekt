from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from api.serializers import EventsSerializer
from viewer.models import Event


class Events(ListModelMixin, GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)