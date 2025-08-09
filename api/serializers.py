from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from viewer.models import Event


class EventsSerializer(ModelSerializer):
    owner_of_event = serializers.CharField(source='owner_of_event.username')
    location = serializers.CharField(source='location.name')
    address = serializers.CharField(source='location.address')
    city = serializers.CharField(source='location.city.name')
    country = serializers.CharField(source='location.city.country.name')

    class Meta:
        model = Event
        fields = [
            'id',
            'name',
            'start_date_time',
            'end_date_time',
            'owner_of_event',
            'location',
            'address',
            'city',
            'country',
            'description'
        ]
