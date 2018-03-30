from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    contributions = models.IntegerField(default=0)
    contribution_points = models.IntegerField(default=0)

    def __str__(self):
        return self.username
