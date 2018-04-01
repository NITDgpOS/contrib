from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    contributions = models.IntegerField(default=0)
    contribution_points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
