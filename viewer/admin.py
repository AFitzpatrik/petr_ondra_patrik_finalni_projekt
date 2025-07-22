from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

from viewer.models import Event, Location, City, Country, Comment, Type


class CityAdmin(ModelAdmin):
    list_display = ['id', 'name', 'zip_code', 'country']
    list_display_links = ['id', 'name']
    list_per_page = 10


class CommentAdmin(ModelAdmin):
    list_display = ['id', 'user', 'event', 'date_time_posted']
    list_display_links = ['id', 'user', 'event']
    list_per_page = 10


class CountryAdmin(ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    list_per_page = 10


class EventAdmin(ModelAdmin):  #ted se tam zobrazovalo co je v __str__
    list_display = ['id', 'name', 'type', 'start_date_time', 'capacity']
    list_display_links = ['id', 'name']
    list_per_page = 10
    list_filter = ['type', 'start_date_time']
    search_fields = ['name', 'type__name', 'location__city__name']


class LocationAdmin(ModelAdmin):
    list_display = ['id', 'name', 'address', 'city']
    list_display_links = ['id', 'name']
    list_per_page = 10


class TypeAdmin(ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    list_per_page = 10


admin.site.register(Event, EventAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Type, TypeAdmin)

