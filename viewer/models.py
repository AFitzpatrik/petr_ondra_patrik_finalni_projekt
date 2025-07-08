from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    
    class Meta:
        verbose_name_plural = 'Countries'
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Country(name={self.name})"


class City(models.Model):
    name = models.CharField(max_length=100, unique=False, null=False, blank=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")
    zip_code = models.CharField(max_length=10, null=False, blank=False)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Cities'
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        country_name = self.country.name if self.country else None
        return f"City(name={self.name}, country={country_name}, zip_code={self.zip_code})"


class Location(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    city = ForeignKey(City, on_delete=models.CASCADE, related_name="locations")
    
    class Meta:
        ordering = ['city__name', 'name']
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        city_name = self.city.name if self.city else None
        return f"Location(name={self.name}, city={city_name}, address={self.address})"


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Type(name={self.name})"


class Event(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="events")
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    start_time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=False, blank=False)
    event_image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    owner_of_event = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_events")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="events")
    
    class Meta:
        ordering = ['start_date', 'name']
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return (f"Event(name={self.name}, description={self.description}, "
                f"start_date={self.start_date}, end_date={self.end_date}, "
                f"location={self.location}, owner_of_event={self.owner_of_event})")


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(null=False, blank=False)
    date_posted = models.DateField(null=False, blank=False)
    time_posted = models.TimeField(null=False, blank=False)
    
    class Meta:
        ordering = ['date_posted', 'time_posted']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.event.name}"

    def __repr__(self):
        return (f"Comment(event={self.event}, user={self.user}, content={self.content},"
                f" date_posted={self.date_posted}, time_posted={self.time_posted})")
