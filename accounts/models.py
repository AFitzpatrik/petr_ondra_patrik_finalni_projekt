from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model, OneToOneField, CASCADE, DateField, CharField


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    date_of_birth = DateField(null=True, blank=True)
    phone = CharField(null=True, blank=True, max_length=11)

    class Meta:
        ordering = ["user__username"]

    def __repr__(self):
        return f"Profile(user={self.user})"

    def __str__(self):
        return self.user.username
