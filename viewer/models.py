from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey, DateTimeField
from django.core.exceptions import ValidationError

class Country(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
        error_messages={"unique": "Stát s tímto názvem již existuje."},
    )

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Country(name={self.name})"

    def clean(self):
        # Kontrola, zda existují události v této zemi
        if self.cities.filter(locations__events__isnull=False).exists():
            raise ValidationError("Tento stát nelze smazat, protože obsahuje události.")

    def delete(self, *args, **kwargs):
        self.clean()  # Provádíme kontrolu před smazáním
        super().delete(*args, **kwargs)


class City(models.Model):
    name = models.CharField(max_length=100, unique=False, null=False, blank=False)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="cities"
    )
    zip_code = models.CharField(max_length=10, null=False, blank=False)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Cities"

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
        ordering = ["city__name", "name"]
        unique_together = ("name", "address")

    def __str__(self):
        return self.name

    def __repr__(self):
        city_name = self.city.name if self.city else None
        return f"Location(name={self.name}, city={city_name}, address={self.address})"


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Type(name={self.name})"


class Event(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="events")
    description = models.TextField(null=True, blank=True)
    start_date_time = DateTimeField(null=False, blank=False)
    end_date_time = DateTimeField(null=False, blank=False)
    event_image = models.ImageField(upload_to="event_images/", null=True, blank=True)
    owner_of_event = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_events"
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="events"
    )
    capacity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # Přidání pole pro datum vytvoření

    class Meta:
        ordering = ["start_date_time", "name"]

    def __str__(self):
        return f"{self.name} ({self.start_date_time.strftime('%d.%m.%Y')})"

    def __repr__(self):
        return (
            f"Event(name={self.name}, description={self.description}, "
            f"start_date={self.start_date_time}, end_date={self.end_date_time}, "
            f"location={self.location}, owner_of_event={self.owner_of_event})"
        )

    def save(self, *args, **kwargs):  # metoda pro zmenšení obrázku
        super().save(*args, **kwargs)

        if self.event_image:
            from PIL import Image

            image_path = self.event_image.path
            img = Image.open(image_path)

            max_size = (1200, 800)  # max velikost v pixelech
            img.thumbnail(max_size)
            img.save(image_path)

    def get_start_date_cz_format(self):
        return self.start_date_time.strftime("%d.%m.%Y, %H:%M")

    def get_end_date_cz_format(self):
        return self.end_date_time.strftime("%d.%m.%Y, %H:%M")

    @property
    def available_spots(self):
        return self.capacity - self.reservations.count()

    @property
    def registered_users_count(self):
        # Počet registrovaných uživatelů (rezervací)
        return self.reservations.count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(null=False, blank=False)
    date_time_posted = models.DateTimeField(auto_now=True)
    date_time_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["date_time_posted"]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.event.name}"

    def __repr__(self):
        return (
            f"Comment(event={self.event}, user={self.user}, content={self.content},"
            f" date_posted={self.date_time_posted}, time_updated={self.date_time_updated})"
        )


class Reservation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reservations"
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="reservations"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "user",
            "event",
        )  # pouze jedna rezervace na událost pro jednoho uživatele
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.username} rezervace na {self.event.name}"

    def __repr__(self):
        return f"Reservation(user={self.user}, event={self.event}, created_at={self.created_at})"

    def clean(self):
        if self.event.available_spots <= 0:
            raise ValidationError("Událost je plně obsazena.")

    def save(self, *args, **kwargs):
        self.full_clean()  # spustí clean() před uložením
        super().save(*args, **kwargs)
