from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from viewer.models import Event, Type, Location, City, Country, Comment


class CommentTests(TestCase):
    def setUp(self):
        print("-" * 80)
        print(f"Spouští se test: {self._testMethodName}")

        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.country = Country.objects.create(name="Česko")
        self.city = City.objects.create(
            name="Praha", country=self.country, zip_code="10000"
        )
        self.location = Location.objects.create(
            name="Letná",
            description="Velké prostranství",
            address="Letenská pláň",
            city=self.city,
        )
        self.event_type = Type.objects.create(name="Koncert")
        self.event = Event.objects.create(
            name="Rockový večer",
            type=self.event_type,
            description="Rockový koncert na Letné",
            start_date_time="2025-08-01T18:00",
            end_date_time="2025-08-01T22:00",
            location=self.location,
            owner_of_event=self.user,
        )

    def test_anonymous_user_cannot_post_comment(self):
        response = self.client.post(
            reverse("event_detail", args=[self.event.id]), {"content": "Těším se!"}
        )
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 0)

    def test_logged_in_user_can_post_comment(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("event_detail", args=[self.event.id]),
            {"content": "Super akce!"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 1)

    def test_comment_saves_correctly_to_database(self):
        self.client.login(username="testuser", password="password")
        self.client.post(
            reverse("event_detail", args=[self.event.id]), {"content": "Už se těším!"}
        )

        comment = Comment.objects.first()
        self.assertIsNotNone(comment)
        self.assertEqual(comment.content, "Už se těším!")
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.event, self.event)