from django.contrib import admin
from django.contrib.auth.models import User

from viewer.models import Event, Location, City, Country, Comment, Type


admin.site.register(Event)
admin.site.register(Location)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(Comment)
admin.site.register(Type)

