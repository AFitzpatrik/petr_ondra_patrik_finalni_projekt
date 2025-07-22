from django.test import TestCase
from django.contrib.auth.models import User
from viewer.models import Event, Reservation, Location, City, Country, Type
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

class EventCapacityTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Test Country")
        self.city = City.objects.create(name="Test City", country=self.country)
        self.location = Location.objects.create(name="Test Location", address="Ulice 1", city=self.city)
        self.type = Type.objects.create(name="Workshop")
        self.owner = User.objects.create_user(username="owner", password="pass")
        self.user1 = User.objects.create_user(username="user1", password="pass")
        self.user2 = User.objects.create_user(username="user2", password="pass")

        self.event = Event.objects.create(
            name="Testovací událost",
            type=self.type,
            location=self.location,
            start_date_time=timezone.now() + timedelta(days=1),
            end_date_time=timezone.now() + timedelta(days=1, hours=2),
            owner_of_event=self.owner,
            capacity=1
        )

    def test_event_accepts_reservation_up_to_capacity(self):
        Reservation.objects.create(user=self.user1, event=self.event)
        self.assertEqual(self.event.reservations.count(), 1)
        self.assertEqual(self.event.available_spots, 0)

    def test_event_rejects_reservation_above_capacity(self):
        Reservation.objects.create(user=self.user1, event=self.event)
        with self.assertRaises(ValidationError):
            Reservation.objects.create(user=self.user2, event=self.event)

    def test_cancel_and_re_reserve(self):
        Reservation.objects.create(user=self.user1, event=self.event)
        self.assertEqual(self.event.available_spots, 0)

        Reservation.objects.filter(user=self.user1, event=self.event).delete()
        self.assertEqual(self.event.available_spots, 1)

        Reservation.objects.create(user=self.user2, event=self.event)
        self.assertEqual(self.event.available_spots, 0)